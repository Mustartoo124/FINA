# investment_tools.py
import requests
from vnstock import Vnstock
import os
import json

COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")


def get_top_10_crypto():
    """
    Fetch top 10 cryptocurrencies by market cap from CoinMarketCap.
    Returns: JSON string with list of crypto info
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }
    params = {"start": 1, "limit": 10, "convert": "USD"}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        top_10_crypto = []
        for item in data.get("data", []):
            crypto_info = {
                "name": item["name"],
                "symbol": item["symbol"],
                "price_usd": round(item["quote"]["USD"]["price"], 2),
                "percent_change_24h": round(item["quote"]["USD"]["percent_change_24h"], 2),
                "market_cap": round(item["quote"]["USD"]["market_cap"], 2)
            }
            top_10_crypto.append(crypto_info)

        return json.dumps(top_10_crypto, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)


def get_crypto_details(symbol: str):
    """
    Fetch detailed data for a specific cryptocurrency by symbol (e.g., BTC, ETH).
    Returns: JSON string with crypto detail info
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }
    params = {"symbol": symbol.upper(), "convert": "USD"}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if "data" in data and symbol.upper() in data["data"]:
            info = data["data"][symbol.upper()]
            return json.dumps({
                "name": info["name"],
                "symbol": info["symbol"],
                "price_usd": round(info["quote"]["USD"]["price"], 2),
                "percent_change_24h": round(info["quote"]["USD"]["percent_change_24h"], 2),
                "market_cap": round(info["quote"]["USD"]["market_cap"], 2),
                "volume_24h": round(info["quote"]["USD"]["volume_24h"], 2),
                "circulating_supply": round(info["circulating_supply"], 2),
                "rank": info["cmc_rank"]
            }, indent=4)
        else:
            return json.dumps({"error": "Symbol not found"}, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

def get_top_10_vn_stocks():
    """
    Fetch top 10 Vietnamese stocks by market cap.
    Returns: JSON string with list of stock info
    """
    try:
        df = Vnstock().stock_top(symbol='VNINDEX', page=0, size=10, sort='marketCap', order='desc')

        top_10_stocks = []
        for _, row in df.iterrows():
            stock_info = {
                "ticker": row["ticker"],
                "price": row["price"],
                "percent_change": row["percentPriceChange"],
                "volume": row["totalMatchVolume"],
                "market_cap": row["marketCap"],
                "industry": row.get("industryName", "N/A")
            }
            top_10_stocks.append(stock_info)

        return json.dumps(top_10_stocks, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)


def get_stock_details(symbol: str):
    """
    Get detailed info of a specific VN stock.
    Returns: JSON string with stock detail info
    """
    try:
        stock = Vnstock().stock(symbol)
        profile = stock.profile()
        quote = stock.quote()

        return json.dumps({
            "ticker": symbol.upper(),
            "company_name": profile.get("companyName", "N/A"),
            "industry": profile.get("industryName", "N/A"),
            "price": quote.get("price", "N/A"),
            "change_percent": quote.get("percentPriceChange", "N/A"),
            "market_cap": profile.get("marketCap", "N/A"),
            "pe_ratio": profile.get("pe", "N/A"),
            "roe": profile.get("roe", "N/A"),
            "eps": profile.get("eps", "N/A")
        }, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

def compare_assets(asset_list: list):
    """
    Compare performance of given assets (mix of crypto symbols and stock tickers).
    Returns: JSON string of asset comparisons
    """
    results = []
    for asset in asset_list:
        try:
            if asset.isalpha() and len(asset) <= 5:
                # Try stock first
                try:
                    stock_data = json.loads(get_stock_details(asset))
                    if "error" not in stock_data:
                        stock_data["type"] = "stock"
                        results.append(stock_data)
                        continue
                except Exception:
                    pass
                # Fallback to crypto
                crypto_data = json.loads(get_crypto_details(asset))
                crypto_data["type"] = "crypto"
                results.append(crypto_data)
        except Exception as e:
            results.append({"asset": asset, "error": str(e)})

    return json.dumps(results, indent=4)


def get_investment_summary():
    """
    Combine top cryptos + top VN stocks into one market summary.
    Returns: JSON string of market overview
    """
    crypto_data = json.loads(get_top_10_crypto())
    stock_data = json.loads(get_top_10_vn_stocks())

    return json.dumps({
        "top_cryptos": crypto_data,
        "top_vn_stocks": stock_data
    }, indent=4)


def suggest_investment_portfolio(user_profile: dict):
    """
    Suggest an investment portfolio based on user's risk tolerance and goals.
    Example input: {"risk": "low", "goal": "long-term"}
    Returns: JSON string with recommended allocation
    """
    risk = user_profile.get("risk", "medium").lower()
    goal = user_profile.get("goal", "balanced").lower()

    if risk == "low":
        allocation = {
            "bonds_or_safe_stocks": 70,
            "blue_chip_vn_stocks": 25,
            "crypto": 5
        }
    elif risk == "high":
        allocation = {
            "growth_stocks": 50,
            "crypto": 40,
            "cash": 10
        }
    else:  # medium
        allocation = {
            "vn_stocks": 50,
            "crypto": 30,
            "cash_or_etf": 20
        }

    return json.dumps({
        "risk_profile": risk,
        "goal": goal,
        "recommended_allocation": allocation
    }, indent=4)
