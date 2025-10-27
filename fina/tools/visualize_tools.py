import matplotlib.pyplot as plt
from ..tools.analysis import get_transactions_range
from google.cloud import storage 
import io
import os
from datetime import datetime


def visualize_transactions(period: str = 'month', wallet: str | None = None): 
    """
    Generate a visualization of transactions over a specified time period.

    period: one of 'week', 'month', 'year' (case-insensitive). Semantics:
      - 'week'  -> last 7 days
      - 'month' -> last 30 days
      - 'year'  -> last 365 days

    wallet: optional wallet name to filter transactions by wallet.

    Returns: matplotlib Figure object with the transaction plot.
    """
    df = get_transactions_range(period=period, wallet=wallet)

    fig, ax = plt.subplots(figsize=(10, 6))
    if df.empty:
        ax.text(0.5, 0.5, 'No transactions found in the specified range.',
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14)
        ax.set_title('Transactions Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Amount')
        return fig

    ax.plot(df['time'], df['amount'], marker='o', linestyle='-')
    ax.set_title(f'Transactions Over the Last {period.capitalize()}'
                 + (f' for Wallet: {wallet}' if wallet else ''))
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the figure to Google Cloud Storage and return its URL
    try:
        bucket_name = os.environ.get('FIGURES_BUCKET') or os.environ.get('GCS_BUCKET')
        # destination path: figures/{timestamp}.png
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dest_name = f'figures/transactions_{period}_{timestamp}.png'
        fig_url = save_fig_to_gcs(fig, bucket_name=bucket_name, destination_blob_name=dest_name)
        return {'fig_url': fig_url}
    except Exception as e:
        # If upload fails, still return the figure object for local handling
        # and include the error message in the returned dict
        return {'fig_url': None, 'error': str(e), 'figure': fig}


def save_fig_to_gcs(fig, bucket_name: str | None, destination_blob_name: str, make_public: bool = True) -> str:
  """
  Upload a matplotlib Figure to Google Cloud Storage and return a URL.

  - fig: matplotlib Figure
  - bucket_name: name of the GCS bucket. If None, raises ValueError.
  - destination_blob_name: path inside the bucket (e.g. 'figures/plot.png')
  - make_public: if True, attempts to make the blob public (requires permissions)

  Returns a URL string. If make_public is True the returned URL will be
  `https://storage.googleapis.com/{bucket}/{path}`. If making public fails,
  still returns the same URL but includes no guarantee it's accessible.
  """
  if not bucket_name:
    raise ValueError('No bucket name provided. Set the FIGURES_BUCKET or GCS_BUCKET environment variable.')

  # write the figure to a PNG in-memory
  buf = io.BytesIO()
  fig.savefig(buf, format='png', bbox_inches='tight')
  buf.seek(0)

  client = storage.Client()
  bucket = client.bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)
  # upload_from_file accepts file-like objects
  blob.upload_from_file(buf, content_type='image/png')

  if make_public:
    try:
      blob.make_public()
    except Exception:
      # ignore failures to make public; the URL may still work if IAM allows
      pass

  url = f'https://storage.googleapis.com/{bucket_name}/{destination_blob_name}'
  return url

