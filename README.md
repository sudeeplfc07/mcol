# MCOL — Multi-Code Orchestration Layer

> Never lose your coding conversation to a rate limit again.

A terminal-based AI coding assistant that lets you choose between **Claude, DeepSeek, and Qwen on every prompt** — with full conversation history preserved across model switches.

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/sudeeplfc07/mcol)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

</div>

---

## The problem

You're deep into a debugging session with Claude. The model has read your codebase, understood your architecture, and is mid-explanation of a fix. Then you hit a rate limit.

Now you have to either wait an hour and lose flow, switch to another tool and rebuild context from scratch, or pay for a higher tier and hope it doesn't happen again.

**MCOL treats the conversation as the unit of work, not the model.** You can switch models mid-conversation — Claude to DeepSeek to Qwen and back — and every model sees the full history. No context loss, no re-prompting, no rebuilding.

---

## Features

- 🔀 **Per-prompt model selection** — pick your model for each turn, not once at the start
- 🧠 **Shared conversation memory** — full history preserved across all models
- 🔁 **Automatic rate-limit detection** — when one model hits a limit, MCOL prompts for fallback
- 🧩 **Provider-adapter architecture** — adding a new model means one adapter class, nothing else changes
- 🔒 **Local-first** — your API keys, your machine, your data; nothing leaves except the API calls you make
- 💸 **Zero infrastructure cost** — no servers, no databases, just `pip install` and go

---

## Quick start

### 1. Install

```bash
git clone https://github.com/sudeeplfc07/mcol.git
cd mcol
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` with the keys for the providers you want to use. You only need keys for the models you plan to actually call.

```env
# Anthropic Claude  — https://console.anthropic.com
ANTHROPIC_API_KEY=your_claude_key_here

# DeepSeek         — https://platform.deepseek.com
DEEPSEEK_API_KEY=your_deepseek_key_here

# Qwen / DashScope — https://dashscope.aliyuncs.com
QWEN_API_KEY=your_qwen_key_here
```

### 3. Run

```bash
python3 cli.py
```

On each prompt, choose a model from the menu. If a rate limit is hit mid-conversation, MCOL detects it automatically and asks which model you want to continue with. The full conversation history is preserved.

---

## Architecture

```
                    ┌─────────────────────┐
   User CLI  ───►   │    Orchestrator     │   ◄─── model selection,
                    │                     │        fallback routing,
                    └──────────┬──────────┘        conversation state
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌────────────┐
       │  Claude    │   │  DeepSeek  │   │   Qwen     │
       │  Adapter   │   │  Adapter   │   │  Adapter   │
       └─────┬──────┘   └──────┬─────┘   └──────┬─────┘
             │                 │                │
             └─────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Shared Memory     │   ◄─── full chat history
                    │   (conversation     │        across all models
                    │     transcript)     │
                    └─────────────────────┘
```

Each provider is normalised into a common adapter interface. The orchestrator handles model selection, rate-limit detection, and fallback. Memory is shared at the orchestrator level — every model gets the full conversation context on every call.

---

## Adding a new model

Each provider lives as a single adapter file. To add a new model:

1. Create a new adapter following the same shape as the existing ones (see `adapters/` in the repo)
2. Register it with the orchestrator
3. Add the API key reference to `.env.example`

The orchestrator, memory layer, and CLI work without modification. Most adapters are 50–100 lines.

PRs adding new model adapters are especially welcome.

---

## Roadmap

- [ ] **RAG memory engine** — embedding-based long-term memory via ChromaDB so MCOL can recall earlier conversations
- [ ] **MCP server integration** — expose MCOL as an MCP server so it works with any MCP-compatible client
- [ ] **Continue.dev integration** — bring MCOL routing into VS Code as an extension
- [ ] **Streaming responses** — token-by-token output for faster perceived latency on long responses
- [ ] **Per-conversation budgets** — set token or cost caps per session

---

## Why MCOL exists

Built by [Sudeep Gyawali](https://www.linkedin.com/in/sudeep-gyawali/) — a Cloud & Network Infrastructure Engineer who got tired of losing context every time a rate limit interrupted a real debugging session. MCOL is the tool I wished existed.

If MCOL saves you an hour of context-rebuilding, please ⭐ the repo. It helps others find it.

---

## Contributing

Contributions are welcome — especially new model adapters and roadmap items.

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes (and add a quick test if applicable)
4. Submit a PR with a clear description of what and why

---

## License

MIT — see [LICENSE](./LICENSE). Free to use, modify, and distribute.
