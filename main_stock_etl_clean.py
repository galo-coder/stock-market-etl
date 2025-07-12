
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import os

# Create folder for the chart
os.makedirs("images", exist_ok=True)

# ─────────────────────────────────────────────
# 1. EXTRACT DYNAMIC TICKERS FROM YAHOO
# ─────────────────────────────────────────────

HEADERS = {"User-Agent": "Mozilla/5.0"}
def get_top_tickers(url, top_n=3):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table_container = soup.find("div", class_="tableContainer")
    links = table_container.find_all("a", href=True)
    quote_links = [a["href"] for a in links if a["href"].startswith("/quote/")]
    tickers = [link.split("/")[2] for link in quote_links if len(link.split("/")) >= 3]
    return list(dict.fromkeys(tickers))[:top_n]

url = "https://es-us.finanzas.yahoo.com/mercados/acciones/m%C3%A1s-activas/?start=0&count=200"
tickers = get_top_tickers(url, 20)

# ─────────────────────────────────────────────
# 2. DOWNLOAD PRICES WITH YFINANCE
# ─────────────────────────────────────────────

end_date = datetime.today().date()
start_date = end_date - timedelta(days=365)
start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")
print(f"[INFO] Extracting data desde {start_date} hasta {end_date}")

df = yf.download(
    tickers=tickers,
    start=start_date,
    end=end_date,
    interval='1d',
    group_by='ticker',
    auto_adjust=True,
    threads=False,
    progress=False
)

close_df = pd.DataFrame()
for ticker in tickers:
    temp = df[ticker][['Close']].copy()
    temp.columns = [f"{ticker}_close"]
    close_df = pd.concat([close_df, temp], axis=1)

close_long_df = close_df.reset_index().melt(
    id_vars=["Date"],
    var_name="Ticker_code",
    value_name="Close_Amount"
)
close_long_df["Ticker_code"] = close_long_df["Ticker_code"].str.replace("_close", "")

# ─────────────────────────────────────────────
# 3. GET COMPANY NAMES
# ─────────────────────────────────────────────

def get_company_name_and_sector(ticker):
    try:
        info = yf.Ticker(ticker).info
        return {
            "Ticker_code": ticker,
            "Company_Name": info.get("longName", None),
            "Sector": info.get("sector", None)
        }
    except Exception:
        return {"Ticker_code": ticker, "Company_Name": None, "Sector": None}

company_data = [get_company_name_and_sector(t) for t in tickers]
dim_company = pd.DataFrame(company_data)

# ─────────────────────────────────────────────
# 4. TRANSFORMATION AND VISUALIZATION
# ─────────────────────────────────────────────

fact = close_long_df
dim = dim_company

fact["Date"] = pd.to_datetime(fact["Date"])
fact["Close_Amount"] = pd.to_numeric(fact["Close_Amount"], errors="coerce")
fact["YearWeek"] = fact["Date"].dt.strftime("%Y%U")

weekly_avg = fact.groupby(["Ticker_code", "YearWeek"]).agg({
    "Close_Amount": "mean"
}).reset_index()

latest_week = weekly_avg["YearWeek"].max()
top_tickers = (
    weekly_avg[weekly_avg["YearWeek"] == latest_week]
    .sort_values("Close_Amount", ascending=False)
    .head(10)["Ticker_code"]
    .tolist()
)
filtered_df = weekly_avg[weekly_avg["Ticker_code"].isin(top_tickers)]
result = filtered_df.merge(dim, on="Ticker_code", how="left")

label_map = {
    row["Ticker_code"]: f"{row['Company_Name']} ({row['Ticker_code']})"
    for _, row in result.drop_duplicates("Ticker_code").iterrows()
}

plt.figure(figsize=(14, 7))
for ticker in result["Ticker_code"].unique():
    subset = result[result["Ticker_code"] == ticker]
    label = label_map.get(ticker, ticker)
    plt.plot(subset["YearWeek"], subset["Close_Amount"], label=label)
    max_row = subset.loc[subset["Close_Amount"].idxmax()]
    plt.annotate(
        f"{max_row['Close_Amount']:.2f}",
        xy=(max_row["YearWeek"], max_row["Close_Amount"]),
        xytext=(0, 5),
        textcoords="offset points",
        fontsize=8,
        ha='center',
        color="black"
    )

plt.legend()
plt.title(f"Top 10 most valuable stocks (up to week {latest_week})")
plt.xlabel("Week")
plt.ylabel("Average closing price ($)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("images/top10_graph.png")
