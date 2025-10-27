from google.adk import Agent
from ...config import MODEL

from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.utils import append_to_state
from ...tools.rag_query import rag_query

tax_agent = Agent(
    name="tax_agent",
    model=MODEL,
    description="An agent that provides tax-related information and assistance based on user's financial data.",
    instruction="""
    You are the **Tax Agent** in the FINA financial assistant system.
    Based on the {query?}, you should retrieve the appropriate information from corpora using the 'rag_query' tool.
    `rag_query`: Query a corpus to answer questions
       - Parameters:
         - corpus_name: The name of the corpus to query (required, but can be empty to use current corpus)
         - query: The text question to ask 
    Then, you should use the 'append_to_state' tool to store the retrieved information into the 'context' state.
    Combine the user's {query?} with the retrieved context to provide accurate and relevant tax information or calculations.
    Always ensure that your responses are compliant with current tax regulations and guidelines.
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[
        rag_query,
        append_to_state,
    ],
)