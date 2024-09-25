from typing import Union

class Metrics():
    """
    A class for financial metrics and calculations related to investments and company performance.

    This class provides static methods to calculate various financial metrics, including:

    1. **Years to Double Money**: Estimates the number of years required to double an investment based on the annual interest rate using the Rule of 72.
    
    2. **Years to Triple Money**: Estimates the number of years required to triple an investment based on the annual interest rate using the Rule of 114.
    
    3. **Earnings Per Share (EPS)**: Calculates the earnings available to each share of common stock.
    
    4. **Price to Earnings (P/E) Ratio**: Evaluates the company's current share price relative to its per-share earnings.
    
    5. **Return on Equity (ROE)**: Measures the profitability of a company in relation to shareholders' equity.
    
    6. **Return on Capital Employed (ROCE)**: Assesses a company's efficiency in generating profits from its capital.
    
    7. **Debt to Equity Ratio**: Indicates the proportion of equity and debt used to finance the company's assets.
    
    8. **Dividend Yield Percentage**: Calculates the annual dividend payment expressed as a percentage of the stock's current price.
    
    9. **Dividend Yield**: Determines the actual dividend amount paid based on the yield percentage.
    
    10. **Price to Book Ratio (P/B)**: Compares a company's market value to its book value, indicating how much investors are willing to pay for each dollar of net assets.

    Each method includes input validation and error handling to ensure that inputs are of the correct type and within acceptable ranges.
    """

    @staticmethod
    def years_to_double_money(interest: Union[int, float]) -> float:
        """
        Calculate the number of years required to double an investment based on the interest rate,
        using the Rule of 72.

        The Rule of 72 is a simple formula used to estimate the number of years required to 
        double the value of an investment at a given annual rate of return.

        Args:
            interest (Union[int, float]): The interest rate as a percentage (e.g., 5 for 5%).

        Returns:
            float: The estimated number of years to double the investment.

        Raises:
            ValueError: If the input interest is not of type `int` or `float`, or if the interest is <= 0.
        """
        if not isinstance(interest, (float, int)):
            raise ValueError("The argument should be either an integer or a float.")
        
        if interest <=0:
            raise ValueError("Interest rate must be greater than 0.")
        
        # The calculation using the Rule of 72
        return 72 / interest
    
    @staticmethod
    def years_to_triple_money(interest: Union[float,int]) -> float:
        """
        Calculate the number of years required to triple an investment based on the interest rate,
        using the Rule of 114.

        The Rule of 114 is a simple formula used to estimate the number of years required to 
        double the value of an investment at a given annual rate of return.

        Args:
            interest (Union[int, float]): The interest rate as a percentage (e.g., 5 for 5%).

        Returns:
            float: The estimated number of years to triple the investment.

        Raises:
            ValueError: If the input interest is not of type `int` or `float`, or if the interest is <= 0.
        """
        if not isinstance(interest,(float,int)):
            raise ValueError("The argument should be either an integer or a float.")
        if interest <=0:
            raise ValueError("The interest rate should greater than 0")
        
        # Calculation using rule 114
        return 114 / interest
    
    @staticmethod 
    def earnings_per_share(earnings: Union[float, int], no_of_shares: int) -> float:
        """
        Calculate the earnings per share (EPS) of a company.

        Args:
            earnings (Union[int, float]): The amount that the company earns after tax.
            no_of_shares (int): Total number of shares available in that company.

        Returns:
            float: The earnings per share of the company.

        Raises:
            ValueError: If the input earnings is not of type `int` or `float`, 
                    if input no_of_shares is not `int`, 
                    or if no_of_shares is not greater than 0.
        """

        if not isinstance(earnings, (float, int)):
            raise ValueError("The argument `earnings` should be either int or float.")

        if not isinstance(no_of_shares, int):
            raise ValueError("The argument `no_of_shares` should be an integer.")
        
        if no_of_shares <= 0:
            raise ValueError("The argument `no_of_shares` should be greater than 0.")
        
        return earnings / no_of_shares

    
    @staticmethod
    def pe_ratio(earnings: Union[float, int], no_of_shares: int, current_market_price: Union[float, int]) -> float:
        """
        Calculate the Price to Earnings (P/E) ratio of a company.

        Args:
            earnings (Union[int, float]): The amount that the company earns after tax.
            no_of_shares (int): Total number of shares available in that company.
            current_market_price (Union[int, float]): The current market price of the company stock.

        Returns:
            float: The Price to Earnings ratio of the company.

        Raises:
            ValueError: If the input earnings and current_market_price are not of type `int` or `float`, 
                        if no_of_shares is not an `int`, if current_market_price is not positive, 
                        or if no_of_shares is not greater than 0.
        """

        if not isinstance(earnings, (float, int)):
            raise ValueError("The argument `earnings` should be either int or float.")
        
        if not isinstance(current_market_price, (float, int)):
            raise ValueError("The argument `current_market_price` should be either int or float.")

        if not isinstance(no_of_shares, int):
            raise ValueError("The argument `no_of_shares` should be an integer.")
        
        if no_of_shares <= 0:
            raise ValueError("The argument `no_of_shares` should be greater than 0.")
        
        if current_market_price <= 0:
            raise ValueError("The argument `current_market_price` should be a positive number.")
        
        # Calculate earnings per share
        earnings_per_share = Metrics.earnings_per_share(earnings, no_of_shares)

        return current_market_price / earnings_per_share


    @staticmethod
    def roe_ratio(net_income: Union[float, int], shareholders_equity: Union[float, int]) -> float:
        """
        Calculate the Return on Equity (ROE) ratio of a company.

        Args:
            net_income (Union[int, float]): The net income of the company.
            shareholders_equity (Union[float, int]): Total equity held by the shareholders.

        Returns:
            float: The Return on Equity ratio of the company, expressed as a percentage.

        Raises:
            ValueError: If the input net_income and shareholders_equity are not of type `int` or `float`, 
                        or if shareholders_equity is not a positive number.
        """
        if not isinstance(net_income, (float, int)):
            raise ValueError("The argument `net_income` should be of type int or float.")

        if not isinstance(shareholders_equity, (float, int)):
            raise ValueError("The argument `shareholders_equity` should be of type int or float.")

        if shareholders_equity <= 0:
            raise ValueError("The argument `shareholders_equity` should be a positive number.")

        # Optionally check if net_income is negative
        if net_income < 0:
            raise ValueError("The argument `net_income` should be non-negative.")

        return (net_income / shareholders_equity) * 100

    
    @staticmethod
    def roce_ratio(ebit: Union[float, int], capital_employed: Union[float, int]) -> float:
        """
        Calculate the Return on Capital Employed (ROCE) ratio of a company.

        Args:
            ebit (Union[int, float]): Earnings before interest and tax.
            capital_employed (Union[float, int]): Total capital employed by the company.

        Returns:
            float: The Return on Capital Employed ratio of the company, expressed as a percentage.

        Raises:
            ValueError: If the input ebit and capital_employed are not of type `int` or `float`, 
                        or if capital_employed is not a positive number.
        """
        if not isinstance(ebit, (float, int)):
            raise ValueError("The argument `ebit` should be of type int or float.")

        if not isinstance(capital_employed, (float, int)):
            raise ValueError("The argument `capital_employed` should be of type int or float.")

        if capital_employed <= 0:
            raise ValueError("The argument `capital_employed` should be a positive number.")

        # Optionally check if ebit is negative
        if ebit < 0:
            raise ValueError("The argument `ebit` should be non-negative.")

        return (ebit / capital_employed) * 100

    
    @staticmethod
    def debt_to_equity(total_debt: Union[float, int], shareholders_equity: Union[float, int]) -> float:
        """
        Calculate the debt-to-equity ratio of a company.

        Args:
            total_debt (Union[int, float]): The total debt of the company.
            shareholders_equity (Union[float, int]): Total equity held by the shareholders.

        Returns:
            float: The debt-to-equity ratio of the company, expressed as a percentage.

        Raises:
            ValueError: If the input total_debt and shareholders_equity are not of type `int` or `float`,
                        or if shareholders_equity is not a positive number.
        """
        if not isinstance(total_debt, (float, int)):
            raise ValueError("The argument `total_debt` should be of type int or float.")
        
        if not isinstance(shareholders_equity, (float, int)):
            raise ValueError("The argument `shareholders_equity` should be of type int or float.")
        
        if shareholders_equity <= 0:
            raise ValueError("The argument `shareholders_equity` should be a positive number.")
        
        if total_debt < 0:
            raise ValueError("The argument `total_debt` should be non-negative.")
        
        return (total_debt / shareholders_equity) * 100

    
    @staticmethod
    def dividend_yield_percentage(annual_dividend: Union[float, int], price_per_share: Union[float, int]) -> float:
        """
        Calculate the dividend yield as a percentage of the company's share price.

        Args:
            annual_dividend (Union[int, float]): The annual dividend paid by the company.
            price_per_share (Union[float, int]): Price of a single share.

        Returns:
            float: The dividend yield percentage of the company.

        Raises:
            ValueError: If the input annual_dividend and price_per_share are not of type `int` or `float`,
                        or if price_per_share is not a positive number.
        """
        if not isinstance(annual_dividend, (float, int)):
            raise ValueError("The argument `annual_dividend` should be of type int or float.")
        
        if not isinstance(price_per_share, (float, int)):
            raise ValueError("The argument `price_per_share` should be of type int or float.")
        
        if price_per_share <= 0:
            raise ValueError("The argument `price_per_share` should be a positive number.")
        
        return (annual_dividend / price_per_share) * 100

    
    @staticmethod
    def dividend_yield(dividend_yield_percentage: Union[float, int], price_per_share: Union[float, int]) -> float:
        """
        Calculate the dividend yield of a company.

        Args:
            dividend_yield_percentage (Union[int, float]): The percentage of the share price that the company pays as a dividend.
            price_per_share (Union[float, int]): Price of a single share.

        Returns:
            float: The monetary value of the dividend yield of the company.

        Raises:
            ValueError: If the input dividend_yield_percentage and price_per_share are not of type `int` or `float`,
                        if price_per_share is not a positive number, or if dividend_yield_percentage is a negative number.
        """
        if not isinstance(dividend_yield_percentage, (float, int)):
            raise ValueError("The argument `dividend_yield_percentage` should be of type int or float.")
        
        if not isinstance(price_per_share, (float, int)):
            raise ValueError("The argument `price_per_share` should be of type int or float.")
        
        if price_per_share <= 0:
            raise ValueError("The argument `price_per_share` should be a positive number.")
        
        if dividend_yield_percentage < 0:
            raise ValueError("The argument `dividend_yield_percentage` should be a non-negative number.")
        
        return (price_per_share / 100) * dividend_yield_percentage

    
    @staticmethod
    def price_to_book_ratio(market_price: Union[float, int], book_value_per_share: Union[float, int]) -> float:
        """
        Calculate Price-to-Book Ratio (P/B).

        Args:
            market_price (Union[int, float]): The current market price per share.
            book_value_per_share (Union[int, float]): The book value per share (net asset value).

        Returns:
            float: The price-to-book ratio.
            
        Raises:
            ValueError: If the input market_price and book_value_per_share are not of type `int` or `float`,
                        or if book_value_per_share is not a positive number.
        """
        if not isinstance(market_price, (float, int)):
            raise ValueError("The argument `market_price` should be either int or float.")
        
        if not isinstance(book_value_per_share, (float, int)):
            raise ValueError("The argument `book_value_per_share` should be either int or float.")
        
        if book_value_per_share <= 0:
            raise ValueError("The argument `book_value_per_share` must be a positive number.")
        
        return market_price / book_value_per_share
    def __str__(self):
        return ("Metrics Class for Financial Calculations\n"
                "---------------------------------------------------\n"
                "This class provides static methods for various financial metrics:\n"
                "1. Years to Double Money\n"
                "2. Years to Triple Money\n"
                "3. Earnings Per Share (EPS)\n"
                "4. Price to Earnings (P/E) Ratio\n"
                "5. Return on Equity (ROE)\n"
                "6. Return on Capital Employed (ROCE)\n"
                "7. Debt to Equity Ratio\n"
                "8. Dividend Yield Percentage\n"
                "9. Dividend Yield\n"
                "10. Price to Book Ratio (P/B)\n")

    def __repr__(self):
        return "Metrics()"











        




