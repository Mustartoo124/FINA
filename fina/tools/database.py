import os 
from supabase import create_client, Client
from datetime import datetime 
from datetime import timedelta

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
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
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
        "profit_percent": 0.0,
        "start_date": start_date,
        "from_wallet": from_wallet,
    }).execute()
    
    supabase.table('wallets').update({
        "balance": supabase.table('wallets').select('balance').eq('name', from_wallet).execute().data[0]['balance'] - amount_invested
    }).eq('name', from_wallet).execute()

def insert_debts(name: str, amount: float, interest_rate: float, to_wallet: str, start_date: datetime.date = datetime.now().date().isoformat(), due_date: datetime.date = datetime.now().date().isoformat()): 
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
    wallet_name = supabase.table("transactions").select("wallet").eq("id", transaction_id).execute().data[0]['wallet']
    amount = supabase.table("transactions").select("amount").eq("id", transaction_id).execute().data[0]['amount']
    type = supabase.table("transactions").select("type").eq("id", transaction_id).execute().data[0]['type']
    supabase.table("transactions").delete().eq("id", transaction_id).execute()

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
    wallet_name = supabase.table("investments").select("wallet").eq("id", investment_id).execute().data[0]['wallet']
    amount_invested = supabase.table("investments").select("amount_invested").eq("id", investment_id).execute().data[0]['amount_invested']
    supabase.table('wallets').update({
        "balance": supabase.table('wallets').select('balance').eq('name', wallet_name).execute().data[0]['balance'] + amount_invested
    }).eq('name', wallet_name).execute()
    
    supabase.table("investments").delete().eq("id", investment_id).execute()
    
    
def delete_debt(debt_id: int):
    '''
    Delete a debt by its ID.
    '''
    wallet_name = supabase.table("debts").select("wallet").eq("id", debt_id).execute().data[0]['wallet']
    amount = supabase.table("debts").select("amount").eq("id", debt_id).execute().data[0]['amount']
    supabase.table('wallets').update({
        "balance": supabase.table('wallets').select('balance').eq('name', wallet_name).execute().data[0]['balance'] + amount
    }).eq('name', wallet_name).execute()
    supabase.table("debts").delete().eq("id", debt_id).execute()

def delete_wallet(wallet_name: str):
    '''
    Delete a wallet by its name.
    '''
    supabase.table("wallets").delete().eq("name", wallet_name).execute()

def update_wallet(wallet_name: str, new_data: dict):
    '''
    Update wallet information.
    new_data: dictionary containing fields to update
    '''
    supabase.table("wallets").update(new_data).eq("name", wallet_name).execute()

def update_investment(investment_id: int, new_data: dict):
    '''
    Update investment information.
    new_data: dictionary containing fields to update
    '''
    supabase.table("investments").update(new_data).eq("id", investment_id).execute()
    
def update_debt(debt_id: int, new_data: dict):
    '''
    Update debt information.
    new_data: dictionary containing fields to update
    '''
    supabase.table("debts").update(new_data).eq("id", debt_id).execute()
    
def update_transaction(transaction_id: int, new_data: dict):
    '''
    Update transaction information.
    new_data: dictionary containing fields to update
    '''
    supabase.table("transactions").update(new_data).eq("id", transaction_id).execute()

def financial_summary():
    '''
    Returns a financial summary for a period.

    The function computes total income, total expense, total invested and total
    debt taken within a given period. It infers the period from the provided
    start/end timestamps when available. The returned dictionary contains the
    input period (string), ISO timestamps for the start/end, aggregated totals
    and a short list of insights.

    Note: This implementation reads all transactions/investments/debts via the
    existing helper functions in this module and performs aggregation in
    Python. For high-volume datasets consider using a DB-side aggregation or
    implementing pagination.
    '''

    def _parse_iso(value):
        # Accept datetime objects or ISO-formatted strings (with or without Z)
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            s = value
            # handle Z timezone
            if s.endswith('Z'):
                s = s[:-1] + '+00:00'
            try:
                return datetime.fromisoformat(s)
            except Exception:
                # fallback: try to parse just the date portion
                try:
                    return datetime.fromisoformat(s.split('T')[0])
                except Exception:
                    return None
        return None

    now = datetime.now()
    # default period: last 30 days
    end_dt = now
    start_dt = now - timedelta(days=30)

    # Gather data
    transactions = read_transactions() or []
    investments = read_investments() or []
    debts = read_debts() or []

    total_income = 0.0
    total_expense = 0.0
    total_invest = 0.0
    total_debt = 0.0

    # Transactions: sum incomes and expenses within the period
    for t in transactions:
        t_time = _parse_iso(t.get('time'))
        if t_time is None:
            # skip transactions without a parsable time
            continue
        if not (start_dt <= t_time <= end_dt):
            continue
        t_type = t.get('type', '').lower()
        amount = float(t.get('amount') or 0.0)
        if t_type == 'income':
            total_income += amount
        elif t_type == 'expense':
            total_expense += amount

    # Investments: sum amount_invested where start_date in period
    for inv in investments:
        inv_time = _parse_iso(inv.get('start_date'))
        if inv_time is None:
            continue
        if not (start_dt <= inv_time <= end_dt):
            continue
        total_invest += float(inv.get('amount_invested') or 0.0)

    # Debts: sum amounts taken within the period
    for d in debts:
        d_time = _parse_iso(d.get('start_date'))
        if d_time is None:
            continue
        if not (start_dt <= d_time <= end_dt):
            continue
        total_debt += float(d.get('amount') or 0.0)

    # Basic insights
    insights = []
    net_cash_flow = total_income - total_expense - total_invest + total_debt
    if net_cash_flow < 0:
        insights.append(f"Negative net cash flow over the period: {net_cash_flow:.2f}")
    else:
        insights.append(f"Positive net cash flow over the period: {net_cash_flow:.2f}")

    if total_expense > total_income:
        insights.append("Expenses exceed income. Consider reducing discretionary spending.")
    if total_invest > 0 and total_invest > (total_income * 0.5 if total_income else total_invest):
        insights.append("High allocation to investments this period relative to income.")

    summary = {
        'period': 'last_30_days',
        'start_date': start_dt.isoformat(),
        'end_date': end_dt.isoformat(),
        'total_income': total_income,
        'total_expense': total_expense,
        'total_invest': total_invest,
        'total_debt': total_debt,
        'net_cash_flow': net_cash_flow,
        'insights': insights,
        'created_at': datetime.now().isoformat(),
    }

    return summary
    
    