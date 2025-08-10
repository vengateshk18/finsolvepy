# finsolvepy

**`finsolvepy`** is a versatile Python package for financial enthusiasts and professionals, offering powerful tools to access and analyze **stock market**, **cryptocurrency**, and **currency exchange** data.  
Whether you are a retail investor, analyst, or developer, `finsolvepy` provides an easy-to-use API to fetch, validate, and calculate financial metrics.

---

## 📌 Features

### **Stocks & Indices**
- **Detailed Stock Information** – Get market cap, price, company description, ROE, ROCE, and more.
- **Validate Stock Symbols** – Ensure ticker symbols are correct before querying.
- **Market Index Data** – Retrieve descriptions and lists of Indian and US indices.

### **Cryptocurrencies**
- **Detailed Coin Information** – Access market cap, price, description, rankings, and more.
- **Validate Crypto Symbols** – Quickly check if a cryptocurrency ticker is valid.

### **Currency Conversion**
- **Currency Converter** – Convert amounts between any two currencies in real time.
- **Exchange Rates** – Fetch the current exchange rate between two currencies.

### **Financial Calculations**
- **Price-to-Earnings (P/E) Ratio**
- **Years to Double Investment**

---

## 📦 Installation

```bash
pip install finsolvepy
````

---

## 💡 Usage Examples

### 1️⃣ Get Detailed Stock Information

```python
from finsolvepy.information import StockInsights

obj = StockInsights()
apple_details = obj.stock_detail('AAPL')
print(apple_details)
```

**Example Output:**

```json
{
  "symbol": "AAPL",
  "company": "Apple Inc",
  "market_cap": "3456956105000 USD",
  "about": "Apple Inc. is an American multinational technology company...",
  "curr_market_price": "$227.3877",
  "book_value": "51.83",
  "dividend": "0.0044",
  "roce": 3.812053060477029,
  "roe": "1.606",
  "face_value": 10
}
```

---

### 2️⃣ Validate Stock Symbol

```python
from finsolvepy.information import StockInsights

obj = StockInsights()
print(obj.is_valid_symbol('TATAMOTORS'))
```

**Output:**

```bash
True
```

---

### 3️⃣ Calculate Price-to-Earnings (P/E) Ratio

```python
from finsolvepy.calculation import Metrics

obj = Metrics()
pe = obj.pe_ratio(earnings=227270000000, no_of_shares=2534202430, current_market_price=1779)
print(pe)
```

**Output:**

```bash
19.836960984599816
```

---

### 4️⃣ Calculate Years to Double Your Money

```python
from finsolvepy.calculation import Metrics

obj = Metrics()
years = obj.years_to_double_money(interest=7.5)
print(years)
```

**Output:**

```bash
9.6 years
```

---

### 5️⃣ Get Cryptocurrency Details

```python
from finsolvepy.information import CryptocurrencyInsights

crypto = CryptocurrencyInsights()
btc_details = crypto.coin_details("Bitcoin")
print(btc_details)
```

**Example Output:**

```json
{
  "data": {
    "name": "Bitcoin",
    "symbol": "btc",
    "description": "Bitcoin is the first successful internet money...",
    "current_price_usd": 118745,
    "market_cap": 2363422930356,
    "volume": 34429259271,
    "market_cap_rank": 1,
    "fully_diluted_valuation": 2363422930356,
    "last_updated": "2025-08-10T14:58:20.713Z"
  }
}
```

---

### 6️⃣ Validate Cryptocurrency Symbol

```python
from finsolvepy.information import CryptocurrencyInsights

crypto = CryptocurrencyInsights()
print(crypto.is_valid_symbol("BTC"))
```

**Output:**

```bash
True
```

---

### 7️⃣ Convert Currency

```python
from finsolvepy.information import CurrencyConverter

cc = CurrencyConverter()
converted_amount = cc.convert(from_currency="INR", to_currency="USD", amount=100)
print(converted_amount)
```

**Output:**

```bash
$1.141
```

---

### 8️⃣ Get Currency Exchange Rate

```python
from finsolvepy.information import CurrencyConverter

cc = CurrencyConverter()
rate = cc.exchange_rate(from_currency="USD", to_currency="INR")
print(rate)
```

**Output:**

```bash
87.6119
```

---

## 🏁 Conclusion

With a wide range of features — from stock market insights to cryptocurrency analysis and currency conversion — `finsolvepy` is your go-to toolkit for financial data.
Whether you're an experienced trader or just starting your investment journey, `finsolvepy` empowers you to make informed financial decisions.

---

## 👨‍💻 Author

**Vengatesh K**
[GitHub](https://github.com/vengateshk18)
Feel free to fork the repository and contribute!
