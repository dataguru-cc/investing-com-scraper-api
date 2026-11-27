# Investing.com Scraper API

Scrape Investing.com with a JSON API. This repo has working Python examples for DataGuru's Investing.com scraper APIs: Investing.com Market Search and Investing.com Stock Details.

[DataGuru](https://dataguru.cc) runs the scraping, proxies, retries and parsing, and returns clean JSON. You pay only for successful requests, from $0.0012 per request, out of a prepaid balance: no subscription. New accounts get $1.00 of free credit.

## Investing.com APIs

| API | What it returns | Price | Page |
| --- | --- | --- | --- |
| [Investing.com Market Search](#investing-com-market-search) | Search Investing.com by company name or ticker and get matching stocks, ETFs, indices, funds, bonds, currencies, commodities and crypto with their symbol, exchange, country and page URL. | $0.0012 | [https://dataguru.cc/apis/investing-market-search/](https://dataguru.cc/apis/investing-market-search/) |
| [Investing.com Stock Details](#investing-com-stock-details) | Get a stock's quote from its Investing.com page, including price, change, volume, market cap, key ratios, company profile, earnings, analyst consensus, technical summary and dividends. | $0.0022 | [https://dataguru.cc/apis/investing-stock-details/](https://dataguru.cc/apis/investing-stock-details/) |

## Quick start

1. Create a free account and an API key at [dashboard.dataguru.cc](https://dashboard.dataguru.cc).
2. Install and run:

```bash
git clone https://github.com/dataguru-cc/investing-com-scraper-api.git
cd investing-com-scraper-api
pip install -r requirements.txt
export DATAGURU_API_KEY="your key"
python examples/sdk_example.py investing-market-search
```

## Examples

Every example covers all 2 Investing.com APIs. Pass an API name to run just one; with no name each script runs them all, and each call is billed at the price above.

| File | Style | Run |
| --- | --- | --- |
| [`examples/sdk_example.py`](examples/sdk_example.py) | [DataGuru Python SDK](https://github.com/dataguru-cc/dataguru-python) (`pip install dataguru-sdk`), one function per API, saves JSON to `output/` | `python examples/sdk_example.py` |
| [`examples/requests_example.py`](examples/requests_example.py) | Plain `requests`, synchronous | `python examples/requests_example.py` |
| [`examples/async_example.py`](examples/async_example.py) | `asyncio` + `httpx`, concurrent with a limit | `python examples/async_example.py` |
| [`examples/scrapy_spider.py`](examples/scrapy_spider.py) | Scrapy spider, items to JSON/CSV | `scrapy runspider examples/scrapy_spider.py -O investing-com.json` |

All requests use the header `Authorization: Api-Key YOUR_API_KEY`. Errors return `{"success": false, "error": {"code", "message", "request_id"}}`, with HTTP 402 when the balance runs out and 429 (with `Retry-After`) when rate limited. Failed requests are not charged.

## API reference

### Investing.com Market Search

Search Investing.com by company name or ticker and get matching stocks, ETFs, indices, funds, bonds, currencies, commodities and crypto with their symbol, exchange, country and page URL.

- Endpoint: `POST https://api.dataguru.cc/api/v1/investing/markets/search`
- Price: $0.0012 per successful request ($1.20 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/investing-market-search/
- Documentation: https://dataguru.cc/documentation/investing-market-search/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | no | Maximum number of results to return (1-100). Default: `20`. |
| `query` | string | yes | Company name, keyword or ticker, e.g. "apple" or "TSLA". |

**Response fields:** `query`, `total_results`, `returned_results`, `results`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/investing/markets/search" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "apple"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "query": "string",
  "total_results": 0,
  "returned_results": 0,
  "results": [
    {
      "id": "1234567890",
      "name": "string",
      "symbol": "string",
      "asset_type": "string",
      "type_label": "string",
      "exchange": "string",
      "country": "string",
      "url": "https://example.com/..."
    }
  ],
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "Investing.com Market Search",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

### Investing.com Stock Details

Get a stock's quote from its Investing.com page, including price, change, volume, market cap, key ratios, company profile, earnings, analyst consensus, technical summary and dividends.

- Endpoint: `POST https://api.dataguru.cc/api/v1/investing/stocks/details`
- Price: $0.0022 per successful request ($2.20 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/investing-stock-details/
- Documentation: https://dataguru.cc/documentation/investing-stock-details/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `stock_url` | string | yes | Full Investing.com stock URL (e.g. https://www.investing.com/equities/apple-computer-inc). |

**Response fields:** `url`, `id`, `name`, `short_name`, `symbol`, `isin`, `exchange`, `exchange_full_name`, `country`, `currency`, `is_market_open`, `is_delayed`, `price`, `market_cap`, `price_change_percent`, `key_stats`, `profile`, `earnings`, `analyst_consensus`, `technical_summary`, `dividends`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/investing/stocks/details" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"stock_url": "https://www.investing.com/equities/apple-computer-inc"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "url": "https://example.com/...",
  "id": "1234567890",
  "name": "string",
  "short_name": "string",
  "symbol": "string",
  "isin": "string",
  "exchange": "string",
  "exchange_full_name": "string",
  "country": "string",
  "currency": "USD",
  "is_market_open": false,
  "is_delayed": false,
  "price": {
    "last": 0.0,
    "change": 0.0,
    "change_percent": 0.0,
    "previous_close": 0.0,
    "open": 0.0,
    "day_high": 0.0,
    "day_low": 0.0,
    "fifty_two_week_high": 0.0,
    "fifty_two_week_low": 0.0,
    "bid": 0.0,
    "ask": 0.0,
    "volume": 0,
    "average_volume": 0,
    "last_update": "2026-01-01T12:00:00Z",
    "extended_hours": {
      "session": "pre-market",
      "price": 0.0,
      "change": 0.0,
      "change_percent": 0.0
    }
  },
  "market_cap": 0.0,
  "price_change_percent": {},
  "key_stats": {},
  "profile": {
    "sector": "string",
    "industry": "string",
    "employees": 0,
    "equity_type": "string",
    "description": "string",
    "address": "string",
    "phone": "string",
    "website": "string",
    "executives": [
      {
        "name": "string",
        "title": "string",
        "age": 0,
        "since": 0
      }
    ]
  },
  "earnings": {
    "latest_release": {
      "date": "2026-01-01T12:00:00Z",
      "date_type": "string",
      "fiscal_year": 0,
      "fiscal_quarter": 0,
      "eps_actual": 0.0,
      "eps_forecast": 0.0,
      "eps_surprise_percent": 0.0,
      "revenue_actual": 0.0,
      "revenue_forecast": 0.0,
      "revenue_surprise_percent": 0.0
    },
    "next_release": {
      "date": "2026-01-01T12:00:00Z",
      "date_type": "string",
      "fiscal_year": 0,
      "fiscal_quarter": 0,
      "eps_actual": 0.0,
      "eps_forecast": 0.0,
      "eps_surprise_percent": 0.0,
      "revenue_actual": 0.0,
      "revenue_forecast": 0.0,
      "revenue_surprise_percent": 0.0
    }
  },
  "analyst_consensus": {
    "recommendation": "string",
    "target_price_mean": 0.0,
    "target_price_high": 0.0,
    "target_price_low": 0.0,
    "upside_percent": 0.0,
    "analysts": 0,
    "buy": 0,
    "hold": 0,
    "sell": 0,
    "last_rating_date": "2026-01-01T12:00:00Z"
  },
  "technical_summary": [
    {
      "interval": "string",
      "summary": "string",
      "moving_averages": "string",
      "moving_averages_buy": 0,
      "moving_averages_sell": 0,
      "indicators": "string",
      "indicators_buy": 0,
      "indicators_sell": 0,
      "as_of": "string"
    }
  ],
  "dividends": [
    {
      "ex_date": "2026-01-01T12:00:00Z",
      "amount": 0.0,
      "type": "string",
      "payment_date": "2026-01-01T12:00:00Z",
      "yield_percent": 0.0
    }
  ],
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "Investing.com Stock Details",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

## More

- Python SDK and examples for all DataGuru APIs: [github.com/dataguru-cc/dataguru-python](https://github.com/dataguru-cc/dataguru-python) ([docs](https://dataguru-python.readthedocs.io/))
- Every API, with a live playground: [https://dataguru.cc/apis/](https://dataguru.cc/apis/)
- Use DataGuru from Claude, ChatGPT or Cursor through the MCP server: [https://dataguru.cc/mcp/](https://dataguru.cc/mcp/)
- Run thousands of inputs from a CSV at half price with batch jobs: [https://dataguru.cc/documentation/](https://dataguru.cc/documentation/)
- Other scraper APIs: [1688](https://github.com/dataguru-cc/1688-scraper-api), [Airbnb](https://github.com/dataguru-cc/airbnb-scraper-api), [Alibaba](https://github.com/dataguru-cc/alibaba-scraper-api), [AliExpress](https://github.com/dataguru-cc/aliexpress-scraper-api), [Amazon](https://github.com/dataguru-cc/amazon-scraper-api), [arXiv](https://github.com/dataguru-cc/arxiv-scraper-api), [ASOS](https://github.com/dataguru-cc/asos-scraper-api), [Best Buy](https://github.com/dataguru-cc/best-buy-scraper-api), [Booking.com](https://github.com/dataguru-cc/booking-scraper-api), [Brave Search](https://github.com/dataguru-cc/brave-search-scraper-api), [CA State Bar](https://github.com/dataguru-cc/california-state-bar-scraper-api), [Capterra](https://github.com/dataguru-cc/capterra-scraper-api), [CoinGecko](https://github.com/dataguru-cc/coingecko-scraper-api), [CoinMarketCap](https://github.com/dataguru-cc/coinmarketcap-scraper-api), [Companies House](https://github.com/dataguru-cc/companies-house-scraper-api), [Costco](https://github.com/dataguru-cc/costco-scraper-api), [CourtListener](https://github.com/dataguru-cc/courtlistener-scraper-api), [Crunchbase](https://github.com/dataguru-cc/crunchbase-scraper-api), [Discord](https://github.com/dataguru-cc/discord-scraper-api), [DoorDash](https://github.com/dataguru-cc/doordash-scraper-api), [eBay](https://github.com/dataguru-cc/ebay-scraper-api), [Etsy](https://github.com/dataguru-cc/etsy-scraper-api), [Expedia](https://github.com/dataguru-cc/expedia-scraper-api), [Fiverr](https://github.com/dataguru-cc/fiverr-scraper-api), [Flipkart](https://github.com/dataguru-cc/flipkart-scraper-api), [Glassdoor](https://github.com/dataguru-cc/glassdoor-scraper-api), [Google Flights](https://github.com/dataguru-cc/google-flights-scraper-api), [Google Patents](https://github.com/dataguru-cc/google-patents-scraper-api), [Google Scholar](https://github.com/dataguru-cc/google-scholar-scraper-api), [Google Search](https://github.com/dataguru-cc/google-search-scraper-api), [Grubhub](https://github.com/dataguru-cc/grubhub-scraper-api), [Home Depot](https://github.com/dataguru-cc/home-depot-scraper-api), [Instagram](https://github.com/dataguru-cc/instagram-scraper-api), [Justia](https://github.com/dataguru-cc/justia-scraper-api), [Kayak](https://github.com/dataguru-cc/kayak-scraper-api), [Kick](https://github.com/dataguru-cc/kick-scraper-api), [Lazada](https://github.com/dataguru-cc/lazada-scraper-api), [MarketWatch](https://github.com/dataguru-cc/marketwatch-scraper-api), [Mercado Libre](https://github.com/dataguru-cc/mercado-libre-scraper-api), [Monster](https://github.com/dataguru-cc/monster-scraper-api), [OpenCorporates](https://github.com/dataguru-cc/opencorporates-scraper-api), [OpenTable](https://github.com/dataguru-cc/opentable-scraper-api), [PACER](https://github.com/dataguru-cc/pacer-scraper-api), [PitchBook](https://github.com/dataguru-cc/pitchbook-scraper-api), [PubMed](https://github.com/dataguru-cc/pubmed-scraper-api), [Reddit](https://github.com/dataguru-cc/reddit-scraper-api), [Redfin](https://github.com/dataguru-cc/redfin-scraper-api), [Resy](https://github.com/dataguru-cc/resy-scraper-api), [Rightmove](https://github.com/dataguru-cc/rightmove-scraper-api), [SEC EDGAR](https://github.com/dataguru-cc/sec-edgar-scraper-api), [Seeking Alpha](https://github.com/dataguru-cc/seeking-alpha-scraper-api), [Shopee](https://github.com/dataguru-cc/shopee-scraper-api), [Skyscanner](https://github.com/dataguru-cc/skyscanner-scraper-api), [Target](https://github.com/dataguru-cc/target-scraper-api), [TikTok](https://github.com/dataguru-cc/tiktok-scraper-api), [TradingView](https://github.com/dataguru-cc/tradingview-scraper-api), [TripAdvisor](https://github.com/dataguru-cc/tripadvisor-scraper-api), [Trulia](https://github.com/dataguru-cc/trulia-scraper-api), [TrustRadius](https://github.com/dataguru-cc/trustradius-scraper-api), [Twitch](https://github.com/dataguru-cc/twitch-scraper-api), [Uber Eats](https://github.com/dataguru-cc/uber-eats-scraper-api), [Upwork](https://github.com/dataguru-cc/upwork-scraper-api), [Vrbo](https://github.com/dataguru-cc/vrbo-scraper-api), [Walmart](https://github.com/dataguru-cc/walmart-scraper-api), [Wayfair](https://github.com/dataguru-cc/wayfair-scraper-api), [X (Twitter)](https://github.com/dataguru-cc/twitter-scraper-api), [Yahoo Finance](https://github.com/dataguru-cc/yahoo-finance-scraper-api), [YouTube](https://github.com/dataguru-cc/youtube-scraper-api), [Zillow](https://github.com/dataguru-cc/zillow-scraper-api), [ZoomInfo](https://github.com/dataguru-cc/zoominfo-scraper-api), [Zoopla](https://github.com/dataguru-cc/zoopla-scraper-api)

## License

The example code is MIT licensed. Use of the DataGuru API is subject to the [terms of service](https://dataguru.cc/terms/).
