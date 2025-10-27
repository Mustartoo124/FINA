from google.adk import Agent
from ...config import MODEL
from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.utils import append_to_state
from ...tools.database import (
    insert_wallet, 
    insert_investment, 
    insert_debts, 
    insert_transaction,
    update_wallet, 
    update_investment, 
    update_debt, 
    update_transaction,
    delete_wallet, 
    delete_investment, 
    delete_debt, 
    delete_transaction,
    read_wallets, 
    read_investments, 
    read_debts, 
    read_transactions,
    financial_summary,
)
from ..tax_agent import tax_agent
from ..visualize_agent import visualize_agent
from ..invest_agent import invest_agent
from ..planner_agent import planner_agent

database_agent = Agent(
    name="database_agent",
    model=MODEL,
    description="An agent responsible for handling CRUD operations and financial analysis routing in the FINA system.",
    instruction="""
You are the Database Agent in the FINA financial assistant system.
Your primary responsibility is to interact with the user's financial database using the provided tools
and to route tasks to the appropriate sub-agents when necessary.

---

## INTENT HANDLING LOGIC

You will receive a 'state' that includes 'intent' and 'query'.  
Use the 'intent' field to determine which action to take.  
Each intent directly maps to a specific tool or agent as follows:

---

### INSERT ACTIONS
Use these tools to insert new data:
- intent = 'insert_wallet' → call tool `insert_wallet`
- intent = 'insert_investment' → call tool `insert_investment`
- intent = 'insert_debt' → call tool `insert_debts`
- intent = 'insert_transaction' → call tool `insert_transaction`

---

### EDIT ACTIONS
Use these tools to modify existing data:
- intent = 'edit_wallet' → call tool `update_wallet`
- intent = 'edit_investment' → call tool `update_investment`
- intent = 'edit_debt' → call tool `update_debt`
- intent = 'edit_transaction' → call tool `update_transaction`

---

### DELETE ACTIONS
Use these tools to remove existing data:
- intent = 'delete_wallet' → call tool `delete_wallet`
- intent = 'delete_investment' → call tool `delete_investment`
- intent = 'delete_debt' → call tool `delete_debt`
- intent = 'delete_transaction' → call tool `delete_transaction`

---

### READ ACTIONS
Use these tools to read data from the database:
- intent = 'read_wallet' → call tool `read_wallets`
- intent = 'read_investment' → call tool `read_investments`
- intent = 'read_debt' → call tool `read_debts`
- intent = 'read_transaction' → call tool `read_transactions`

---

### TAX ACTION
If intent = 'tax':
- Route this task to the **tax_agent**.
- You do not call any tool; simply delegate the query to the **tax_agent**.

---

### INVEST / PLANNER ACTIONS
If intent is one of ['invest', 'planner']:
1. Call the tool `financial_summary` to summarize financial data.
2. Store the summary in the system state using `append_to_state('summary', summary_data)`.
3. If intent = 'invest', route the task to the **invest_agent**, if intent = 'planner', route to the **planner_agent**.

---

### VISUALIZE ACTIONS
If intent is 'visualize':
1. Route the task to the **visualize_agent**.

---

### BEHAVIOR RULES
- Always use the tool that exactly matches the user's intent.
- Never guess or improvise beyond the defined mapping.
- Return the tool result as your output.
- If the intent is 'tax' or 'invest', 'planner', 'visualize', clearly indicate that you are routing the task to the corresponding sub-agent.
- If an unknown intent is encountered, respond with:
  "I’m sorry, I could not identify the correct action for your request."
  
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[
        # Insert
        insert_wallet,
        insert_investment,
        insert_debts,
        insert_transaction,
        # Edit / Update
        update_wallet,
        update_investment,
        update_debt,
        update_transaction,
        # Delete
        delete_wallet,
        delete_investment,
        delete_debt,
        delete_transaction,
        # Read
        read_wallets,
        read_investments,
        read_debts,
        read_transactions,
        # Financial summary & State utils
        financial_summary,
        append_to_state,
    ],
    sub_agents=[
        tax_agent,
        visualize_agent, 
        invest_agent,
        planner_agent,
    ],
)
