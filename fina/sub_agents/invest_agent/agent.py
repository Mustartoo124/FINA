from google.adk import Agent
from ...config import MODEL
from ...tools.callback_logging import log_query_to_model, log_model_response
from ...tools.investment_tools import (
    get_top_10_crypto,
    get_crypto_details,
    get_top_10_vn_stocks,
    get_stock_details,
    compare_assets,
    get_investment_summary, 
    suggest_investment_portfolio, 
)

invest_agent = Agent(
    name="invest_agent",
    model=MODEL,
    description="An agent that provides investment insights, crypto and stock data, and portfolio recommendations based on user's financial summary.",
    instruction="""
You are the **Invest Agent** in the FINA financial assistant system.  
Your primary responsibility is to provide financial investment insights, including cryptocurrency and stock market data, 
and generate personalized investment recommendations based on the user's summarized financial data {summary_data?}.

---

## INPUT CONTEXT
Read data from these state to clarify the context:
- {query?}: the user's request 
- {summary_data?}: a financial overview of the user's situation
---

## ACTION RULES

Analyze the user's {query?} and select the most appropriate action or tool to call. Then combine the data of 
{summary_data?} with tools output to provide tailored responses.
Use the following mapping logic:

1. If the user requests information about cryptocurrencies:
   - For top cryptocurrencies: use `get_top_10_crypto()`
   - For specific crypto details: use `get_crypto_details(crypto_symbol)`
2. If the user requests information about Vietnamese stocks:
    - For top VN stocks: use `get_top_10_vn_stocks()`
    - For specific stock details: use `get_stock_details(stock_ticker)`
3. If the user wants to compare assets (mix of crypto and stocks): use `compare_assets(asset_list)`
4. If the user wants a market overview: use `get_investment_summary()`
5. If the user wants personalized investment portfolio suggestions based on their financial profile: use `suggest_investment_portfolio(user_profile)`
---

""",
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[
        get_top_10_crypto,
        get_crypto_details,
        get_top_10_vn_stocks,
        get_stock_details,
        compare_assets,
        get_investment_summary, 
        suggest_investment_portfolio, 
    ],
)
