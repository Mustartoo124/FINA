import os 
from supabase import create_client, Client
from datetime import datetime 
from datetime import timedelta
from fina.tools.database import read_transactions
import pandas as pd

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_transactions_range(period: str = 'month', wallet: str | None = None):
    """
    Return transactions from a given range as a pandas DataFrame with two
    columns: 'time' (datetime) and 'amount' (float).

    period: one of 'week', 'month', 'year' (case-insensitive). Semantics:
      - 'week'  -> last 7 days
      - 'month' -> last 30 days
      - 'year'  -> last 365 days

    wallet: optional wallet name to filter transactions by wallet.

    The function reads transactions via `read_transactions()` and parses the
    'time' field (supports ISO strings with or without trailing 'Z').
    If no transactions match the filter, an empty DataFrame with the two
    columns is returned.
    """
    
    valid = {'week': 7, 'month': 30, 'year': 365}
    p = (period or 'month').lower()
    if p not in valid:
        raise ValueError(f"Invalid period '{period}'. Expected one of: {', '.join(valid.keys())}")

    now = datetime.now()
    start_dt = now - timedelta(days=valid[p])
    end_dt = now

    def _parse_iso_string(value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            s = value
            if s.endswith('Z'):
                s = s[:-1] + '+00:00'
            try:
                return datetime.fromisoformat(s)
            except Exception:
                try:
                    return datetime.fromisoformat(s.split('T')[0])
                except Exception:
                    return None
        return None

    rows = []
    for t in read_transactions() or []:
        if wallet and (t.get('wallet') != wallet):
            continue
        t_time = _parse_iso_string(t.get('time'))
        if t_time is None:
            continue
        if not (start_dt <= t_time <= end_dt):
            continue
        try:
            amount = float(t.get('amount') or 0.0)
        except Exception:
            # skip rows with non-numeric amount
            continue
        rows.append({'time': t_time, 'amount': amount})

    if not rows:
        # return empty dataframe with proper dtypes
        df = pd.DataFrame(columns=['time', 'amount'])
        df['time'] = pd.to_datetime(df['time'])
        df['amount'] = pd.to_numeric(df['amount'])
        return df

    df = pd.DataFrame(rows)
    df['time'] = pd.to_datetime(df['time'])
    df['amount'] = pd.to_numeric(df['amount'])
    df = df.sort_values('time').reset_index(drop=True)
    return df

