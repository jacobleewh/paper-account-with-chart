import os
import requests
import matplotlib.pyplot as plt
import datetime as dt

API_KEY = 'B2HBUBP8HW31O97S'

def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    try:
        price = float(data['Global Quote']['05. price'])
        return price
    except KeyError:
        return None

portfolio = {
    "cash": 10000.00,
    "stocks": {}
}

def buy_stock(symbol, quantity, price):
    total_cost = quantity * price
    if portfolio["cash"] >= total_cost:
        portfolio["cash"] -= total_cost
        if symbol in portfolio["stocks"]:
            portfolio["stocks"][symbol] += quantity
        else:
            portfolio["stocks"][symbol] = quantity
        return True
    else:
        return False

def sell_stock(symbol, quantity, price):
    if symbol in portfolio["stocks"] and portfolio["stocks"][symbol] >= quantity:
        portfolio["stocks"][symbol] -= quantity
        portfolio["cash"] += quantity * price
        if portfolio["stocks"][symbol] == 0:
            del portfolio["stocks"][symbol]
        return True
    else:
        return False

def get_portfolio():
    return portfolio

def display_menu():
    print("\nStock Broker App Menu")
    print("1. View Stock Prices")
    print("2. Buy Stocks")
    print("3. Sell Stocks")
    print("4. View Portfolio")
    print("5. Exit")

def handle_user_input():
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            ssymbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
            price = get_stock_price(ssymbol)
            if price:
                print(f"The current price of {ssymbol} is ${price:.2f}")

                # Get the Alpha Vantage API key from environment variables
                api_key = os.getenv('ALPHA_VANTAGE_API_KEY')


                # Function to fetch historical stock data from Alpha Vantage
                def get_stock_data(symbol, api_key):
                    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
                    response = requests.get(url)
                    data = response.json()
                    return data['Time Series (Daily)']

                # Fetch historical data
                stock_data = get_stock_data(ssymbol, api_key)

                # Extract dates and closing prices
                dates = []
                closing_prices = []

                for date, data in stock_data.items():
                    dates.append(dt.datetime.strptime(date, '%Y-%m-%d').date())
                    closing_prices.append(float(data['4. close']))

                # Sort the dates and closing prices (Alpha Vantage returns data in descending order)
                dates.reverse()
                closing_prices.reverse()

                # Plot the stock data
                plt.figure(figsize=(10, 5))
                plt.plot(dates, closing_prices, marker='o', linestyle='-', color='b')
                plt.title(f'{ssymbol} Stock Prices')
                plt.xlabel('Date')
                plt.ylabel('Closing Price (USD)')
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

            else:
                print(f"Stock symbol {symbol} not found.")

        elif choice == '2':
            symbol = input("Enter the stock symbol to buy (e.g., AAPL): ").upper()
            quantity = int(input("Enter the quantity to buy: "))
            price = get_stock_price(symbol)
            if price:
                success = buy_stock(symbol, quantity, price)
                if success:
                    print(f"Successfully bought {quantity} shares of {symbol} at ${price:.2f} each.")
                else:
                    print("Insufficient cash to complete the transaction.")
            else:
                print(f"Stock symbol {symbol} not found.")

        elif choice == '3':
            symbol = input("Enter the stock symbol to sell (e.g., AAPL): ").upper()
            quantity = int(input("Enter the quantity to sell: "))
            price = get_stock_price(symbol)
            if price:
                success = sell_stock(symbol, quantity, price)
                if success:
                    print(f"Successfully sold {quantity} shares of {symbol} at ${price:.2f} each.")
                else:
                    print("Insufficient stock quantity to complete the transaction.")
            else:
                print(f"Stock symbol {symbol} not found.")

        elif choice == '4':
            portfolio = get_portfolio()
            print("\nPortfolio Summary:")
            print(f"Cash: ${portfolio['cash']:.2f}")
            if portfolio["stocks"]:
                for symbol, quantity in portfolio["stocks"].items():
                    print(f"{symbol}: {quantity} shares")
            else:
                print("No stocks owned.")

        elif choice == '5':
            print("Thank you for using the Stock Broker App. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

#from broker import handle_user_input

def main():
    print("Welcome to the Stock Broker App!")
    handle_user_input()

if __name__ == "__main__":
    main()