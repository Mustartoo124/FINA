# FINA

**FINA** is a **Multi-Agent AI System** designed to simulate a virtual teacher that helps students learn through intelligent document retrieval and dynamic internet-based reasoning.  
The system is built using **Google Cloud’s Agent Development Kit (ADK)**, **Vertex AI RAG Engine**, and **LangGraph/LangChain/CrewAI** integration.

---

## 🧠 Overview

This project introduces a multi-agent framework for learning assistance.  
Each agent in the system plays a specialized role — from understanding the user’s query to retrieving, summarizing, and generating responses based on contextually relevant data.

The system combines:
- **RAG (Retrieval-Augmented Generation)** via Vertex AI  
- **LangGraph** and **LangChain** for workflow orchestration  
- **CrewAI** tools for internet retrieval and multi-agent collaboration  
- **Google Cloud ADK** for managing agents and deployment  

![System Overview](assets/overview.png)
---

## ⚙️ Core Features

- 🧩 **Multi-Agent Design:** Modular and extensible agents specialized for distinct learning tasks.  
- 🔍 **RAG-based Retrieval:** Combines knowledge from uploaded materials and internet sources.  
- 🧑‍🏫 **Context Awareness:** Maintains user learning context through query history.  
- 🧠 **Automated Lesson Summarization:** Generates concise and informative summaries.  
- 🎯 **Quiz Generation:** Builds personalized quizzes based on retrieved lesson data.  
- 🌐 **Web Integration:** Uses real-time internet search for information supplementation.  

---

## 📂 Project Structure
```bash
ADK_RAG_AGENT/
├── rag_agent/
│   ├── schemas/
│   ├── sub_agents/
│   │   ├── answer_agent/
│   │   ├── context_adapter_agent/
│   │   ├── knowledge_router_agent/
│   │   ├── output_adapter_agent/
│   │   ├── quiz_generator_agent/
│   │   ├── summarize_lesson_agent/
│   │   └── user_context_agent/
│   └── __init__.py
│
├── tools/
│   ├── callback_logging.py
│   ├── rag_query.py
│   ├── utils.py
│   └── __init__.py
│
├── agent.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🚀 Installation & Setup
- Clone the Repository 

```bash
git clone https://github.com/Mustartoo124/ADK_RAG_AGENT.git
cd ADK_RAG_AGENT
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
    ```
## Run the Agent System
```bash
gcloud auth application-default login
adk web
```