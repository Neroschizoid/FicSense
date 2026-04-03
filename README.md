# FicSense 📖

FicSense is an automated, AI-driven assistant designed to scrape fanfiction from multiple platforms, evaluate the storylines using semantic embeddings, and present the most relevant results straight to you via a Telegram bot interface. Stop relying on outdated tags—let the AI find you what you actually want to read.

---

## 🚀 Features

- **Multi-Source Scraping**: Collect fanfics directly from major sites using specialized web drivers.
  - **Archive of Our Own (AO3)**: Accelerated scraping mode.
  - **Webnovel**: Bypasses Cloudflare using stealth configurations (SeleniumBase UC mode).
- **Semantic Recommendation Engine**: Powered by `ollama` embeddings and cosine similarity mapping, FicSense goes beyond keyword exact matches. It understands your "intent" to rank stories intelligently by plot.
- **Telegram Interface**: Interact seamlessly with the application through a Telegram Bot. Just send your favorite fandom alongside your hidden trope desires!
- **Antigravity Managed**: Built under an Antigravity agent-first philosophy with specific run profiles and sandbox protections.

---

## 📂 Repository Structure

```text
FicSense/
├── .agents/                 # Antigravity Workspace Intelligence documents
├── config.py                # Environment & model configurations
├── core/                    # Engine & logic
│   ├── embeddings.py        # Connects to Ollama to generate vector embeddings
│   └── processor.py         # Handles and merges scraped metadata
├── data/                    # The "Fic-Vault"
│   └── raw/                 # Local JSON storage for all scraped assets
├── interface/               
│   └── telegram_bot.py      # The primary bot interface for querying
├── spiders/                 # The Scraper Engines (SeleniumBase)
│   ├── ao3_spider.py        
│   ├── base_spider.py       
│   └── webnovel_spider.py   
├── tests/                   # Testing modules for embedding accuracy
├── main.py                  # CLI orchestrator & pipeline integration
└── requirements.txt         # Project runtime dependencies
```

---

## 🛠️ Setup & Installation

### 1. Requirements

Make sure you have Google Chrome and the latest version of ChromeDriver installed on your system. This project also heavily utilizes `seleniumbase` and `ollama` for AI computation.

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file at the root of the project with the following (it is tracked nicely by our `.gitignore`):

```env
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
```

### 3. Local Model Deployment (Ollama)

You must have `ollama` running locally to compute the embeddings. Follow the [Ollama documentation](https://ollama.ai) to pull the model you have specified inside `config.py` (e.g., `nomic-embed-text`).

---

## 🤖 Usage

### Via Telegram Bot

The most robust way to use FicSense is through its dedicated bot. Boot the bot up:

```bash
python interface/telegram_bot.py
```

Send a message in the following format:
```
Fandom | Intent
```
*Example:* `onepiece | time travel ace`

### Via CLI Orchestrator

You can run a fallback pipeline directly via the command line orchestrator:

```bash
python main.py "naruto" "system user gets overpowered"
```

---

## 📜 Development Notes

- **Zombie Processes**: If you notice instability on Linux environments (e.g., ASUS TUF), the spiders have `pkill -f chrome` logic hardcoded to clean up orphaned processes before execution as a local safety measure. 
- **Wait Durations**: Scrapers use built-in waiting parameters (via `time.sleep()`). Keep this in mind when troubleshooting slow query returns.
