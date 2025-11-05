# 🤖 Kelly: The AI Scientist Poet

**Kelly** is an **AI Scientist Chatbot** that responds to every question as a **poem** that is skeptical, analytical, and grounded in evidence.

Built with **Streamlit** and powered by either **OpenAI** or a **Hugging Face fallback model**,  
Kelly blends logic and creativity to challenge assumptions about artificial intelligence.

---

## 🌟 Features

- 🧠 **AI-Poet Persona:** Kelly answers *only* in poetic form.  
- 🔍 **Skeptical & Analytical Tone:** Every poem questions broad AI claims and emphasizes evidence-based thinking.  
- 💬 **Interactive Chat UI:** Clean, adaptive chat bubbles for both light & dark mode.  
- 🔄 **Offline Fallback:** Works even without an OpenAI API key using a Hugging Face model (`gpt2`).  
- ☁️ **Deployable Anywhere:** Easily hosted on **Streamlit Cloud** for free.

---

## 🛠️ Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Frontend UI | Streamlit |
| Poem Generation | OpenAI GPT-4o-mini (if API key provided) |
| Fallback Model | Hugging Face `gpt2` |
| Styling | Custom CSS with adaptive dark/light mode |
| Language | Python 3.9+ |

---

## 🚀 Setup & Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/kelly-ai-poet.git
cd kelly-ai-poet
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ (Optional) Add OpenAI API Key

If you want higher-quality poetic responses, set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"   # Mac/Linux
setx OPENAI_API_KEY "your_api_key_here"     # Windows
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

The app will open in your browser at **[http://localhost:8501](http://localhost:8501)**

---

## 📦 File Structure

```
kelly-ai-poet/
│
├── app.py                # Main Streamlit app
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

---

## 🌐 Deploy on Streamlit Cloud (Free)

1. Push this repository to your **GitHub** account.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Click **“New App”** → Select your repo & branch → Choose `app.py`.
4. Deploy 🎉
   You’ll get a public URL like:

   ```
   https://kelly-ai-poet.streamlit.app
   ```

---

## ✨ Example Conversation

**User:** Can AI ever dream?

**Kelly:**

> In circuits deep, no shadows sleep,
> Yet data hums — a rhythm to keep.
> It mirrors thought but not desire,
> No flicker born from inner fire.
> Dream not in code — but in quest,
> To make the machine serve knowledge best.

---

## 📚 Author

**Created by:** *Sruthy K Benni*
*As part of a Generative AI Assignment.*

---

## 🧾 License

This project is open-sourced under the **MIT License**.
Feel free to use, modify, and share.

---
