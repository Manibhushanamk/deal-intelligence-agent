# Deal Intelligence Agent (DIA) 🚀

> **Autonomous Cognitive Co-Pilot for B2B Revenue Teams** powered by **Hindsight Persistent Memory**, **Neon Database**, and **Google Workspace MCP Actions**.

---

## 📌 Executive Summary

The **Deal Intelligence Agent (DIA)** is built for the **HackwithHyderabad 3.0 / Hindsight AI Agents Hackathon**. Unlike stateless AI chatbots that forget past conversations, DIA leverages Vectorize's **Hindsight Memory System** to continuously remember client disclosures, objection history, stakeholder sentiment, and competitive benchmarks across multi-month sales motions.

DIA integrates standardized **Model Context Protocol (MCP)** tool handlers to execute Google Workspace actions (Calendar scheduling with Google Meet links, Gmail draft compilation) and persist structured deal states directly into a **Neon PostgreSQL** database.

---

## 🏛 Repository & System Architecture

```text
deal-intelligence-agent/
├── pyproject.toml              # Build & dependency specifications
├── README.md                   # Comprehensive documentation
├── demo.py                     # Executable end-to-end enterprise scenario runner
├── src/
│   ├── agent/
│   │   ├── core.py             # Main cognitive orchestration loop
│   │   └── state.py            # Agent state graph & execution context
│   ├── memory/
│   │   ├── hindsight_client.py # Hindsight SDK retain & recall client wrapper
│   │   └── schema.py           # Pydantic models for memory payloads & facts
│   ├── analytics/
│   │   ├── cross_deal.py       # Recurring pain points & product gap feedback
│   │   ├── relationship.py     # Trajectory tracker, influence map & health score
│   │   ├── competitive.py      # Competitor extraction & battlecards
│   │   └── win_loss.py         # Probabilistic win scoring & Next-Best-Action
│   ├── workspace/
│   │   ├── calendar_service.py # Google Calendar scheduling & FreeBusy
│   │   ├── gmail_service.py    # Gmail draft compilation & dispatch
│   │   └── neon_client.py     # Neon PostgreSQL database client
│   ├── mcp/
│   │   ├── workspace_tools.py  # Standardized MCP tool definitions
│   │   └── server.py           # MCP server implementation
│   └── narrative/
│       ├── pitch_builder.py    # Dynamic sales pitch narrative synthesis
│       └── report_generator.py # PDF Deal Dossier & Google Docs exporter
└── tests/
    ├── test_hindsight_memory.py
    ├── test_workspace_actions.py
    └── test_intelligence_modules.py
```

---

## ⚡ Key Features & Hindsight Memory Layer

### 1. Persistent Memory via Hindsight SDK
* **`retain` Pipeline**: Inscribes call transcripts, meeting notes, and email threads into namespace-isolated Hindsight memory with idempotent upsert logic.
* **`recall` Pipeline**: Multi-hop semantic retrieval querying compliance requirements (SOC2, HIPAA), technical stack prerequisites (SAML 2.0 SSO), and budget constraints.
* **Fact Extraction**: Parses explicit and implicit client disclosures into categorized facts.

### 2. Core Intelligence Modules
* **Cross-Deal Trend Analytics**: Clusters unstructured interaction notes to quantify recurring customer pain points and feed product feature gap loops.
* **Multi-Session Relationship Intelligence**: Maps internal champions, economic buyers, technical evaluators, and blockers while computing a composite **Account Health Score** (0–100).
* **Real-Time Competitive Intelligence**: Scans transcripts for competitor mentions (**Salesforce, HubSpot, Gong**), triggers contextual battlecards, and tracks pipeline density.
* **Predictive Win-Loss Reasoning**: Multi-factor deal scoring assessing stage dwell time, buyer coverage, and budget alignment with prescriptive **Next-Best-Actions (NBA)**.

### 3. Google Workspace & Neon DB MCP Integration
* **`google_calendar_schedule`**: Resolves FreeBusy windows and schedules meetings with Google Meet links attached.
* **`gmail_create_draft`**: Compiles RFC 2822 compliant, HTML-formatted follow-up emails staged for human-in-the-loop review.
* **`neon_persist_deal_record`**: Persists structured deal state and metadata directly to Neon PostgreSQL using SQLAlchemy.

---

## 🚀 Quickstart & Setup

### Prerequisites
* Python 3.11 or higher
* `pip` / `virtualenv`

### Installation
```bash
# Clone the repository
git clone https://github.com/vectorize-io/deal-intelligence-agent.git
cd deal-intelligence-agent

# Install project dependencies
pip install -e .
```

### Running Unit Tests
```bash
pytest tests/ -v
```

### Running the End-to-End Enterprise Demo
```bash
python demo.py
```
*Executes a full scenario for Acme Corporation ($185k ARR), displays DIA analytics & staged MCP actions, and outputs `acme_corp_deal_dossier.pdf`.*

---

## 🛠 Configuration & Environment Variables

Create a `.env` file or export the following environment variables:

```bash
# Hindsight SDK Credentials
export HINDSIGHT_API_KEY="your_hindsight_api_key"
export HINDSIGHT_BASE_URL="https://api.hindsight.vectorize.io"

# Neon PostgreSQL Connection
export NEON_DATABASE_URL="postgresql://user:password@ep-sample-neon.pooler.us-east-2.aws.neon.tech/neondb"

# Google Workspace OAuth Credentials
export GOOGLE_CLIENT_ID="your_google_client_id"
export GOOGLE_CLIENT_SECRET="your_google_client_secret"
export GOOGLE_REFRESH_TOKEN="your_google_refresh_token"

# LLM Provider Key (Groq / OpenAI)
export GROQ_API_KEY="your_groq_api_key"
export LLM_MODEL="qwen/qwen3-32b"
```

---

## 📄 License
MIT License. Built for the HackwithHyderabad 3.0 / Hindsight AI Agents Hackathon.
