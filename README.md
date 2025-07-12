
# 📈 Stock Market ETL (Automated with GitHub Actions)

This project performs weekly extraction, transformation, and visualization of the most active stocks on the market using Python, `yfinance`, and `matplotlib`. The results are automatically updated every week via **GitHub Actions**.

---

## 🔁 Project Workflow

1. 🧠 **Extraction**: scrape the most active tickers from Yahoo Finance
2. 📉 **Download**: historical stock prices with `yfinance`
3. 🧪 **Transformation**: compute weekly average prices
4. 📊 **Visualization**: plot top 10 most valuable stocks
5. 🔄 **Automation**: run weekly with GitHub Actions

---

## 🗂️ Project Structure

```
📁 images/
   └── top10_graph.png       ← weekly updated chart
📄 main_stock_etl_clean.py   ← main ETL script
📄 requirements.txt          ← dependencies
📄 .github/workflows/        ← GitHub Actions workflow
```

---

## 🛠️ Technologies Used

- Python 3.10
- `yfinance`, `pandas`, `matplotlib`, `beautifulsoup4`
- GitHub Actions
- Git & GitHub (for version control and CI/CD)

---

## 🕒 Weekly Automation

[![ETL Status](https://github.com/galo-coder/stock-market-etl/actions/workflows/run_stock_etl.yml/badge.svg)](https://github.com/galo-coder/stock-market-etl/actions)

Every Monday at 7am (Lima 🇵🇪 time), the workflow automatically:
- Fetches the latest data
- Regenerates the stock chart
- Commits the image back to the repository

---

## 📊 Latest Generated Chart

![Top 10 Stocks](images/top10_graph.png)

---

## 🧠 Author

- 👤 Gonzalo Rivera – [galo-coder](https://github.com/galo-coder)
- 💼 Data Engineer | Specialist in Azure, ETL, Visualization, and Automation

---
