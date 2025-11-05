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
gen_pipeline = None
def generate_with_huggingface(prompt):
    global gen_pipeline
    if not hf_available:
        return "⚠️ Transformers not available. Install with: pip install transformers torch"
    if gen_pipeline is None:
        gen_pipeline = pipeline("text-generation", model="gpt2")
        set_seed(42)
    text = gen_pipeline(
        f"{KELLY_SYSTEM_PROMPT}\nUser: {prompt}\nKelly:",
        max_length=180,
        temperature=0.8,
        top_p=0.9,
        num_return_sequences=1,
    )[0]["generated_text"]
    lines = text.splitlines()[-10:]
    return "\n".join(lines)

# ------------------------------------------------
# Streamlit App Setup
# ------------------------------------------------
st.set_page_config(
    page_title="Kelly — The AI Scientist",
    page_icon="🧠",
    layout="centered"
)

# CSS Styling
st.markdown("""
<style>
body {
    background: #f4f4f9;
    color: #222;
    font-family: 'Georgia', serif;
}
.chat-container {
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    background: #ffffff;
    box-shadow: 0 0 5px rgba(0,0,0,0.1);
}
.kelly {
    background-color: #e8eaf6;
    border-left: 4px solid #3f51b5;
}
.user {
    background-color: #fff3e0;
    border-left: 4px solid #fb8c00;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Sidebar — About Kelly
# ------------------------------------------------
st.sidebar.title("🧬 About Kelly")
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
st.title("🧠 Kelly — The AI Scientist")

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
