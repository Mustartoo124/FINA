from fina.tools import database
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# database.insert_wallet(name="Test Wallet", type="cash", balance=1000.0)
# database.insert_investment(asset_name="Test Investment", type="stocks", amount_invested=500.0, from_wallet="Test Wallet")
# database.insert_debts(name="Test Debt", amount=200.0, interest_rate=5.0, to_wallet="Test Wallet")
# database.insert_transaction(wallet="Test Wallet", amount=150.0, category="expense")
wallets = database.read_wallets()
investments = database.read_investments()
debts = database.read_debts()
transactions = database.read_transactions()

print("Wallets:", wallets)
print("Investments:", investments)
print("Debts:", debts)
print("Transactions:", transactions)
