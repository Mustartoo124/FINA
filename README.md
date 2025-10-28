# 💰 FINA MULTI-AGENT SYSTEM

**FINA MULTI-AGENT SYSTEM** is a **Multi-Agent AI Architecture** designed to manage personal finance intelligently — from secure prompt filtering to investment analysis, tax assistance, financial planning, and visualization.

The system is built using **Google Cloud ADK**, **Vertex AI RAG**, **LangChain**, **CrewAI**, **PostgreSQL (Supabase)**, and **Python-based financial APIs** (Vnstock & CoinMarketCap).  

---

## 🧠 System Overview

This project implements a **multi-agent workflow** for personal finance management.  
Each agent is specialized for a unique responsibility — from securing the system against prompt injections to analyzing, planning, investing, and visualizing user financial data.

### 🧩 Agent Workflow

1. **🛡️ Defend Agent**  
   - Detects and blocks **malicious prompts (prompt injection attacks)** using a fine-tuned **DeBERTa-v3-base** model on the **Malicious Prompt Detection Dataset (MPDD)**.  
   - If safe → forwards query to **User Context Agent**.

2. **🧾 User Context Agent**  
   - Extracts user **intent** and **query**.  
   - Stores context in memory (state).  
   - Routes to **Database Agent** for execution.

3. **💾 Database Agent**  
   - Handles CRUD operations on **Supabase PostgreSQL** tables. 
   - Analyzes user transactions and spending habits.  
   - Generates structured financial insights (balance, categories, frequency, anomalies).  
   - For non-CRUD intents, routes to specialized sub-agents:  
     - `TaxAgent`  
     - `InvestAgent`  
     - `PlannerAgent`  
     - `VisualizeAgent`  
     - `ResearchAgent`

4. **💹 Invest Agent**  
   - Fetches **real-time stock and crypto data**.  
   - Recommends investment opportunities based on user’s financial data.  
   - **APIs used:**  
     - [CoinMarketCap API](https://coinmarketcap.com/api/documentation/v1/#section/Introduction)  
     - [Vnstock API](https://pypi.org/project/vnstock/)

5. **📆 Planner Agent**  
   - Uses AI reasoning to design **personalized financial plans**.  
   - Suggests saving goals and expense allocations.

6. **💸 Tax Agent**  
   - Answers tax-related questions using **Vertex AI RAG** and **Google Cloud Storage** datasets.  
   - Retrieves relevant tax information based on user profile and transaction data.

7. **🔍 Research Agent**  
   - Fetches **real-time financial information** using:  
     - `LangChain Wikipedia tool`  
     - `CrewAI ScrapeWebsiteTool`  
   - Keeps the system updated with latest market and finance news.

8. **📈 Visualize Agent**  
   - Converts financial data into **graphs and dashboards** using `matplotlib`.  
   - Saves visualizations to **Google Cloud Storage**.  
   - Provides shareable URLs for users to access their financial visualizations.

---

## ⚙️ Core Features

- 🧠 **Intent-based Multi-Agent Workflow** — Modular agents handle specific reasoning paths.  
- 🛡️ **Prompt Safety Filter** — Prevents prompt injection using fine-tuned models.  
- 💾 **Supabase PostgreSQL Integration** — Secure and structured financial data storage.  
- 📊 **Data Analysis Layer** — Extracts insights from user transactions.  
- 💹 **Investment Recommendation Engine** — Uses real-time market data.  
- 🧾 **Tax Question Answering (RAG)** — Integrated with Vertex AI.  
- 📈 **Visualization Tools** — Generates financial charts stored on the cloud.  
- 🌐 **Web Knowledge Integration** — Uses Wikipedia and web scraping for financial research.

---

## 📂 Project Structure
```bash
FINA/
│
├── assets/
├── client/
├── fina/
│   ├── schemas/
│   │   ├── __init__.py
│   │
│   ├── sub_agents/
│   │   ├── database_agent/
│   │   ├── defend_agent/
│   │   ├── invest_agent/
│   │   ├── planner_agent/
│   │   ├── research_agent/
│   │   ├── tax_agent/
│   │   ├── user_context_agent/
│   │   ├── visualize_agent/
│   │   └── __init__.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── analysis.py
│   │   ├── callback_logging.py
│   │   ├── database.py
│   │   ├── defend_tools.py
│   │   ├── financial_tools.py
│   │   ├── investment_tools.py
│   │   ├── rag_query.py
│   │   ├── utils.py
│   │   └── visualize_tools.py
│   │
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   └── .env
│
└── README.md
```

## 🚀 Installation & Setup
- Clone the Repository 

```bash
git clone https://github.com/Mustartoo124/FINA.git
cd FINA
```

- Create a Virtual Environment

```bash
python -m venv .venv

# Activate the environment
.venv\Scripts\activate #Window

source .venv/bin/activate  #macOS/Linux

.venv\Scripts\Activate.ps1 #Window Powershell
```

- Install Dependencies
```bash
pip install -r requirements.txt
```

### Google Cloud Setup
- Step 1: Create and Configure a Google Cloud Project: 
    - Follow the quickstart guide: [Quickstart](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=adc#configure-project)

    - Enable Vertex AI API: [enable Vertex AI API](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com)

- Step 2: Set up Google Cloud CLI
    - Install and configure gcloud locally:
    [gcloud](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=adc#setup-local)
    - Authenticate to Google Cloud: 
    ```bash
    gcloud auth application-default login
    ```

- Step 3: Configure Environment Variables
    - Create a .env file in the project root: 
    ```bash
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
    GOOGLE_CLOUD_LOCATION=YOUR_LOCATION
    MODEL=YOUR_LLM_MODEL
    SUPABASE_URL=YOUR_SUPABASE_URL 
    SUPABASE_KEY=YOUR_SUPABASE_KEY
    COINMARKETCAP_API_KEY=YOUR_COINMARKETCAP_KEY
    ```
## Run the Agent System
```bash
gcloud auth application-default login
adk web
```