# finsolvepy

`finsolvepy` is a comprehensive Python package designed for financial enthusiasts and professionals. It provides insightful tools for obtaining detailed information about stocks and market indices. By leveraging data from CSV files and Market Data, this package allows users to fetch stock details, validate stock symbols, and retrieve descriptions for various market indices effortlessly.

## Features

- **Fetch Detailed Stock Information**: Easily retrieve comprehensive data for specified stock symbols, including market cap, current market price, and company descriptions.
  
- **Validate Stock Symbols**: Check the validity of stock symbols in market data to ensure accurate information retrieval.

- **Retrieve Index Descriptions**: Get detailed descriptions for a variety of market indices, enhancing your understanding of different markets.

- **List Indices**: Access a list of all indices available in the Indian and US markets, providing a broader context for financial analysis.

## Installation

Before using the package, you need to install it. You can do this via pip:

```bash
pip install finsolvepy
```

## Example Usage

### Get Details About a Specific Stock

To retrieve information about a specific stock, such as Apple Inc. (AAPL), you can use the following code:

```python
from finsolvepy.information import StockInsights

obj = StockInsights()
apple_details = obj.stock_detail('AAPL')
print(apple_details)
```

### Expected Output

```json
{
  "symbol": "AAPL",
  "company": "Apple Inc",
  "market_cap": "3456956105000 USD",
  "about": "Apple Inc. is an American multinational technology company that specializes in consumer electronics, computer software, and online services. Apple is the world's largest technology company by revenue (totalling $274.5 billion in 2020) and, since January 2021, the world's most valuable company. As of 2021, Apple is the world's fourth-largest PC vendor by unit sales, and fourth-largest smartphone manufacturer. It is one of the Big Five American information technology companies, along with Amazon, Google, Microsoft, and Facebook.",
  "curr_market_price": "$227.3877",
  "book_value": "51.83",
  "dividend": "0.0044",
  "roce": 3.812053060477029,
  "roe": "1.606",
  "face_value": null
}
```

### Check if a Stock Symbol is Valid

To verify the validity of a stock symbol, such as TATAMOTORS, you can run:

```python
from finsolvepy.information import StockInsights

obj = StockInsights()
tatamotors_symbol = obj.is_valid_symbol('TATAMOTORS')
print(tatamotors_symbol)
```

### Expected Output

```bash
True
```

### Calculate the P/E Ratio of a Company

To find the Price-to-Earnings (P/E) ratio for a company, you can use the `Metrics` class:

```python
from finsolvepy.calculation import Metrics

obj = Metrics()
hdfc_bank_pe = obj.pe_ratio(earnings=227270000000, no_of_shares=2534202430, current_market_price=1779)
print(hdfc_bank_pe)
```

### Expected Output

```bash
19.836960984599816
```

### Determine the Number of Years to Double Your Money

You can also calculate how many years it will take to double your investment based on a given interest rate:

```python
from finsolvepy.calculation import Metrics

obj = Metrics()
fd_interest = obj.years_to_double_money(interest=7.5)
print(fd_interest)
```

### Expected Output 

```bash
9.6 years
```

## Conclusion

With a wide array of methods and functionalities, the `finsolvepy` package is your go-to solution for financial data analysis. Whether you're a seasoned investor or just getting started, this package will enhance your financial decision-making process. Enjoy exploring the features!


## Credits

By **Vengatesh K**  
[GitHub](https://github.com/vengateshk18)  
Feel free to fork the repository and make changes!