# In finsolvepy/information.py
import pandas as pd
from finsolvepy.database.company_symbol_dict import company_dict  # Update this line
import json
import requests
import os

from dotenv import load_dotenv

# Load the .env file
load_dotenv()
market_api=os.getenv('ALPHA_VANTAGE_API_KEY')
currency_api=os.getenv('CURRENCY_API_KEY')

class StockInsights():
    """
    A class to provide insights and detailed information about stocks and indices in the market.

    This class allows users to fetch detailed stock information, validate stock symbols and indices,
    and retrieve descriptions for various market indices. It utilizes data from CSV files and an external 
    API to gather relevant stock and index information.

    Attributes:
    -----------
    stock : pandas.DataFrame
        A DataFrame containing stock information loaded from 'database/complete_data.csv'.
    index : pandas.DataFrame
        A DataFrame containing index descriptions loaded from 'database/indices_descriptions.csv'.

    Methods:
    --------
    stock_detail(symbol: str) -> dict:
        Fetches detailed information for a specified stock symbol, including market cap, company name,
        and financial metrics.

    index_lists() -> dict:
        Returns a list of all indices present in the Indian and US markets.

    index_description(index: str) -> dict:
        Retrieves a description of a specified market index.

    is_valid_symbol(symbol: str) -> bool:
        Checks if a provided stock symbol is valid by verifying its presence in market data.

    is_valid_index(index: str) -> bool:
        Checks if a provided index is valid by verifying its presence in the index data.
    """
    def __init__(self) -> None:
        # Get the directory of the current file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.stock = pd.read_csv(os.path.join(base_dir, 'database', 'complete_data.csv'))
        self.index = pd.read_csv(os.path.join(base_dir, 'database', 'indices_descriptions.csv'))

    def stock_detail(self, symbol: str) -> dict:
        """
        Fetches detailed stock information for a given stock symbol.
        
        Args:
            symbol (str): The stock symbol for which details are to be retrieved.
        
        Returns:
            dict: A dictionary containing stock information if found, or an error message if not.
        
        Raises:
            ValueError: If the stock symbol does not exist in the market.
        """
        try:
            # Check if the symbol exists in the DataFrame
            us_response=requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={market_api}")
            if symbol not in self.stock['symbol'].values and us_response.text == "{}":
                raise ValueError(f"Information for '{symbol}' is not available or the symbol is invalid.")
            
            if symbol not in self.stock['symbol'].values and us_response.text != "{}":
                stock=us_response.json()
                data={
                    'symbol':stock['Symbol'],
                    'company': stock['Name'],
                    'market_cap':str(stock['MarketCapitalization'])+" USD",
                    'about':stock['Description'],
                    'curr_market_price': "$"+str(float(stock['PERatio']) * float(stock['EPS'])),
                    'book_value':stock['PriceToBookRatio'],
                    'divident':stock['DividendYield'],
                    'roce':( float(stock['EBITDA']) / float(stock['MarketCapitalization'])) * 100,
                    'roe':stock['ReturnOnEquityTTM'],
                    'face_value': None
                }
                return json.dumps(data, indent=2)
            
            # Fetch the row where 'symbol' matches the input
            stock = self.stock.loc[self.stock['symbol'] == symbol]
            
            # If the stock symbol exists but the DataFrame is empty (just in case)
            if stock.empty:
                raise ValueError(f"No information available for the stock symbol '{symbol}'.")

            # Extract values and handle potential missing data in each column
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

            # Convert the dictionary to a JSON formatted string
            return json.dumps(stock_info, indent=4)

        except ValueError as ve:
            return {"error": str(ve)}
        
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}



    def index_lists(self) -> dict:
        """
        Returns all index's present in Indian and US market.

        Returns:
            dict: A dictionary containing the 'Index' data as a list or an error message.

        Raises:
            KeyError: If the 'Index' column is not found in the DataFrame.
            ValueError: If the index data cannot be serialized to JSON.
        """
        try:
            # Check if 'Index' exists in the DataFrame
            if 'Index' not in self.index.columns:
                raise KeyError("'Index' column not found in the DataFrame.")

            index = self.index['Index'].values.tolist()  
            return json.dumps({'Index': index}, indent=2)
        
        except KeyError as e:
            return json.dumps({'error': str(e)}, indent=2)
        except ValueError as e:
            return json.dumps({'error': f'Error serializing to JSON: {str(e)}'}, indent=2)
        except Exception as e:
            return json.dumps({'error': f'An unexpected error occurred: {str(e)}'}, indent=2)

    def index_description(self, index: str) -> dict:
        """
        Retrieve the description of a given index from the stock market.

        Args:
            index (str): The index for which to retrieve information.

        Returns:
            dict: A dictionary containing the index details or an error message.

        Raises:
            ValueError: If the provided index is not a string.
            KeyError: If the necessary columns are not found in the index DataFrame.
        """
        try:
            # Check if the index is a string
            if not isinstance(index, str):
                raise ValueError("The argument should be a string.")
            
            # Check if the index exists in the DataFrame
            if index not in self.index['Index'].values:
                return {"error": f"Information for '{index}' is not available or the index is invalid."}
            
            # Retrieve information for the valid index
            info = self.index[self.index['Index'] == index]

            # Prepare the data to return
            data = {
                "Index": info['Index'].values[0],
                "Region": info['Exchange'].values[0],
                "Description": info['Description'].values[0]
            }
            return json.dumps(data, indent=2)

        except KeyError as e:
            return {"error": f"Column not found: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}


    def is_valid_symbol(self, symbol: str) -> bool:
        """
        Check if the provided stock symbol is valid by verifying its presence
        in the Indian and US market data.

        Args:
            symbol (str): The stock symbol to validate.

        Returns:
            bool: True if the symbol is valid (exists in the stock market data), False otherwise.

        Raises:
            ValueError: If the provided symbol is not a string.
            requests.RequestException: If the API request fails.
        """
        try:
            # Check if the symbol is a string
            if not isinstance(symbol, str):
                raise ValueError("The provided symbol must be a string.")

            # Check if the symbol exists in the DataFrame
            if symbol in self.stock['symbol'].values:
                return True

            # Query the external API for symbol validation
            response = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api}')
            response.raise_for_status()  # Raise an error for HTTP requests that return an unsuccessful status code

            # Check if the response contains valid data
            if response.text != "{}":
                return True
            
            return False

        except ValueError as e:
            return json.dumps({'error': str(e)}, indent=2)
        except requests.RequestException as e:
            return json.dumps({'error': f'API request failed: {str(e)}'}, indent=2)
        except Exception as e:
            return json.dumps({'error': f'An unexpected error occurred: {str(e)}'}, indent=2)
        
    def is_valid_index(self, index: str) -> bool:
        """
        Check if the provided index is valid by verifying its presence in the market data.

        Args:
            index (str): The index to validate.

        Returns:
            bool: True if the index is valid (exists in the index DataFrame), False otherwise.

        Raises:
            ValueError: If the provided index is not a string.
            KeyError: If the 'Index' column is not found in the index DataFrame.
        """
        try:
            # Check if the index is a string
            if not isinstance(index, str):
                raise ValueError("The provided index must be a string.")

            # Check if 'Index' exists in the DataFrame
            if 'Index' not in self.index.columns:
                raise KeyError("'Index' column not found in the index DataFrame.")

            return index in self.index['Index'].values

        except ValueError as e:
            return json.dumps({'error': str(e)}, indent=2)
        except KeyError as e:
            return json.dumps({'error': str(e)}, indent=2)
        except Exception as e:
            return json.dumps({'error': f'An unexpected error occurred: {str(e)}'}, indent=2)
    
    def __str__(self):
        return "StockInsights Class for Market Analysis"

    def __repr__(self):
        return "StockInsights()"


class CurrencyConverter:
    """
        A class to perform real-time currency conversion and exchange rate lookups using the ExchangeRate-API.

        This class provides functionality to convert currency amounts between different currencies, 
        fetch exchange rates, and list supported currencies via RESTful API calls to the ExchangeRate-API.

        Attributes
        ----------
        base_url : str
            The base URL of the ExchangeRate-API endpoint.
        api_key : str
            The API key used for authenticating requests to the ExchangeRate-API.

        Methods
        -------
        convert(from_currency: str, to_currency: str, amount: float) -> float:
            Converts a specified amount from one currency to another.

        exchange_rate(from_currency: str, to_currency: str) -> float:
            Retrieves the current exchange rate between two given currencies.

        supported_currencies() -> list:
            Returns a list of supported currency codes and their full names.

        exchange_rate_for_base_currency(base_currency: str) -> dict:
            Retrieves all exchange rates from a given base currency to others.

        __str__() -> str:
            Returns a human-readable string representation of the CurrencyConverter instance.

        __repr__() -> str:
            Returns a developer-friendly representation of the CurrencyConverter instance.
    """


    def __init__(self):
        """
        Initializes the CurrencyConverter with the base API URL and API key.
        """
        self.base_url = "https://v6.exchangerate-api.com/v6/"
        self.api_key = currency_api

    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        """
        Converts a specified amount from one currency to another.

        Args:
            from_currency (str): The source currency code (e.g., "USD").
            to_currency (str): The target currency code (e.g., "INR").
            amount (float): The amount to convert.

        Returns:
            float: The converted amount in the target currency.

        Raises:
            ValueError: If the input types are invalid or API response is incorrect.
            requests.RequestException: If the API request fails.
        """
        try:
            if not isinstance(from_currency, str) or not isinstance(to_currency, str):
                raise ValueError("Currency codes must be strings.")
            if not isinstance(amount, (int, float)):
                raise ValueError("Amount must be a number.")

            url = f"{self.base_url}{self.api_key}/pair/{from_currency}/{to_currency}/{amount}"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if "conversion_rate" not in data:
                raise ValueError("Invalid API response")

            return data["conversion_result"]

        except ValueError as e:
            return json.dumps({'error': str(e)}, indent=2)
        except requests.RequestException as e:
            sanitized_msg = str(e).replace(self.api_key, "[API_KEY]")
            return json.dumps({'error': f'API request failed: {sanitized_msg}'}, indent=2)
        except Exception as e:
            return json.dumps({'error': f'An unexpected error occurred: {str(e)}'}, indent=2)

    def exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Retrieves the exchange rate between two currencies.

        Args:
            from_currency (str): The base currency code.
            to_currency (str): The target currency code.

        Returns:
            float: The current exchange rate from base to target currency.

        Raises:
            ValueError: If the input types are invalid or API response is incorrect.
            requests.RequestException: If the API request fails.
        """
        try:
            if not isinstance(from_currency, str) or not isinstance(to_currency, str):
                raise ValueError("Currency codes must be strings.")

            url = f"{self.base_url}{self.api_key}/pair/{from_currency}/{to_currency}"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if "conversion_rate" not in data:
                raise ValueError("Invalid API response")

            return data["conversion_rate"]

        except ValueError as e:
            return json.dumps({'error': str(e)}, indent=2)
        except requests.RequestException as e:
            sanitized_msg = str(e).replace(self.api_key, "[API_KEY]")
            return json.dumps({'error': f'API request failed: {sanitized_msg}'}, indent=2)
        except Exception as e:
            return json.dumps({'error': f'An unexpected error occurred: {str(e)}'}, indent=2)

    def supported_currencies(self) -> list:
        """
        Retrieves a list of all supported currency codes and their full names.

        Returns:
            list: A list of dictionaries mapping currency codes to full names.

        Raises:
            requests.RequestException: If the API request fails.
        """
        try:
            url = f"{self.base_url}{self.api_key}/codes"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if "supported_codes" not in data:
                raise ValueError("Invalid API response")

            return [{code[0]: code[1]} for code in data["supported_codes"]]

        except requests.RequestException as e:
            sanitized_msg = str(e).replace(self.api_key, "[API_KEY]")
            return json.dumps({'error': f'API request failed: {sanitized_msg}'}, indent=2)
        except Exception as e:
            return json.dumps({'error': f'An unexpected error occurred: {str(e)}'}, indent=2)

    def exchange_rate_for_base_currency(self, base_currency: str) -> dict:
        """
        Retrieves exchange rates from a base currency to all other supported currencies.

        Args:
            base_currency (str): The base currency code (e.g., "USD").

        Returns:
            dict: A dictionary of currency codes mapped to exchange rates.

        Raises:
            ValueError: If the base currency is not a string or API response is invalid.
            requests.RequestException: If the API request fails.
        """
        try:
            if not isinstance(base_currency, str):
                raise ValueError("Base currency must be a string.")

            url = f"{self.base_url}{self.api_key}/latest/{base_currency}"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if "conversion_rates" not in data:
                raise ValueError("Invalid API response")

            return data["conversion_rates"]

        except ValueError as e:
            return json.dumps({'error': str(e)}, indent=2)
        except requests.RequestException as e:
            sanitized_msg = str(e).replace(self.api_key, "[API_KEY]")
            return json.dumps({'error': f'API request failed: {sanitized_msg}'}, indent=2)
        except Exception as e:
            return json.dumps({'error': f'An unexpected error occurred: {str(e)}'}, indent=2)

    def __str__(self):
        """
        Returns a human-readable string representation of the CurrencyConverter class.

        Returns:
            str: Description of the class.
        """
        return "CurrencyConverter Class for Currency Exchange"

    def __repr__(self):
        """
        Returns an unambiguous string representation of the CurrencyConverter object.

        Returns:
            str: Developer-friendly representation.
        """
        return "CurrencyConverter()"
