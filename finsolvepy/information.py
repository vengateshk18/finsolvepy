# In finsolvepy/information.py
import pandas as pd
from finsolvepy.database.company_symbol_dict import company_dict 
from finsolvepy.database.apis import DATA_APIS
import json
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

market_api = DATA_APIS['ALPHA_VANTAGE_API_KEY']
currency_api = DATA_APIS['CURRENCY_API_KEY']


class StockInsights:
    """
    A class to provide comprehensive insights and detailed information about stocks and market indices.

    This class enables users to fetch detailed stock information, validate stock symbols and indices,
    and retrieve descriptions for various market indices. It utilizes local data sources and external 
    market data providers to gather comprehensive financial information.

    Attributes:
        stock (pandas.DataFrame): DataFrame containing stock information loaded from local database.
        index (pandas.DataFrame): DataFrame containing index descriptions from local database.

    Methods:
        stock_detail(symbol): Fetches detailed information for a specified stock symbol.
        index_lists(): Returns a list of all available market indices.
        index_description(index): Retrieves description of a specified market index.
        is_valid_symbol(symbol): Validates if a stock symbol exists in market data.
        is_valid_index(index): Validates if an index exists in the database.
    """

    def __init__(self) -> None:
        """
        Initialize the StockInsights class.
        
        Loads stock and index data from local CSV files in the database directory.
        Sets up the necessary data structures for market analysis operations.
        """
        # Get the directory of the current file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.stock = pd.read_csv(os.path.join(base_dir, 'database', 'complete_data.csv'))
        self.index = pd.read_csv(os.path.join(base_dir, 'database', 'indices_descriptions.csv'))

    def stock_detail(self, symbol: str) -> dict:
        """
        Retrieve comprehensive stock information for a given stock symbol.
        
        Fetches detailed financial information including market cap, current price,
        financial ratios, and company description for the specified stock symbol.
        
        Args:
            symbol (str): The stock symbol for which details are to be retrieved.
        
        Returns:
            dict: A dictionary containing stock information with the following structure:
                {
                    "symbol": str,
                    "company": str,
                    "market_cap": str,
                    "about": str,
                    "curr_market_price": str,
                    "pe_ratio": float (Indian stocks only),
                    "book_value": str,
                    "divident": str,
                    "roce": float,
                    "roe": str,
                    "face_value": str
                }
                If error occurs: {"error": str}
        
        Example:
            >>> insights = StockInsights()
            >>> result = insights.stock_detail("AAPL")
            >>> print(result["company"])  # Apple Inc.
        """
        try:
            # Check local database first
            if symbol in self.stock['symbol'].values:
                stock = self.stock.loc[self.stock['symbol'] == symbol]
                
                if stock.empty:
                    return json.dumps({"error": f"No information available for the stock symbol '{symbol}'."}, indent=2)

                stock_info = {
                    'symbol': stock['symbol'].values[0],
                    'company': stock['name'].values[0],
                    'market_cap': str(int(stock['market_cap'].values[0])) + " crores" if not pd.isna(stock['market_cap'].values[0]) else "N/A",
                    'about': stock['about'].values[0] if not pd.isna(stock['about'].values[0]) else "No information available",
                    'curr_market_price': stock['curr_market_price'].values[0] if not pd.isna(stock['curr_market_price'].values[0]) else "N/A",
                    'pe_ratio': stock['pe_ratio'].values[0] if not pd.isna(stock['pe_ratio'].values[0]) else "N/A",
                    'book_value': stock['book_value'].values[0] if not pd.isna(stock['book_value'].values[0]) else "N/A",
                    'divident': stock['divident'].values[0] if not pd.isna(stock['divident'].values[0]) else "N/A",
                    'roce': stock['roce'].values[0] if not pd.isna(stock['roce'].values[0]) else "N/A",
                    'roe': stock['roe'].values[0] if not pd.isna(stock['roe'].values[0]) else "N/A",
                    'face_value': stock['face_value'].values[0] if not pd.isna(stock['face_value'].values[0]) else "N/A",
                }
                return json.dumps(stock_info, indent=2)
            
            # Check external data source if not found locally
            try:
                us_response = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={market_api}")
                
                if us_response.text == "{}":
                    return json.dumps({"error": f"Information for '{symbol}' is not available or the symbol is invalid."}, indent=2)
                
                stock = us_response.json()
                
                # Calculate current market price and ROCE safely
                try:
                    current_price = float(stock.get('PERatio', 0)) * float(stock.get('EPS', 0))
                    current_price_str = f"${current_price:.2f}" if current_price > 0 else "N/A"
                except (ValueError, TypeError):
                    current_price_str = "N/A"
                
                try:
                    ebitda = float(stock.get('EBITDA', 0))
                    market_cap = float(stock.get('MarketCapitalization', 0))
                    roce = (ebitda / market_cap) * 100 if market_cap > 0 else 0
                except (ValueError, TypeError):
                    roce = "N/A"
                
                data = {
                    'symbol': stock.get('Symbol', 'N/A'),
                    'company': stock.get('Name', 'N/A'),
                    'market_cap': str(stock.get('MarketCapitalization', 'N/A')) + " USD",
                    'about': stock.get('Description', 'No information available'),
                    'curr_market_price': current_price_str,
                    'book_value': stock.get('PriceToBookRatio', 'N/A'),
                    'divident': stock.get('DividendYield', 'N/A'),
                    'roce': roce,
                    'roe': stock.get('ReturnOnEquityTTM', 'N/A'),
                    'face_value': None
                }
                return json.dumps(data, indent=2)
                
            except requests.RequestException:
                return json.dumps({"error": f"Unable to fetch data for symbol '{symbol}'. Please check the symbol and try again."}, indent=2)
            except Exception:
                return json.dumps({"error": f"An unexpected error occurred while processing '{symbol}'."}, indent=2)

        except Exception:
            return json.dumps({"error": f"An unexpected error occurred while processing '{symbol}'."}, indent=2)

    def index_lists(self) -> dict:
        """
        Retrieve a list of all available market indices.

        Returns all market indices available in the database, including both
        Indian and international market indices.

        Args:
            None

        Returns:
            dict: A dictionary containing the indices list with the following structure:
                {"Index": list} - List of all available index names
                If error occurs: {"error": str}

        Example:
            >>> insights = StockInsights()
            >>> result = insights.index_lists()
            >>> print(len(result["Index"]))  # Number of available indices
        """
        try:
            if 'Index' not in self.index.columns:
                return json.dumps({"error": "'Index' column not found in the database."}, indent=2)

            index_list = self.index['Index'].values.tolist()
            return json.dumps({"Index": index_list}, indent=2)

        except Exception:
            return json.dumps({"error": "An unexpected error occurred while retrieving index list."}, indent=2)

    def index_description(self, index: str) -> dict:
        """
        Retrieve detailed description of a specified market index.

        Provides comprehensive information about a market index including its
        description, region, and exchange details.

        Args:
            index (str): The name of the index for which to retrieve information.

        Returns:
            dict: A dictionary containing index details with the following structure:
                {
                    "Index": str,
                    "Region": str,
                    "Description": str
                }
                If error occurs: {"error": str}

        Example:
            >>> insights = StockInsights()
            >>> result = insights.index_description("S&P 500")
            >>> print(result["Description"])  # Index description
        """
        try:
            if not isinstance(index, str):
                return json.dumps({"error": "The index parameter must be a string."}, indent=2)

            if index not in self.index['Index'].values:
                return json.dumps({"error": f"Information for '{index}' is not available or the index is invalid."}, indent=2)

            info = self.index[self.index['Index'] == index]

            data = {
                "Index": info['Index'].values[0],
                "Region": info['Exchange'].values[0],
                "Description": info['Description'].values[0]
            }
            return json.dumps(data, indent=2)

        except Exception:
            return json.dumps({"error": f"An unexpected error occurred while processing '{index}'."}, indent=2)

    def is_valid_symbol(self, symbol: str) -> dict:
        """
        Validate if a stock symbol exists in available market data.

        Checks both local database and external market data sources to determine
        if the provided stock symbol is valid and tradeable.

        Args:
            symbol (str): The stock symbol to validate.

        Returns:
            dict: A dictionary containing validation result with the following structure:
                {"is_valid": bool} - True if symbol exists, False otherwise
                If error occurs: {"error": str}

        Example:
            >>> insights = StockInsights()
            >>> result = insights.is_valid_symbol("AAPL")
            >>> print(result["is_valid"])  # True or False
        """
        try:
            if not isinstance(symbol, str):
                return json.dumps({"error": "The provided symbol must be a string."}, indent=2)

            # Check local database first
            if symbol in self.stock['symbol'].values:
                return json.dumps({"is_valid": True}, indent=2)

            # Check external data source
            try:
                response = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={market_api}')
                return json.dumps({"is_valid": response.text != "{}"}, indent=2)
            except requests.RequestException:
                return json.dumps({"is_valid": False}, indent=2)

        except Exception:
            return json.dumps({"error": f"An unexpected error occurred while validating '{symbol}'."}, indent=2)

    def is_valid_index(self, index: str) -> dict:
        """
        Validate if an index exists in the available market data.

        Checks the local database to determine if the provided index name
        is valid and available for analysis.

        Args:
            index (str): The index name to validate.

        Returns:
            dict: A dictionary containing validation result with the following structure:
                {"is_valid": bool} - True if index exists, False otherwise
                If error occurs: {"error": str}

        Example:
            >>> insights = StockInsights()
            >>> result = insights.is_valid_index("NIFTY 50")
            >>> print(result["is_valid"])  # True or False
        """
        try:
            if not isinstance(index, str):
                return json.dumps({"error": "The provided index must be a string."}, indent=2)

            if 'Index' not in self.index.columns:
                return json.dumps({"error": "'Index' column not found in the database."}, indent=2)

            return json.dumps({"is_valid": index in self.index['Index'].values}, indent=2)

        except Exception:
            return json.dumps({"error": f"An unexpected error occurred while validating '{index}'."}, indent=2)

    def __str__(self):
        return "StockInsights Class for Market Analysis"

    def __repr__(self):
        return "StockInsights()"


class CryptocurrencyInsights:
    """
    A class to provide comprehensive insights and detailed information about cryptocurrencies.

    This class enables users to fetch detailed cryptocurrency information, validate coin symbols and names,
    and retrieve current pricing data from cryptocurrency markets. It provides comprehensive market analysis
    capabilities with structured data handling and robust error management.

    Attributes:
        base_url (str): The base URL endpoint for accessing cryptocurrency market data.

    Methods:
        coin_details(coin_name, coin_symbol): Fetches detailed cryptocurrency information.
        is_valid_symbol(coin_symbol): Validates if a cryptocurrency symbol exists.
        is_valid_name(coin_name): Validates if a cryptocurrency name exists.
        get_current_price(coin_name, coin_symbol): Retrieves current cryptocurrency price.
    """

    def __init__(self):
        """
        Initialize the CryptocurrencyInsights class.
        
        Sets up the base URL for accessing cryptocurrency market data and prepares
        the instance for making market data requests.
        """
        self.base_url = "https://api.coingecko.com/api/v3"

    def coin_details(self, coin_name: str = None, coin_symbol: str = None) -> dict:
        """
        Retrieve comprehensive cryptocurrency information from market data.

        Fetches detailed information about a specific cryptocurrency including
        current price, market capitalization, trading volume, and other relevant
        market metrics. Either coin name or symbol must be provided.

        Args:
            coin_name (str, optional): Full name of the cryptocurrency (e.g., "Bitcoin").
            coin_symbol (str, optional): Ticker symbol of the cryptocurrency (e.g., "BTC").

        Returns:
            dict: A dictionary containing cryptocurrency details with the following structure:
                {
                    "data": {
                        "name": str,
                        "symbol": str,
                        "description": str,
                        "current_price_usd": float,
                        "market_cap": float,
                        "volume": float,
                        "market_cap_rank": int,
                        "fully_diluted_valuation": float,
                        "last_updated": str
                    }
                }
                If error occurs: {"error": str}

        Example:
            >>> crypto = CryptocurrencyInsights()
            >>> result = crypto.coin_details(coin_symbol="BTC")
            >>> print(result["data"]["current_price_usd"])  # Current Bitcoin price
        """
        if not coin_name and not coin_symbol:
            return json.dumps({"error": "You must provide either 'coin_name' or 'coin_symbol'."}, indent=2)

        try:
            # Get coin list from market data
            response = requests.get(f"{self.base_url}/coins/list")
            coins = response.json()

            # Find matching coin_id
            coin_id = None
            for coin in coins:
                if coin_name and coin['name'].lower() == coin_name.lower():
                    coin_id = coin['id']
                    break
                if coin_symbol and coin['symbol'].lower() == coin_symbol.lower():
                    coin_id = coin['id']
                    break

            if not coin_id:
                return json.dumps({"error": "No coin found matching the provided name or symbol."}, indent=2)

            # Fetch coin details
            coin_detail_url = f"{self.base_url}/coins/{coin_id}"
            detail_response = requests.get(coin_detail_url)
            data = detail_response.json()

            # Filter required fields
            filtered_data = {
                "name": data.get("name", "N/A"),
                "symbol": data.get("symbol", "N/A"),
                "description": data.get("description", {}).get("en", "No description available").strip(),
                "current_price_usd": data.get("market_data", {}).get("current_price", {}).get("usd", 0.0),
                "market_cap": data.get("market_data", {}).get("market_cap", {}).get("usd", 0.0),
                "volume": data.get("market_data", {}).get("total_volume", {}).get("usd", 0.0),
                "market_cap_rank": data.get("market_cap_rank", 0),
                "fully_diluted_valuation": data.get("market_data", {}).get("fully_diluted_valuation", {}).get("usd", 0.0),
                "last_updated": data.get("last_updated", "N/A")
            }

            return json.dumps({"data": filtered_data}, indent=2)

        except requests.RequestException:
            return json.dumps({"error": "Unable to fetch cryptocurrency data. Please check your connection and try again."}, indent=2)
        except Exception:
            return json.dumps({"error": "An unexpected error occurred while processing the cryptocurrency request."}, indent=2)

    def is_valid_symbol(self, coin_symbol: str) -> dict:
        """
        Validate if a cryptocurrency symbol exists in market data.

        Checks whether the provided cryptocurrency ticker symbol is valid
        and available in the cryptocurrency market data sources.

        Args:
            coin_symbol (str): The ticker symbol of the cryptocurrency to validate.

        Returns:
            dict: A dictionary containing validation result with the following structure:
                {"is_valid": bool} - True if symbol is valid, False otherwise
                If error occurs: {"error": str}

        Example:
            >>> crypto = CryptocurrencyInsights()
            >>> result = crypto.is_valid_symbol("BTC")
            >>> print(result["is_valid"])  # True or False
        """
        try:
            response = requests.get(f"{self.base_url}/coins/markets", 
                                  params={"vs_currency": "usd", "symbols": coin_symbol})
            data = response.json()
            
            return json.dumps({"is_valid": len(data) > 0}, indent=2)
            
        except requests.RequestException:
            return json.dumps({"error": "Unable to validate coin symbol. Please check your connection and try again."}, indent=2)
        except Exception:
            return json.dumps({"error": "An unexpected error occurred while validating the coin symbol."}, indent=2)

    def is_valid_name(self, coin_name: str) -> dict:
        """
        Validate if a cryptocurrency name exists in market data.

        Checks whether the provided cryptocurrency name is valid and available
        in the cryptocurrency market data sources.

        Args:
            coin_name (str): The full name of the cryptocurrency to validate.

        Returns:
            dict: A dictionary containing validation result with the following structure:
                {"is_valid": bool} - True if name is valid, False otherwise
                If error occurs: {"error": str}

        Example:
            >>> crypto = CryptocurrencyInsights()
            >>> result = crypto.is_valid_name("Bitcoin")
            >>> print(result["is_valid"])  # True or False
        """
        try:
            response = requests.get(f"{self.base_url}/coins/markets", 
                                  params={"vs_currency": "usd", "ids": coin_name.lower()})
            data = response.json()
            
            return json.dumps({"is_valid": len(data) > 0}, indent=2)
            
        except requests.RequestException:
            return json.dumps({"error": "Unable to validate coin name. Please check your connection and try again."}, indent=2)
        except Exception:
            return json.dumps({"error": "An unexpected error occurred while validating the coin name."}, indent=2)

    def get_current_price(self, coin_name: str = None, coin_symbol: str = None) -> dict:
        """
        Retrieve the current price of a cryptocurrency in USD.

        Fetches the real-time price of a cryptocurrency from market data
        using either the coin name or symbol. The price is returned in USD.

        Args:
            coin_name (str, optional): Full name of the cryptocurrency (e.g., "Bitcoin").
            coin_symbol (str, optional): Ticker symbol of the cryptocurrency (e.g., "BTC").

        Returns:
            dict: A dictionary containing price information with the following structure:
                {"current_price_usd": float} - Current price in USD
                If error occurs: {"error": str}

        Example:
            >>> crypto = CryptocurrencyInsights()
            >>> result = crypto.get_current_price(coin_symbol="BTC")
            >>> print(f"Bitcoin price: ${result['current_price_usd']:.2f}")
        """
        if not coin_name and not coin_symbol:
            return json.dumps({"error": "You must provide either 'coin_name' or 'coin_symbol'."}, indent=2)

        try:
            details = self.coin_details(coin_name, coin_symbol)
            
            if "error" in details:
                return json.dumps({"error": details["error"]}, indent=2)
            
            current_price = details["data"].get("current_price_usd", 0.0)
            return json.dumps({"current_price_usd": current_price}, indent=2)

        except Exception:
            return json.dumps({"error": "An unexpected error occurred while fetching current price."}, indent=2)

    def __str__(self) -> str:
        return "CryptocurrencyInsights Class for Market Analysis"

    def __repr__(self) -> str:
        return "CryptocurrencyInsights()"


class CurrencyConverter:
    """
    A class to perform real-time currency conversion and exchange rate operations.

    This class provides functionality to convert currency amounts between different currencies, 
    fetch exchange rates, and list supported currencies. It handles all currency-related
    operations with robust error handling and comprehensive data validation.

    Attributes:
        base_url (str): The base URL endpoint for currency exchange operations.

    Methods:
        convert(from_currency, to_currency, amount): Converts amount between currencies.
        exchange_rate(from_currency, to_currency): Retrieves exchange rate between currencies.
        supported_currencies(): Returns list of supported currency codes.
        exchange_rate_for_base_currency(base_currency): Gets all rates from base currency.
    """

    def __init__(self):
        """
        Initialize the CurrencyConverter class.
        
        Sets up the base URL for currency exchange operations and prepares
        the instance for making currency conversion requests.
        """
        self.base_url = "https://v6.exchangerate-api.com/v6/"

    def convert(self, from_currency: str, to_currency: str, amount: float) -> dict:
        """
        Convert a specified amount from one currency to another.

        Performs real-time currency conversion using current exchange rates
        to convert the specified amount from source to target currency.

        Args:
            from_currency (str): The source currency code (e.g., "USD").
            to_currency (str): The target currency code (e.g., "EUR").
            amount (float): The amount to convert.

        Returns:
            dict: A dictionary containing conversion result with the following structure:
                {"converted_amount": float} - The converted amount
                If error occurs: {"error": str}

        Example:
            >>> converter = CurrencyConverter()
            >>> result = converter.convert("USD", "EUR", 100)
            >>> print(f"Converted amount: {result['converted_amount']:.2f}")
        """
        try:
            if not isinstance(from_currency, str) or not isinstance(to_currency, str):
                return {"error": "Currency codes must be strings."}
            if not isinstance(amount, (int, float)):
                return {"error": "Amount must be a number."}

            url = f"{self.base_url}{currency_api}/pair/{from_currency}/{to_currency}/{amount}"
            response = requests.get(url)
            data = response.json()
            
            if "conversion_result" not in data:
                return {"error": "Invalid currency codes or service unavailable."}

            return {"converted_amount": data["conversion_result"]}

        except requests.RequestException:
            return {"error": "Unable to perform currency conversion. Please check your connection and try again."}
        except Exception:
            return {"error": "An unexpected error occurred during currency conversion."}

    def exchange_rate(self, from_currency: str, to_currency: str) -> dict:
        """
        Retrieve the current exchange rate between two currencies.

        Fetches the real-time exchange rate from the source currency to the
        target currency for conversion calculations.

        Args:
            from_currency (str): The base currency code (e.g., "USD").
            to_currency (str): The target currency code (e.g., "EUR").

        Returns:
            dict: A dictionary containing exchange rate with the following structure:
                {"exchange_rate": float} - Current exchange rate
                If error occurs: {"error": str}

        Example:
            >>> converter = CurrencyConverter()
            >>> result = converter.exchange_rate("USD", "EUR")
            >>> print(f"Exchange rate: {result['exchange_rate']:.4f}")
        """
        try:
            if not isinstance(from_currency, str) or not isinstance(to_currency, str):
                return {"error": "Currency codes must be strings."}

            url = f"{self.base_url}{currency_api}/pair/{from_currency}/{to_currency}"
            response = requests.get(url)
            data = response.json()
            
            if "conversion_rate" not in data:
                return {"error": "Invalid currency codes or service unavailable."}

            return {"exchange_rate": data["conversion_rate"]}

        except requests.RequestException:
            return {"error": "Unable to fetch exchange rate. Please check your connection and try again."}
        except Exception:
            return {"error": "An unexpected error occurred while fetching exchange rate."}

    def supported_currencies(self) -> dict:
        """
        Retrieve a list of all supported currency codes and their descriptions.

        Provides comprehensive list of all available currencies that can be
        used for conversion operations along with their full names.

        Args:
            None

        Returns:
            dict: A dictionary containing supported currencies with the following structure:
                {"currencies": list} - List of currency dictionaries with code and name
                If error occurs: {"error": str}

        Example:
            >>> converter = CurrencyConverter()
            >>> result = converter.supported_currencies()
            >>> print(len(result["currencies"]))  # Number of supported currencies
        """
        try:
            url = f"{self.base_url}{currency_api}/codes"
            response = requests.get(url)
            data = response.json()
            
            if "supported_codes" not in data:
                return {"error": "Unable to retrieve supported currencies."}

            currencies = [{"code": code[0], "name": code[1]} for code in data["supported_codes"]]
            return {"currencies": currencies}

        except requests.RequestException:
            return {"error": "Unable to fetch supported currencies. Please check your connection and try again."}
        except Exception:
            return {"error": "An unexpected error occurred while retrieving supported currencies."}

    def exchange_rate_for_base_currency(self, base_currency: str) -> dict:
        """
        Retrieve exchange rates from a base currency to all supported currencies.

        Provides comprehensive exchange rate data from the specified base currency
        to all other available currencies in a single response.

        Args:
            base_currency (str): The base currency code (e.g., "USD").

        Returns:
            dict: A dictionary containing all exchange rates with the following structure:
                {"rates": dict} - Dictionary of currency codes mapped to exchange rates
                If error occurs: {"error": str}

        Example:
            >>> converter = CurrencyConverter()
            >>> result = converter.exchange_rate_for_base_currency("USD")
            >>> print(result["rates"]["EUR"])  # USD to EUR rate
        """
        try:
            if not isinstance(base_currency, str):
                return {"error": "Base currency must be a string."}

            url = f"{self.base_url}{currency_api}/latest/{base_currency}"
            response = requests.get(url)
            data = response.json()
            
            if "conversion_rates" not in data:
                return {"error": "Invalid base currency or service unavailable."}

            return {"rates": data["conversion_rates"]}

        except requests.RequestException:
            return {"error": "Unable to fetch exchange rates. Please check your connection and try again."}
        except Exception:
            return {"error": "An unexpected error occurred while retrieving exchange rates."}

    def __str__(self):
        return "CurrencyConverter Class for Currency Exchange"

    def __repr__(self):
        return "CurrencyConverter()"