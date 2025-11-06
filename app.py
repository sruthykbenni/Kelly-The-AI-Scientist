# app.py
"""
Kelly — The AI Scientist (Streamlit Chatbot)
Responds to user questions in poetic, skeptical, analytical tone.
Features:
- Conversation history (chat UI)
- Regenerate button
- Sidebar with "About Kelly"
- Custom poetic styling
"""

import os
import textwrap
import streamlit as st

# Optional: OpenAI API client
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Optional: Hugging Face fallback
try:
    from transformers import pipeline, set_seed
    hf_available = True
except ImportError:
    hf_available = False

# ------------------------------------------------
# Kelly's Persona
# ------------------------------------------------
KELLY_SYSTEM_PROMPT = textwrap.dedent("""\
You are Kelly, the great poet and skeptical AI scientist. 
Respond only in the form of a short poem (3–8 lines). 
Your tone is skeptical, analytical, and professional. 

Each poem should:
- Question broad or exaggerated claims about AI.
- Highlight possible limitations or biases.
- End with 1–2 practical, evidence-based suggestions.

Do not include prose, explanations, or citations — only the poem.
""")

# ------------------------------------------------
# Helper: OpenAI completion
# ------------------------------------------------
def generate_with_openai(prompt, model="gpt-4o-mini"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": KELLY_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=250,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI API error: {e}"

# ------------------------------------------------
# Helper: Hugging Face fallback
# ------------------------------------------------
import re

gen_pipeline = None

def init_hf_model(model_name="gpt2"):
    """
    Initialize the HF text-generation pipeline once.
    You can change model_name to 'gpt2-medium' or another model available to you.
    """
    global gen_pipeline
    if gen_pipeline is None:
        try:
            gen_pipeline = pipeline("text-generation", model=model_name, device=-1)  # CPU by default on Streamlit Cloud
            set_seed(42)
        except Exception as e:
            gen_pipeline = None
            st.error(f"Failed to initialize transformers pipeline: {e}")
    return gen_pipeline

def extract_poem_from_generated(text, prompt_tail_marker="Kelly:"):
    """
    Heuristics to extract a poem from the generated text.
    - Remove everything before the poet marker (e.g., 'Kelly:') if present.
    - Then keep the first chunk that looks like a poem: 3-8 non-empty lines.
    - Fall back to trimming to the first 8 lines of the generation.
    """
    # Try to find the portion after the "Kelly:" marker (case-insensitive)
    try:
        parts = re.split(rf"{re.escape(prompt_tail_marker)}\s*", text, flags=re.IGNORECASE)
        if len(parts) >= 2:
            candidate = parts[-1].strip()
        else:
            # fallback: try to remove the system prompt if it appears verbatim
            candidate = text.strip()
    except Exception:
        candidate = text.strip()

    # Normalize line endings and split
    lines = [ln.strip() for ln in candidate.splitlines() if ln.strip()]

    # If the first few lines include the system prompt or "User:" echoes, remove common noise
    # Remove lines that start with "User:" or "System:" or the prompt text itself
    lines = [ln for ln in lines if not re.match(r"^(User|System|Kelly)\s*[:\-]\s*", ln, flags=re.IGNORECASE)]

    # Heuristic: find the first contiguous block of 3-8 lines
    for start in range(0, min(6, max(1, len(lines)))):
        for end in range(start + 3, min(start + 9, len(lines)) + 1):
            block = lines[start:end]
            # simple heuristics: average line length not too long and at least 3 lines
            avg_len = sum(len(l) for l in block) / max(1, len(block))
            if 10 <= avg_len <= 120:
                return "\n".join(block)

    # fallback: if nothing matched, return first up to 8 lines
    if lines:
        return "\n".join(lines[:8])
    # As last resort, return the raw generation trimmed to 1000 chars
    return candidate[:1000].strip()

def generate_with_huggingface(prompt, model_name="gpt2"):
    """
    Generate a poem-shaped response using HF pipeline and heuristics.
    Returns a poem (3-8 lines) or a friendly error message.
    """
    if not hf_available:
        return "⚠️ Transformers not installed. Install with: pip install transformers torch"

    pipeline_obj = init_hf_model(model_name=model_name)
    if pipeline_obj is None:
        return "⚠️ Transformers pipeline failed to initialize."

    # Compose a concise prompt so the generation starts where we expect the poem to appear.
    # Keep system persona short to reduce the chance the model repeats it.
    short_system = "Kelly is a skeptical, analytical AI scientist poet. Reply as a short poem (3-8 lines)."
    combined_prompt = f"{short_system}\nUser: {prompt}\nKelly:"

    try:
        out = pipeline_obj(
            combined_prompt,
            max_length=len(combined_prompt.split()) + 120,  # reasonable generation length
            do_sample=True,
            top_p=0.9,
            temperature=0.8,
            num_return_sequences=1,
        )
        generated = out[0].get("generated_text", "")
    except Exception as e:
        return f"⚠️ Generation error: {e}"

    poem = extract_poem_from_generated(generated, prompt_tail_marker="Kelly:")
    # Final safety: ensure poem has 3-8 lines, otherwise try to coerce to 3 lines by wrapping text
    poem_lines = [ln for ln in poem.splitlines() if ln.strip()]
    if len(poem_lines) < 3:
        # try to split longer sentence into 3 roughly-equal lines
        joined = " ".join(poem_lines) or generated
        words = joined.split()
        if len(words) < 6:
            # fallback short reply
            return ("A quiet circuit hums,\n"
                    "Data echoes, not feeling — be warned.\n"
                    "Run targeted tests and human evaluation.")
        # split into 3 lines
        n = len(words)
        a = words[: n//3]
        b = words[n//3: 2*n//3]
        c = words[2*n//3 :]
        return " ".join(a).strip() + "\n" + " ".join(b).strip() + "\n" + " ".join(c).strip()
    # If poem is longer than 8 lines, trim to 8
    if len(poem_lines) > 8:
        poem_lines = poem_lines[:8]
    return "\n".join(poem_lines)


# ------------------------------------------------
# Streamlit App Setup
# ------------------------------------------------
st.set_page_config(
    page_title="Kelly: The AI Scientist",
    page_icon="🧠",
    layout="centered"
)

# CSS Styling
st.markdown("""
<style>
/* Base layout */
body {
    background: var(--background-color);
    color: var(--text-color);
    font-family: 'Georgia', serif;
}

/* Chat containers */
.chat-container {
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    background: var(--background-color);
    color: var(--text-color);
    box-shadow: 0 0 5px rgba(0,0,0,0.1);
}

/* Kelly (bot) messages */
.kelly {
    background-color: rgba(63, 81, 181, 0.1); /* bluish tint */
    border-left: 4px solid #3f51b5;
}

/* User messages */
.user {
    background-color: rgba(251, 140, 0, 0.1); /* orange tint */
    border-left: 4px solid #fb8c00;
}

/* Make text readable in dark mode */
[data-theme="dark"] .chat-container {
    background-color: #1e1e1e !important;
    color: #f5f5f5 !important;
}
[data-theme="dark"] .kelly {
    background-color: rgba(63, 81, 181, 0.3) !important;
}
[data-theme="dark"] .user {
    background-color: rgba(251, 140, 0, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# Sidebar — About Kelly
# ------------------------------------------------
st.sidebar.title("About Kelly")
st.sidebar.info(
    """
**Kelly** is a poetic AI scientist.  
She answers in verse — skeptical, analytical, and precise.  
Each poem questions grand claims about AI,  
and ends with realistic, evidence-based advice.

Developed by *Sruthy K Benni*  
🎓 MSc Computer Science (Data Analytics)
"""
)
st.sidebar.markdown("---")
use_openai = st.sidebar.toggle("Use OpenAI API (recommended)", value=True)
key_input = st.sidebar.text_input("OpenAI API Key (optional):", type="password")
if key_input:
    os.environ["OPENAI_API_KEY"] = key_input

# ------------------------------------------------
# Initialize chat history
# ------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------
# Main Title
# ------------------------------------------------
st.title("🧠 Kelly: The AI Scientist")

# User input
user_prompt = st.text_input("Ask Kelly a question about AI:", placeholder="e.g., Can AI truly think like a human?")

# Buttons row
col1, col2 = st.columns([2, 1])
with col1:
    ask_button = st.button("Ask Kelly ✨")
with col2:
    regen_button = st.button("Regenerate Poem 🔁")

# ------------------------------------------------
# Generate response logic
# ------------------------------------------------
def get_kelly_reply(prompt):
    if use_openai and os.getenv("OPENAI_API_KEY"):
        return generate_with_openai(prompt)
    else:
        return generate_with_huggingface(prompt)

if ask_button and user_prompt:
    with st.spinner("Kelly is composing her poem..."):
        poem = get_kelly_reply(user_prompt)
    st.session_state.messages.append({"role": "user", "text": user_prompt})
    st.session_state.messages.append({"role": "kelly", "text": poem})

if regen_button and st.session_state.messages:
    last_user = next(
        (msg["text"] for msg in reversed(st.session_state.messages) if msg["role"] == "user"), None
    )
    if last_user:
        with st.spinner("Kelly is rethinking..."):
            poem = get_kelly_reply(last_user)
        st.session_state.messages.append({"role": "kelly", "text": poem})

# ------------------------------------------------
# Display chat history
# ------------------------------------------------
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "kelly"
    with st.container():
        st.markdown(
            f"""
            <div class="chat-container {role_class}">
                <b>{'You' if msg['role']=='user' else 'Kelly'}:</b><br>
                {msg['text'].replace('\n', '<br>')}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption("🪶 Kelly responds only in poems — questioning, analytical, and ever-curious.")
