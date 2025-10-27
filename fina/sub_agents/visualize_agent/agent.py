from google.adk import Agent
from ...config import MODEL
from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.visualize_tools import (
    visualize_transactions,
)

visualize_agent = Agent(
    name="visualize_agent",
    model=MODEL,
    description="An agent that creates visualizations of the user's financial data to aid in understanding andanalysis.",
    instruction="""
    Use the 'visualize_transactions' tool to create visualizations of financial transactions.
    'visualize_transactions': Generate visual representations of financial transactions
    - Parameters:
      - period: The time period for the transactions to visualize (e.g., last month, last year)
      - wallet: (optional) The specific wallet to focus on
    
    The function return this {'fig_url': None, 'error': str(e), 'figure': fig} so you should show 
    the figure to the user by showing the fig_url to the user. 
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,                            
    tools=[
        visualize_transactions,
    ],  
)
