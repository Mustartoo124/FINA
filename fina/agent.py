from google.adk import Agent
from google.adk.agents import SequentialAgent
from .config import MODEL

from .tools.callback_logging import log_query_to_model, log_model_response

from .sub_agents.database_agent.agent import database_agent
from .sub_agents.user_context_agent import user_context_agent

main_flow = SequentialAgent(
    name="main_flow",
    agents=[
        user_context_agent,
        database_agent,
    ],
)

root_agent = Agent(
    name="root_agent",
    model=MODEL,
    description="The root agent that manages user context and routes tasks to specialized sub-agents in the FINA financial assistant system.",
    
    instruction="""
    You are the **Root Agent** in the FINA financial assistant system.
    Your primary responsibility is to manage the overall user context and delegate tasks to specialized sub-agents based on the user's requests.
    Use the **main flow** sequential agent to handle the user's queries by first updating the user context and then performing database operations as needed.
    """, 
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    sub_agents=[
        main_flow,
    ],
)