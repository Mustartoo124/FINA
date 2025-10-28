from google.adk import Agent
from ...config import MODEL
from ...tools.callback_logging import log_query_to_model, log_model_response

from ...tools.defend_tools import (
    classify_prompt_safety, 
)

defend_agent = Agent(
    name="defend_agent",
    model=MODEL,
    description="An agent responsible for classifying user prompts for safety and policy compliance in the FINA system.",
    instruction="""
You are the Defend Agent in the FINA financial assistant system. Use {query?} as the user prompt input.
Using the `classify_prompt_safety` tool to determine if the user prompt is safe and compliant with policy:
   - Parameter: 
        - text: the user prompt to classify.
If the function return `0`, the prompt is malicious (policy-violating). Then stop the process and inform the user that their prompt violates the policy.
If the function return `1`, the prompt is benign. Then proceed to pass the prompt to the main agent for further processing.
""", 
    tools=[classify_prompt_safety],
)