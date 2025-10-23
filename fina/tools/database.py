import os 
from supabase import create_client, Client
from datetime import datetime 

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def insert_wallet(name: str, type: str, balance: float = 0.0): 
    '''
    id: auto increment primary key
    name: wallet name
    type: wallet type (e.g., cash, bank, e-wallet)
    balance: initial balance
    created_at: timestamp of wallet creation
    updated_at: timestamp of last update
    '''
    supabase.table("wallets").insert({
        "name": name,
        "type": type,
        "balance": balance,
        "created_at": datetime.now().date(),
        "updated_at": datetime.now().date(),
    }).execute()
    

def insert_investment(asset_name: str, type: str, amount_invested: float, from_wallet: str, start_date: datetime = datetime.now().isoformat()): 
    '''
    id: auto increment primary key
    asset_name: name of the asset
    type: type of investment (e.g., stock, crypto)
    amount_invested: amount of money invested
    current_value: current value of the investment
    profit: profit or loss from the investment
    profit_percentage: profit or loss percentage
    start_date: date when the investment was made
    from_wallet: wallet from which the investment was made
    '''
    supabase.table("investments").insert({
        "asset_name": asset_name,
        "type": type,
        "amount_invested": amount_invested,
        "current_value": amount_invested,
        "profit": 0.0,
        "profit_percentage": 0.0,
        "start_date": start_date,
        "from_wallet": from_wallet,
    }).execute()
    
    supabase.table('wallets').update({
        "balance": supabase.table('wallets').select('balance').eq('name', from_wallet).execute().data[0]['balance'] - amount_invested
    }).eq('name', from_wallet).execute()

def insert_debts(name: str, amount: float, interest_rate: float, to_wallet: str, start_date: datetime.date = datetime.now().date(), due_date: datetime.date = datetime.now().date()): 
    '''
    id: auto increment primary key
    name: name of the debtor
    amount: amount owed
    interest_rate: interest rate of the debt
    start_date: date when the debt was taken
    due_date: date when the debt is due
    to_wallet: wallet to which the debt is owed
    '''
    supabase.table("debts").insert({
        "name": name,
        "amount": amount,
        "interest_rate": interest_rate,
        "start_date": start_date,
        "due_date": due_date,
        "to_wallet": to_wallet,
    }).execute()

    supabase.table('wallets').update({
        "balance": supabase.table('wallets').select('balance').eq('name', to_wallet).execute().data[0]['balance'] + amount
    }).eq('name', to_wallet).execute()

def insert_transaction(wallet: str, amount: float, category: str = "None", type: str = "expense",  description: str = "None", time: datetime = datetime.now().isoformat()): 
    '''
    id: auto increment primary key
    wallet: wallet name
    category: transaction category
    type: income or expense or invest or debt
    amount: amount of money
    description: text description
    time: transaction time
    '''
    supabase.table("transactions").insert({
        "wallet": wallet,   
        "category": category,
        "type": type,
        "amount": amount,
        "description": description,
        "time": time, 
    }).execute()

    if (type == "expense"):
        supabase.table('wallets').update({
            "balance": supabase.table('wallets').select('balance').eq('name', wallet).execute().data[0]['balance'] - amount
        }).eq('name', wallet).execute()
    elif (type == "income"):
        supabase.table('wallets').update({
            "balance": supabase.table('wallets').select('balance').eq('name', wallet).execute().data[0]['balance'] + amount
        }).eq('name', wallet).execute()
    elif (type == "invest"):
        pass  # Investment handling is done in insert_investment
    elif (type == "debt"):
        pass  # Debt handling is done in insert_debts

def read_wallets():
    '''
    Read all wallets from the database.
    '''
    response = supabase.table("wallets").select("*").execute()
    return response.data

def read_investments():
    '''
    Read all investments from the database.
    '''
    response = supabase.table("investments").select("*").execute()
    return response.data

def read_debts():
    '''
    Read all debts from the database.
    '''
    response = supabase.table("debts").select("*").execute()
    return response.data

def read_transactions():
    '''
    Read all transactions from the database.
    '''
    response = supabase.table("transactions").select("*").execute()
    return response.data

def delete_transaction(transaction_id: int):
    '''
    Delete a transaction by its ID.
    '''
    supabase.table("transactions").delete().eq("id", transaction_id).execute()
    wallet_name = supabase.table("transactions").select("wallet").eq("id", transaction_id).execute().data[0]['wallet']
    amount = supabase.table("transactions").select("amount").eq("id", transaction_id).execute().data[0]['amount']
    type = supabase.table("transactions").select("type").eq("id", transaction_id).execute().data[0]['type']
    if (type == "expense"):
        supabase.table('wallets').update({
            "balance": supabase.table('wallets').select('balance').eq('name', wallet_name).execute().data[0]['balance'] + amount
        }).eq('name', wallet_name).execute()
    elif (type == "income"):
        supabase.table('wallets').update({
            "balance": supabase.table('wallets').select('balance').eq('name', wallet_name).execute().data[0]['balance'] - amount
        }).eq('name', wallet_name).execute()

def delete_investment(investment_id: int):
    '''
    Delete an investment by its ID.
    '''
    supabase.table("investments").delete().eq("id", investment_id).execute()
    wallet_name = supabase.table("investments").select("wallet").eq("id", investment_id).execute().data[0]['wallet']
    amount_invested = supabase.table("investments").select("amount_invested").eq("id", investment_id).execute().data[0]['amount_invested']
    supabase.table('wallets').update({
        "balance": supabase.table('wallets').select('balance').eq('name', wallet_name).execute().data[0]['balance'] + amount_invested
    }).eq('name', wallet_name).execute()
    
def delete_debt(debt_id: int):
    '''
    Delete a debt by its ID.
    '''
    supabase.table("debts").delete().eq("id", debt_id).execute()
    wallet_name = supabase.table("debts").select("wallet").eq("id", debt_id).execute().data[0]['wallet']
    amount = supabase.table("debts").select("amount").eq("id", debt_id).execute().data[0]['amount']
    supabase.table('wallets').update({
        "balance": supabase.table('wallets').select('balance').eq('name', wallet_name).execute().data[0]['balance'] + amount
    }).eq('name', wallet_name).execute()

def update_wallet_balance(wallet_name: str, new_balance: float):
    '''
    Update the balance of a wallet.
    '''
    supabase.table("wallets").update({
        "balance": new_balance,
        "updated_at": datetime.now().date(),
    }).eq("name", wallet_name).execute()
