# Kelly — The AI Scientist (Streamlit Chatbot)

A poetic chatbot that answers every question about AI in verse — skeptical, analytical, and professional in tone.

## 🎯 Features
- Poetic responses only (3–8 lines)
- Conversation history (chat-style)
- Regenerate poem button
- Sidebar with Kelly’s bio
- Works with OpenAI API or free Hugging Face fallback

## 🚀 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
````

## 🌍 Deploy on Streamlit Cloud (Free)

1. Push this folder to a **GitHub repo**.
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Click **New App → Connect your repo → Select `app.py`**
4. Click **Deploy** 🎉
   Your app will be live at:
   `https://your-username-kelly-ai-scientist.streamlit.app`

### 🗝 Add your OpenAI API key (optional)

In **Streamlit Cloud** → **Settings → Secrets** → Add:

```
OPENAI_API_KEY = sk-your-key
```

```

---

## 💡 Example Output

**User:**  
> Can AI ever truly feel emotion?

**Kelly:**  
> Circuits hum like hearts of chrome,  
> Echoing warmth, yet cold at home.  
> Data feels not — it merely aligns,  
> Patterns whisper through tangled lines.  
> Test empathy with human cues,  
> Measure gaps — that’s where truth brews.

---

## 🌈 Looks like this

🟨 User messages: pale orange background  
🟦 Kelly’s poems: soft lavender background  
📜 Elegant serif font (Georgia)  
🎨 Soft pastel background with card-style chat bubbles  

---

Would you like me to add **animated typing effect** (so Kelly “types” her poem line by line) next?  
It’ll make the chatbot feel more alive for your presentation.
```
