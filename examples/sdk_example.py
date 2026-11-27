"""Investing.com scraper API: DataGuru Python SDK example.

Runs DataGuru's Investing.com APIs and prints the JSON they return:
  - Investing.com Market Search: $0.0012 per successful request ($1.20 per 1,000)
  - Investing.com Stock Details: $0.0022 per successful request ($2.20 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    python examples/sdk_example.py            # every API below
    python examples/sdk_example.py investing-market-search
"""
import json
import sys
from pathlib import Path

from dataguru import DataGuru, DataGuruError

def investing_market_search(dg):
    """Investing.com Market Search: Search Investing.com by company name or ticker and get matching stocks, ETFs, indices, funds, bonds, currencies, commodities and crypto with their symbol, exchange, country and page URL."""
    return dg.call(
        "investing-market-search",
        query="apple",
    )


def investing_stock_details(dg):
    """Investing.com Stock Details: Get a stock's quote from its Investing.com page, including price, change, volume, market cap, key ratios, company profile, earnings, analyst consensus, technical summary and dividends."""
    return dg.call(
        "investing-stock-details",
        stock_url="https://www.investing.com/equities/apple-computer-inc",
    )


EXAMPLES = {
    "investing-market-search": investing_market_search,
    "investing-stock-details": investing_stock_details,
}
DEFAULT = ['investing-market-search', 'investing-stock-details']


def main(names):
    out = Path("output")
    out.mkdir(exist_ok=True)
    with DataGuru() as dg:  # reads DATAGURU_API_KEY
        for name in names:
            data = EXAMPLES[name](dg)
            (out / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"{name}: saved output/{name}.json")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    names = sys.argv[1:] or DEFAULT
    unknown = [n for n in names if n not in EXAMPLES]
    if unknown:
        sys.exit(f"Unknown API {unknown}. Choose from: {', '.join(EXAMPLES)}")
    try:
        main(names)
    except DataGuruError as error:
        sys.exit(f"DataGuru error: {error}")
