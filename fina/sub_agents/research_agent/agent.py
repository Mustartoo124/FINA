import os

from ...tools.callback_logging import log_query_to_model, log_model_response

from google.genai import types
from google.adk import Agent
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.crewai_tool import CrewaiTool
from crewai_tools import ScrapeWebsiteTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


research_agent = Agent(
    name="crewai_tool_agent",
    model=os.getenv("MODEL"),
    description="An agent that uses CrewAI tools to perform web scraping tasks.",
    instruction="Use the available tools to get the information needed and combine it to answer the user's {query?}.",
    generate_content_config=types.GenerateContentConfig(
        temperature=0
    ),
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,    
    tools = [
        CrewaiTool(
            name="scrape_apnews",
            description=(
                """Scrapes the latest news content about financial from
                the Associated Press (AP) News website."""
            ),
            tool=ScrapeWebsiteTool("https://apnews.com/")
        ),
        LangchainTool(
            tool=WikipediaQueryRun(
                api_wrapper=WikipediaAPIWrapper()
            )
        )
    ]

)