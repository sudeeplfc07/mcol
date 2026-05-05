# MCOL – Multi Code Orchestration Layer

A terminal‑based coding assistant that lets you pick **Claude, DeepSeek, Qwen** (and more) **on every prompt**.  
If one model hits a rate limit, you instantly continue with another – **the conversation is fully preserved**.

---

## ✨ Features

- 🔀 Model selection every prompt  
- 🔁 Seamless mid‑conversation fallback on rate limits  
- 🧠 Shared chat history across all models  
- 🧩 Easily add new models (one adapter class)  
- 🔒 API keys kept in local `.env` – never committed  

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/mcol.git
cd mcol
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your real API keys

## ⚙️ Configuration

Edit your `.env` file with your API keys:

```env
ANTHROPIC_API_KEY=your_claude_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
OPENAI_API_KEY=your_qwen_key_here   # Qwen uses OpenAI-compatible API
```

Get your keys:
- Claude → [console.anthropic.com](https://console.anthropic.com)
- DeepSeek → [platform.deepseek.com](https://platform.deepseek.com)
- Qwen → [dashscope.aliyuncs.com](https://dashscope.aliyuncs.com)

---

## 🚀 Usage

```bash
python3 cli.py
```

On each prompt, select your model. If a rate limit is hit, MCOL detects it 
automatically and asks which model to continue with — full conversation history 
is preserved.

---

## 🏗️ Architecture
User (CLI)
│
┌───────────────┐
│  Orchestrator │  ← model selection, fallback, conversation state
└──────┬────────┘
│
┌──────┼──────────┐
│      │          │
Claude DeepSeek  Qwen  ← normalised via adapters
│
┌──────┴──────────┐
│  Shared Memory  │  ← full chat history across all models

## 🤝 Contributing

Contributions welcome — especially new model adapters.

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 📄 License

MIT — free to use, modify, and distribute.
