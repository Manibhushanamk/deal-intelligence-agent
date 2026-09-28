# Deal Intelligence Agent (DIA) 🚀

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pytest 100% Passing](https://img.shields.io/badge/pytest-100%25%20Passing-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Standard%20v1.0-blueviolet.svg?style=flat)](https://modelcontextprotocol.io/)
[![Neon DB Powered](https://img.shields.io/badge/Neon-Serverless%20PostgreSQL-00E599.svg?style=flat&logo=postgresql&logoColor=white)](https://neon.tech/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)

> **Autonomous Cognitive Co-Pilot for Enterprise B2B Revenue Teams** powered by **Hindsight Persistent Memory**, **Neon Serverless PostgreSQL**, and **Model Context Protocol (MCP) Google Workspace Automation**.

---

## 📌 Executive Summary & Problem-Solution

Enterprise B2B sales cycles span 6 to 18 months across dozens of fragmented stakeholder calls, email threads, and shifting procurement hurdles. Traditional CRM tools and stateless LLM wrappers suffer from **contextual amnesia**—they lose critical historical disclosures when Account Executives switch, fail to retain technical compliance constraints across quarters, and lack the autonomous agency to proactively protect pipeline health.

**Deal Intelligence Agent (DIA)** bridges this chasm by pairing an autonomous cognitive agent with **Vectorize's Hindsight Persistent Memory Layer**. DIA retains and synthesizes historical disclosures across calls, calculates multi-vector deal health and competitive battlecards, persists structured deal records to **Neon PostgreSQL**, and stages human-in-the-loop **Google Workspace actions** (Calendar scheduling and Gmail drafts), culminating in an executive-ready **Deal Dossier PDF**.

---

## 🏛 Architecture & Data Flow

### End-to-End Lifecycle Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Rep as Account Executive / Client
    participant Agent as Deal Intelligence Agent
    participant Memory as Hindsight Memory SDK
    participant Analytics as Multi-Vector Analytics Engine
    participant Pitch as Narrative & Pitch Synthesizer
    participant MCP as Workspace MCP Server
    participant DB as Neon PostgreSQL
    participant Dossier as ReportLab Dossier Engine

    Rep->>Agent: Ingest Interaction (Transcript / Notes / Email)
    Agent->>Memory: retain(namespace=account_id, key=interaction_id, payload)
    Note over Memory: Inscribes facts & categories<br/>(budget, technical, competitor)
    Agent->>Memory: recall(namespace=account_id, query="compliance, budget, sso")
    Memory-->>Agent: High-precision semantic contextual memories

    Agent->>Analytics: Execute Multi-Vector Diagnostics
    Note over Analytics: Relationship Intelligence (Health Score 0-100)<br/>Competitive Battlecards (Salesforce/HubSpot/Gong)<br/>Cross-Deal Gap Loops & Win-Loss NBA
    Analytics-->>Agent: Structured Risk Vectors, Health & Win Probability

    Agent->>Pitch: Synthesize Pitch Narrative & Value Proposition
    Pitch-->>Agent: Dynamic Executive Summary

    Agent->>MCP: Stage Workspace Actions
    MCP->>DB: neon_persist_deal_record(account_id, opportunity_id, state)
    MCP-->>Agent: Staged Gmail Draft (RFC 2822) & Google Meet Calendar Event

    Agent->>Dossier: Generate PDF Deal Dossier
    Dossier-->>Rep: acme_corp_deal_dossier.pdf (Ready for Executive Review)
```

---

## 📂 Codebase Directory & File Responsibilities

```text
deal-intelligence-agent/
├── pyproject.toml                     # PEP 621 build configuration and dependency matrix
├── README.md                          # Executive submission showcase & technical documentation
├── demo.py                            # Standalone end-to-end enterprise scenario runner
├── acme_corp_deal_dossier.pdf         # Sample generated high-resolution PDF Deal Dossier
├── src/
│   ├── config.py                      # Pydantic BaseSettings loading .env and fallback defaults
│   ├── agent/
│   │   ├── core.py                    # Master cognitive loop orchestrating memory, analytics, MCP & PDF
│   │   └── state.py                   # Pydantic AgentState tracking deal lifecycle and diagnostics
│   ├── memory/
│   │   ├── hindsight_client.py        # Hindsight API client with namespace partitioning & offline fallback
│   │   └── schema.py                  # Pydantic models for interactions, stakeholders, opportunities & facts
│   ├── analytics/
│   │   ├── cross_deal.py              # Cross-account trend clustering & lost-deal product gap feedback loops
│   │   ├── relationship.py            # Stakeholder influence mapping & 0-100 Account Health scoring formula
│   │   ├── competitive.py             # Transcript competitor extraction, battlecards & pipeline density
│   │   └── win_loss.py                # Multi-factor stage dwell decay, budget risk & Next-Best-Action (NBA)
│   ├── workspace/
│   │   ├── calendar_service.py        # Google Calendar FreeBusy resolution & Meet link scheduling
│   │   ├── gmail_service.py           # RFC 2822-compliant HTML email draft compiler
│   │   └── neon_client.py             # SQLAlchemy client persisting state to Neon PostgreSQL
│   ├── mcp/
│   │   ├── workspace_tools.py         # Standardized Model Context Protocol (MCP) tool schemas & execution
│   │   └── server.py                  # MCP server exposing JSON-RPC tool endpoints
│   └── narrative/
│       ├── pitch_builder.py           # Context-aware sales narrative synthesis and objection-handling
│       └── report_generator.py        # ReportLab PDF Deal Dossier generator & Google Docs export schema
└── tests/
    ├── test_hindsight_memory.py       # Unit tests for retain, recall, and fact extraction pipelines
    ├── test_intelligence_modules.py   # Unit tests for cross-deal, relationship, competitive, and win-loss
    └── test_workspace_actions.py      # Unit tests for Calendar, Gmail, and MCP server tool execution
```

---

## 🔬 Core Subsystems Deep Dive

### 1. Hindsight Memory SDK Layer (`src/memory/`)

The memory foundation is encapsulated in `HindsightClient`, implementing:
* **Namespace Partitioning:** Every client account is isolated within its own dedicated namespace (`namespace=account_id`). This guarantees zero cross-tenant memory leakage while enabling account-level longitudinal context retention.
* **Idempotent Retention (`retain`):** Automatically detects existing interaction IDs, updating state when transcripts are enriched and appending new interaction events with ISO 8601 timestamps.
* **Multi-Hop Semantic Recall (`recall`):** Employs semantic term intersection and relevance weighting across stored interaction payloads, retrieving historical compliance disclosures (e.g., SOC2 Type II, HIPAA, SAML 2.0 SSO) made months prior.
* **Automated Fact Extraction (`extract_facts`):** Automatically categorizes extracted statements into three critical deal dimensions:
  * `budget`: Budget ceilings, cost objections, payment terms.
  * `technical`: Infrastructure constraints, auth prerequisites, data residency.
  * `competitor`: Alternative evaluations and vendor benchmark mentions.
* **Offline Fallback Resilience:** When `HINDSIGHT_API_KEY` is unset or mocked, the client automatically defaults to an internal thread-safe in-memory store without failing or interrupting agent execution.

### 2. Multi-Vector Intelligence Modules (`src/analytics/`)

#### A. Relationship Intelligence & Account Health Score (`relationship.py`)
Computes an empirical **Account Health Score** ($S \in [0, 100]$) using stakeholder role topology, sentiment balance, and interaction velocity:

$$\text{Health Score} = 100 - P_{\text{latency}} - P_{\text{coverage}} + B_{\text{sentiment}}$$

* **Velocity Penalty ($P_{\text{latency}}$):**
  * $> 14$ days since last contact: $-30.0$
  * $> 7$ days since last contact: $-15.0$
* **Stakeholder Coverage Penalty ($P_{\text{coverage}}$):**
  * No Economic Buyer mapped: $-20.0$
  * No designated internal Champion: $-25.0$
  * Blocker Presence: $-15.0 \times N_{\text{blockers}}$
* **Sentiment Modifier ($B_{\text{sentiment}}$):**
  * $+(5.0 \times N_{\text{positive}}) - (10.0 \times N_{\text{negative}})$
* **Status Classification:** `Healthy` ($\ge 75$), `At Risk` ($50 - 74$), `Critical` ($< 50$).

#### B. Predictive Win-Loss Reasoning (`win_loss.py`)
Calculates stage-specific probabilistic win outcomes adjusted for deal stagnation and qualification gaps:
* **Base Stage Probabilities:** Qualification (0.20), Discovery (0.35), Proposal (0.55), Negotiation (0.75), Closed Won (1.00).
* **Decay Factors:**
  * **Stage Dwell Stagnation:** $> 30$ days in stage docks $-15\%$.
  * **Unconfirmed Budget:** $-20\%$.
  * **Unengaged Economic Buyer:** $-15\%$.
  * **Absent Champion:** $-15\%$.
  * **Active Blocker:** $-10\%$.
* **Prescriptive Next-Best-Action (NBA) Engine:** Dynamically generates prioritized mitigation tasks:
  * *Budget Risk:* "Schedule ROI & Business Case review with CFO / Economic Buyer."
  * *Buyer Gap:* "Request Executive Briefing call to engage Economic Buyer."
  * *Champion Gap:* "Identify technical lead to nurture into internal Champion."

#### C. Real-Time Competitive Intelligence (`competitive.py`)
Scans unstructured text for competitor signals (**Salesforce Sales Cloud**, **HubSpot Sales Hub**, **Gong.io**), generates pipeline density matrices, and triggers targeted objection battlecards:
* *Salesforce Counter:* Highlights 2-week time-to-value vs. 6-month deployment and flat transparent pricing.
* *HubSpot Counter:* Contrasts deep multi-session memory retention with surface-level CRM copilot limits.
* *Gong Counter:* Contrasts autonomous proactive execution (calendar + email) with passive conversation recording.

#### D. Cross-Deal Analytics (`cross_deal.py`)
Aggregates interactions across the sales floor to cluster recurring friction points (ERP latency, GDPR/compliance, seat-based pricing reluctance) and automatically feeds lost-deal postmortems into engineering product gap backlogs.

---

### 3. Model Context Protocol (MCP) & Google Workspace Tools (`src/mcp/`)

DIA implements standardized MCP tool definitions that expose typed schemas for Google Workspace and database persistence:

#### Tool Schemas

```json
[
  {
    "name": "google_calendar_schedule",
    "description": "Schedule a Google Calendar meeting with Google Meet video link.",
    "parameters": {
      "type": "object",
      "properties": {
        "summary": { "type": "string" },
        "description": { "type": "string" },
        "start_time": { "type": "string" },
        "end_time": { "type": "string" },
        "attendees": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["summary", "description", "start_time", "end_time", "attendees"]
    }
  },
  {
    "name": "gmail_create_draft",
    "description": "Create an RFC 2822 formatted follow-up email draft in Gmail.",
    "parameters": {
      "type": "object",
      "properties": {
        "to_email": { "type": "string" },
        "subject": { "type": "string" },
        "body_html": { "type": "string" }
      },
      "required": ["to_email", "subject", "body_html"]
    }
  },
  {
    "name": "neon_persist_deal_record",
    "description": "Persists structured deal state and interaction log into Neon DB.",
    "parameters": {
      "type": "object",
      "properties": {
        "account_id": { "type": "string" },
        "opportunity_id": { "type": "string" },
        "deal_data": { "type": "object" }
      },
      "required": ["account_id", "opportunity_id", "deal_data"]
    }
  }
]
```

#### Example Staged Payloads

* **`gmail_create_draft`:**
  ```json
  {
    "to_email": "buyer@acmecorporation.com",
    "subject": "Follow-up & Executive Summary - Acme Corporation",
    "body_html": "<p>Thank you for our discussion regarding Acme Corporation's Proposal stage ($185,000 ARR)...</p>"
  }
  ```
* **`google_calendar_schedule`:**
  ```json
  {
    "summary": "Executive Alignment Call - Acme Corporation",
    "description": "Next Best Action: Draft customized proposal and schedule closing review meeting.",
    "start_time": "2025-03-15T10:00:00Z",
    "end_time": "2025-03-15T10:30:00Z",
    "attendees": ["ae@company.com", "buyer@acmecorporation.com"]
  }
  ```

---

### 4. Programmatic Dossier Engine (`src/narrative/`)

The reporting engine uses **ReportLab Platypus** to compile publication-ready Deal Dossiers:
* **Typography & Palette:** Enterprise styling using deep navy (`#1a365d`), slate blue (`#2b6cb0`), and neutral backgrounds (`#f7fafc`).
* **Financial Snapshot Table:** Formats ARR, win probability, deal stage, and top risk vectors into a styled summary grid.
* **Document Flowables:** Renders multi-paragraph executive summaries, bulleted Next-Best-Actions, and stakeholder health tables into a single high-resolution PDF (`acme_corp_deal_dossier.pdf`).
* **Google Docs API Compatibility:** Provides structured JSON payloads compatible with `docs.documents.batchUpdate` for teams collaborating in Google Workspace.

---

## 📊 Evaluation Matrix & Competitive Differentiation

| Capability | Traditional CRM Plugins (Salesforce / HubSpot Copilots) | Conversational Recording Tools (Gong / Chorus) | Deal Intelligence Agent (DIA) |
| :--- | :--- | :--- | :--- |
| **Cognitive Memory** | Stateless single-turn prompt context | Audio indexing & keyword search | **Longitudinal multi-session persistent retention (Hindsight SDK)** |
| **Cross-Session Recall** | None (wipes when chat closes) | None (manual search across recordings) | **Autonomous multi-hop semantic recall by account namespace** |
| **Action Execution** | Limited to CRM record edits | None (purely passive recording) | **Standardized MCP tool invocation (Calendar, Gmail, Neon DB)** |
| **Safety Model** | Hallucination risks / automated spam | Informational only | **Human-in-the-Loop staging (Gmail drafts staged, never blindly fired)** |
| **Database Architecture** | Proprietary CRM silo | Vendor cloud storage | **Serverless PostgreSQL (Neon) with full relational audit trail** |
| **Executive Artifacts** | Standard dashboard widgets | Snippet links | **High-resolution programmatic PDF Deal Dossiers & Google Docs export** |

---

## ⚙️ Configuration & Environment Variables

DIA features seamless zero-configuration fallbacks: all services run out of the box with built-in mock handlers if credentials are not supplied.

| Variable | Description | Required? | Default / Fallback Mode |
| :--- | :--- | :--- | :--- |
| `HINDSIGHT_API_KEY` | Vectorize Hindsight API Key for cloud memory | Optional | Uses thread-safe local in-memory fallback store |
| `HINDSIGHT_BASE_URL` | Hindsight endpoint URL | Optional | `https://api.hindsight.vectorize.io` |
| `NEON_DATABASE_URL` | Neon Serverless PostgreSQL connection string | Optional | `postgresql://user:pass@ep-mock-neon...` (in-memory fallback) |
| `GOOGLE_CLIENT_ID` | Google Cloud OAuth Client ID for Workspace APIs | Optional | Mock OAuth credential provider |
| `GOOGLE_CLIENT_SECRET`| Google Cloud OAuth Client Secret | Optional | Mock OAuth credential provider |
| `GOOGLE_REFRESH_TOKEN`| OAuth 2.0 Refresh Token for Calendar/Gmail | Optional | Staged mock service provider |
| `GROQ_API_KEY` | Groq API Key for high-speed LLM inference | Optional | Local rule-based pitch and diagnostic synthesizer |
| `LLM_MODEL` | Large language model identifier | Optional | `qwen/qwen3-32b` |

---

## 🛠 Step-by-Step Reproduction Guide

Follow these exact steps to set up, test, and run the Deal Intelligence Agent on an Ubuntu/Debian Linux system.

### 1. Install System Dependencies
Ensure C build tooling and PostgreSQL development headers are present:
```bash
sudo apt update && sudo apt install -y python3-dev libpq-dev build-essential
```

### 2. Set Up Virtual Environment
```bash
# Clone the repository
git clone https://github.com/Manibhushanamk/deal-intelligence-agent.git
cd deal-intelligence-agent

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Package in Editable Mode
```bash
pip install -e .
```

### 4. Execute Unit Test Suite
Run `pytest` to execute all unit test suites across memory, intelligence, and workspace tools:
```bash
pytest tests/ -v
```

**Expected Test Output:**
```text
============================= test session starts ==============================
platform linux -- Python 3.14.x, pytest-9.x, pluggy-1.x
rootdir: /home/.../deal-intelligence-agent
configfile: pyproject.toml
plugins: asyncio-1.4.0, anyio-4.15.1

tests/test_hindsight_memory.py::test_hindsight_retain_and_recall PASSED  [ 11%]
tests/test_hindsight_memory.py::test_hindsight_fact_extraction PASSED    [ 22%]
tests/test_intelligence_modules.py::test_cross_deal_analytics PASSED     [ 33%]
tests/test_intelligence_modules.py::test_relationship_intelligence PASSED [ 44%]
tests/test_intelligence_modules.py::test_competitive_intelligence PASSED [ 55%]
tests/test_intelligence_modules.py::test_win_loss_reasoning PASSED       [ 66%]
tests/test_workspace_actions.py::test_calendar_service PASSED            [ 77%]
tests/test_workspace_actions.py::test_gmail_service PASSED               [ 88%]
tests/test_workspace_actions.py::test_mcp_server_workspace_tools PASSED  [100%]

============================== 9 passed in 0.61s ===============================
```

### 5. Run the End-to-End Enterprise Demo
Execute the full enterprise sales scenario simulation:
```bash
python3 demo.py
```

**Expected Terminal Output:**
```text
================================================================================
      DEAL INTELLIGENCE AGENT (DIA) - ENTERPRISE DEMO RUNNER
================================================================================

[1] Processing Deal State for Account: Acme Corporation ($185,000.00 ARR)
    - Current Stage: Proposal
    - Total Interactions Ingested: 3
    - Total Stakeholders Mapped: 3

================================================================================
                        DIA ANALYTICS & INSIGHTS
================================================================================

▶ Account Health Score: 100.0/100 (Healthy)
▶ Computed Win Probability: 55%
▶ Causal Risk Vectors:
▶ Prescriptive Next-Best-Actions (NBA):
    ✔ Draft customized proposal and schedule closing review meeting.
▶ Identified Competitor Mentions: Salesforce, Gong

================================================================================
                   STAGED WORKSPACE MCP ACTIONS
================================================================================

[MCP Action #1] Tool: gmail_create_draft
    - Gmail Draft ID: draft_5001
    - Recipient: buyer@acmecorporation.com
    - Subject: Follow-up & Executive Summary - Acme Corporation

[MCP Action #2] Tool: google_calendar_schedule
    - Meeting Event ID: evt_1001
    - Summary: Executive Alignment Call - Acme Corporation
    - Google Meet Link: https://meet.google.com/dia-evt_1001

================================================================================
                 PROGRAMMATIC PDF DOSSIER GENERATION
================================================================================

 Successfully generated Deal Dossier PDF: .../deal-intelligence-agent/acme_corp_deal_dossier.pdf
================================================================================
```

### 6. Verify Generated Artifact
Inspect the generated PDF Deal Dossier:
```bash
ls -lh acme_corp_deal_dossier.pdf
```

---

## 🏆 Hackathon Submission Details

* **Event:** HackwithHyderabad 3.0 / Hindsight AI Agents Hackathon
* **Track:** Cognitive Agents, Enterprise Productivity & Persistent Memory
* **Repository:** [https://github.com/Manibhushanamk/deal-intelligence-agent](https://github.com/Manibhushanamk/deal-intelligence-agent)
* **Core Technologies:** Hindsight Memory SDK, Neon Serverless PostgreSQL, Model Context Protocol (MCP), ReportLab, Google Workspace APIs, Pydantic, SQLAlchemy.
* **License:** [MIT License](LICENSE)
