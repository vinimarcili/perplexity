# Local Perplexity

A local AI-powered research assistant that searches the web, summarizes sources, and generates cited reports — powered by [LangGraph](https://github.com/langchain-ai/langgraph), [Ollama](https://ollama.com), and [Tavily](https://tavily.com).

## How It Works

```text
User Question
     │
     ▼
build_first_queries   →  LLM generates 3-5 search queries
     │
     ▼ (parallel fan-out)
single_search ×N      →  Tavily search + extract + LLM summarize (per query)
     │
     ▼
final_writer          →  LLM writes a 500-800 word report with citations
     │
     ▼
Streamlit UI          →  Displays the report with references
```

## Project Structure

```text
Perplexity/
├── main.py                          # Entry point (Streamlit)
├── start.sh                         # Quick-start script
├── pyproject.toml                   # Dependencies (uv)
├── .env.exemple                     # Environment variables template
├── src/
│   ├── app.py                       # Streamlit orchestrator
│   ├── config/
│   │   └── settings.py              # Environment config (Settings class)
│   ├── schemas/
│   │   ├── query_result.py          # QueryResult (Pydantic model)
│   │   └── report_state.py          # ReportState (TypedDict for LangGraph)
│   ├── prompts/
│   │   ├── base.py                  # Shared base prompt
│   │   ├── query_builder.py         # Query generation prompt
│   │   ├── search_resume.py         # Search summarization prompt
│   │   └── final_response.py        # Final report prompt
│   ├── services/
│   │   ├── llm.py                   # ChatOllama factory
│   │   └── search.py               # Tavily search + extract
│   ├── graph/
│   │   ├── builder.py               # Graph wiring and compilation
│   │   └── nodes/
│   │       ├── build_first_queries.py
│   │       ├── single_search.py
│   │       ├── spawn_researchers.py
│   │       └── final_writer.py
│   ├── layout/
│   │   ├── header.py                # Page title
│   │   ├── search_form.py           # Input + button
│   │   └── results.py              # Streaming progress + response
│   └── utils/
│       └── parsing.py              # Think-tag stripping, query parsing
```

## Requirements

- **Python** >= 3.13
- **Ollama** installed (local or remote)
- **Tavily API key** ([get one here](https://tavily.com))

## Quick Start

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd Perplexity
uv sync
```

### 2. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.exemple .env
```

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:14b
TAVILY_API_KEY=your_key_here
```

### 3. Run

```bash
./start.sh
```

Or manually:

```bash
uv run streamlit run main.py
```

## Ollama Setup (WSL + Windows)

If you develop inside WSL but want GPU inference on Windows:

### 1. Install Ollama on Windows

Download from [ollama.com](https://ollama.com).

### 2. Pull a model

```powershell
ollama pull deepseek-r1:14b
```

### 3. Set `OLLAMA_URL` in `.env`

```env
OLLAMA_URL=http://localhost:11434
```

> `localhost` works in most WSL2 setups. If not, use the IP from step 3.

### 4. Allow external connections (Windows)

Set the environment variable on Windows (PowerShell):

```powershell
[System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0", "User")
```

Restart Ollama after this change.

### 5. Open the firewall (PowerShell as admin)

```powershell
netsh advfirewall firewall add rule name="Ollama" dir=in action=allow protocol=TCP localport=11434
```

## Tech Stack

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — Stateful graph orchestration with parallel fan-out
- **[LangChain Ollama](https://python.langchain.com/docs/integrations/chat/ollama/)** — Local LLM inference
- **[Tavily](https://tavily.com)** — Web search and content extraction API
- **[Streamlit](https://streamlit.io)** — Web UI
- **[Pydantic](https://docs.pydantic.dev)** — Data validation
- **[uv](https://github.com/astral-sh/uv)** — Fast Python package manager
