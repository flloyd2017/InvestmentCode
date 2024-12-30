import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd

def calculate_put_returns(strike_price, premium, current_price, contract_size=100):
    """
    Calculate returns of a cash-secured put given the inputs.

    Parameters:
        strike_price (float): The strike price of the put option.
        premium (float): The premium received for the option.
        current_price (float): The current stock price.
        contract_size (int): Number of shares per option contract (usually 100).

    Returns:
        dict: Contains data for graphing returns.
    """
    # Generate a range of stock prices for visualization
    prices = np.linspace(current_price * 0.5, current_price * 1.5, 100)

    # Calculate profit/loss for each price point
    profit_loss = np.where(
        prices >= strike_price,
        premium * contract_size,
        (prices - strike_price + premium) * contract_size
    )

    return {
        "prices": prices,
        "profit_loss": profit_loss
    }

def calculate_call_returns(strike_price, premium, current_price, contract_size=100):
    """
    Calculate returns of a covered call given the inputs.

    Parameters:
        strike_price (float): The strike price of the call option.
        premium (float): The premium received for the option.
        current_price (float): The current stock price.
        contract_size (int): Number of shares per option contract (usually 100).

    Returns:
        dict: Contains data for graphing returns.
    """
    # Generate a range of stock prices for visualization
    prices = np.linspace(current_price * 0.5, current_price * 1.5, 100)

    # Calculate profit/loss for each price point
    profit_loss = np.where(
        prices <= strike_price,
        premium * contract_size,
        (strike_price - prices + premium) * contract_size
    )

    return {
        "prices": prices,
        "profit_loss": profit_loss
    }

def graph_returns(prices, profit_loss, current_price, strike_price, premium, title):
    """
    Plot the profit/loss graph for options with additional details.

    Parameters:
        prices (np.array): Array of stock prices.
        profit_loss (np.array): Array of profit/loss values.
        current_price (float): The current stock price to mark on the graph.
        strike_price (float): The strike price of the option.
        premium (float): The premium received for the option.
        title (str): Title of the graph.
    """
    break_even = strike_price - premium
    current_profit_loss = np.interp(current_price, prices, profit_loss)

    plt.figure(figsize=(10, 6))
    plt.plot(prices, profit_loss, label="Profit/Loss", color="blue")
    plt.axhline(0, color="black", linewidth=1.5, label="Zero Line")
    plt.axhline(premium * 100, color="green", linestyle="--", label="Premium Received")
    plt.axvline(current_price, color="red", linestyle="--", linewidth=1.5, label="Current Stock Price")
    plt.fill_between(prices, profit_loss, where=(prices >= break_even), color='green', alpha=0.1, label="Profit Zone")
    plt.fill_between(prices, profit_loss, where=(prices < break_even), color='red', alpha=0.1, label="Loss Zone")
    plt.scatter([current_price], [current_profit_loss], color="red", label="Current Price", zorder=5)
    plt.scatter([break_even], [0], color="orange", label="Break-even", zorder=5)

    plt.title(title)
    plt.xlabel("Stock Price ($)")
    plt.ylabel("Profit/Loss ($)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Streamlit app
def main():
    st.title("Options Returns Calculator")

    # Option type selection
    option_type = st.selectbox("Select Option Type", ["Cash-Secured Put", "Covered Call"])

    # Inputs from user
    strike_price = st.number_input("Strike Price ($)", min_value=1.0, step=0.1)
    premium = st.number_input("Premium Received ($)", min_value=0.1, step=0.1)
    current_price = st.number_input("Current Stock Price ($)", min_value=1.0, step=0.1)

    if st.button("Calculate Returns"):
        if option_type == "Cash-Secured Put":
            results = calculate_put_returns(strike_price, premium, current_price)
            title = "Cash-Secured Put Returns"
        else:
            results = calculate_call_returns(strike_price, premium, current_price)
            title = "Covered Call Returns"

        st.write("### Profit/Loss Data")
        st.line_chart(
            pd.DataFrame({"Price": results["prices"], "Profit/Loss": results["profit_loss"]}).set_index("Price")
        )

        # Graph the returns with the current price marked and additional details
        graph_returns(results["prices"], results["profit_loss"], current_price, strike_price, premium, title)

if __name__ == "__main__":
    main()
