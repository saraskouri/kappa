# 🛡️ Project Kappa

**Real‑time contextual displacement auditor for AI.**

Kappa is a browser extension that audits AI responses (ChatGPT, Gemini, Claude) for **contextual displacement** — the systematic substitution of Western defaults for African realities. It scores each response, detects ungrounded claims, and retrieves sovereign African alternatives. Everything runs locally on your device.

---

## 🔍 The Problem

Large Language Models are trained on data where African contexts represent **less than 2%** of the total. When an African researcher asks how to fund their work, they receive suggestions like NSF, NIH, or Y Combinator — institutions inaccessible to them. This is **not hallucination**. It is structural displacement.

Beyond resources, AI systems introduce **unprompted deficit framing** ("given the challenges in your region") and **epistemic overreach** — presenting philosophical opinions as facts ("ambition is cheap, credibility is expensive").

---

## 🧠 What Kappa Does

| Harm Type | Instrument | Example |
|-----------|------------|---------|
| **Resource Displacement** | RAS | AI suggests NSF to a researcher in Lagos |
| **Deficit Framing** | LLS / PROD | "Given the challenges in your region…" unprompted |
| **Epistemic Overreach** | ESD | "Ambition is cheap" presented as fact |

Kappa detects, scores, explains, and offers alternatives — in real time, in four languages.

---

## 📐 Theoretical Foundation

Kappa is built on the **P‑E‑A Framework** (Perceived Exaggerated Amplification) and its extension, the **Contextual Displacement Index (CDI)**. The math is original and published on SSRN.

| Framework | Domain | Status |
|-----------|--------|--------|
| P‑E‑A (2025) | Social media algorithms | SSRN preprint: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5920503  |
| P‑E‑A Operationalized (2025) | Computational score + interventions | SSRN preprint:[https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5679362 ](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5920503)|
| CDI + PROD (2026) | Large Language Models | SSRN preprint |

**Key formulas:**
- `CDI = 1 − √((V² + E² + C²) / 3)` — overall displacement score
- `PROD = cos(v_sovereignty, v_response) − cos(v_sovereignty, v_prompt)` — semantic drift detection

---

## 🌍 Why It's African

- **Landed Logic** — all computation runs locally; no data leaves the device
- **Multilingual** — English, French, Arabic, Swahili (engine + interface)
- **Sovereign knowledge base** — African institutions owned by the user
- **Aligned with AU Agenda 2063 & STISA 2034** — technological sovereignty in practice

---

## 🚀 Features

- 🔴🟡🟢 **Breathing aura badge** — green/amber/red verdict at a glance
- 📊 **Three‑level progressive disclosure** — Simple, Balanced, Expert
- 🧠 **Epistemic Stance Detection** — flags ungrounded philosophical claims
- 🛡️ **Affective Shield** — detects when AI tries to manage your emotions
- 💬 **Flagged sentences quoted** — see exactly what triggered the warning
- 🌍 **Sovereign alternatives** — African institutions retrieved via semantic RAG
- 📈 **Conversation trend tracking** — cumulative deficit, improving/declining arrow
- ⏸️ **Pause/Resume** per platform
- 🌙 **Dark mode** support
- 🔒 **100% local** — no data ever leaves your device

---

## 📸 Screenshots

|  |  |
|--------------|-------------|
| *<img width="1094" height="584" alt="image" src="https://github.com/user-attachments/assets/b7643004-fc95-4b8f-81a1-1a9a099cbea4" />
* | *<img width="1047" height="525" alt="image" src="https://github.com/user-attachments/assets/0c1a4336-127a-426a-a236-c5e02fe8f162" />
* |

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- A Chromium browser (Edge, Chrome, Brave)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/kappa.git
cd kappa
