# ResearchMind 🔎

A multi-agent research assistant built with LangChain, Ollama, and Streamlit. ResearchMind automates end-to-end topic research by coordinating specialized agents in a streamlined pipeline.

## 🚀 Architecture & Pipeline

```text
User Topic
    ↓
1. Search Agent   → Finds recent, reliable sources using Tavily Search
    ↓
2. Reader Agent   → Scrapes and extracts full content from the most relevant source
    ↓
3. Writer Chain   → Synthesizes research into a structured, professional report
    ↓
4. Critic Chain   → Rigorously reviews the report, scores it (X/10), and provides feedback
```

---

## 🛠️ Tech Stack

- **Framework**: LangChain, LangChain Core, LangChain Ollama
- **UI**: Streamlit
- **Search & Scraping**: Tavily Search API, BeautifulSoup4, Requests
- **LLM**: Ollama (`gpt-oss:120b-cloud` / configurable)

---

## 📦 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/napapijri5248/ResearchMind.git
cd ResearchMind
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API credentials:
```bash
cp .env.example .env
```

```env
GROQ_API_KEY=your_groq_api_key_here
OLLAMA_API_KEY=your_ollama_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

---

## 💻 Usage

### Run Streamlit Web Application
```bash
streamlit run app.py
```

### Run Terminal Pipeline
```bash
python pipeline.py
```

---

## 📄 License

MIT License.
