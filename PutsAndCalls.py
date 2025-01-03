import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd

def calculate_put_returns(strike_price, premium, current_price, contract_size):
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
    prices = np.linspace(current_price * 0.1, current_price * 2.0, 200)

    # Calculate profit/loss for each price point
    profit_loss = np.where(
        prices >= strike_price,
        premium * contract_size,
        (prices - (strike_price - premium)) * contract_size
    )

    return {
        "prices": prices,
        "profit_loss": profit_loss
    }

def calculate_call_returns(strike_price, premium, current_price, contract_size):
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
    prices = np.linspace(current_price * 0.5, current_price * 2.0, 200)

    # Calculate profit/loss for each price point
    profit_loss = np.where(
        prices < strike_price,
        (premium + (prices - current_price)) * contract_size,
        (premium + (strike_price - current_price)) * contract_size
    )

    return {
        "prices": prices,
        "profit_loss": profit_loss
    }

def graph_returns(prices, contract_size, profit_loss, current_price, strike_price, premium, title):
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
    current_profit_loss = np.interp(current_price, prices, profit_loss)

    # Calculate stock-only returns
    stock_returns = (prices - current_price) * 100*contract_size

    # Calculate break-even point
    break_even = strike_price - premium if title == "Cash-Secured Put Returns" else current_price - premium

    if title == "Covered Call Returns":
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(prices, profit_loss, label="Options Profit/Loss", color="blue")
        ax.plot(prices, stock_returns, label="Stock-Only Returns", color="purple", linestyle="--")
        ax.axhline(0, color="black", linewidth=1.5)
        ax.axvline(current_price, color="red", linestyle="--", linewidth=1.5, label="Current Stock Price")
        ax.axvline(strike_price, color="orange", linestyle="--", linewidth=1.5, label="Strike Price")
        ax.axvline(break_even, color="green", linestyle="--", linewidth=1.5)
        #ax.axvline(break_even, color="green", linestyle="--", linewidth=1.5, label="Break-Even Point")
        #ax.text(break_even, 0, f"Break-Even: {break_even:.2f}", color="green", fontsize=10, verticalalignment='bottom')
        ax.fill_between(prices, stock_returns, profit_loss, where=(stock_returns < profit_loss) & (profit_loss > 0), color='green', alpha=0.2, label="Nailed it")
        ax.fill_between(prices, stock_returns, profit_loss, where=(stock_returns > profit_loss), color='orange', alpha=0.2, label="Should've Just Held It")
        ax.fill_between(prices, profit_loss, 0, where=(profit_loss < 0), color='red', alpha=0.2, label="Should've Just Sold It")
        ax.scatter([current_price], [current_profit_loss], color="red", label=f"Current Price: {current_price:.2f}", zorder=5)
        ax.scatter(break_even, 0 , color="green", label=f"Break-Even: {break_even:.2f}", zorder=6)

    if title == "Cash-Secured Put Returns":
        # Calculate stock-only returns
        stock_returns = (prices - current_price) * 100  # Assuming 100 shares

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(prices, profit_loss, label="Options Profit/Loss", color="blue")
        ax.axhline(0, color="black", linewidth=1.5)
        ax.axvline(current_price, color="red", linestyle="--", linewidth=1.5)
        ax.axvline(strike_price, color="orange", linestyle="--", linewidth=1.5, label="Strike Price")
        ax.axvline(break_even, color="green", linestyle="--", linewidth=1.5)
        #ax.text(break_even, 0, f"{break_even:.2f}", color="green", fontsize=10, verticalalignment='bottom')
        ax.fill_between(prices, profit_loss, 0 , where=(profit_loss > 0), color='green', alpha=0.2, label="Profit Zone")
        ax.fill_between(prices, profit_loss, 0, where=(profit_loss < 0), color='red', alpha=0.2, label="Loss Zone")
        ax.scatter([current_price], [current_profit_loss], color="red", label=f"Current Price: {current_price:.2f}", zorder=5)
        ax.scatter(break_even, 0 , color="green", label=f"Break-Even: {break_even:.2f}", zorder=6)

    ax.set_title(title)
    ax.set_xlabel("Stock Price ($)")
    ax.set_ylabel("Profit/Loss ($)")
    ax.legend()
    ax.grid(True)

    return fig

# Streamlit app
def main():
    st.title("Options Returns Calculator")

    # Option type selection
    option_type = st.selectbox("Select Option Type", ["Cash-Secured Put", "Covered Call"])

    # Inputs from user
    contract_size = st.number_input("Number of Contracts ", min_value=1, step=1)
    strike_price = st.number_input("Strike Price ($)", min_value=1.0, step=0.1)
    premium = st.number_input("Premium Received ($)", min_value=0.1, step=0.1)
    current_price = st.number_input("Current Stock Price ($)", min_value=1.0, step=0.1)

    if st.button("Calculate Returns"):
        if option_type == "Cash-Secured Put":
            results = calculate_put_returns(strike_price, premium, current_price, contract_size*100)
            title = "Cash-Secured Put Returns"
        else:
            results = calculate_call_returns(strike_price, premium, current_price, contract_size*100)
            title = "Covered Call Returns"

        # Render the matplotlib graph in Streamlit
        fig = graph_returns(results["prices"], contract_size, results["profit_loss"], current_price, strike_price, premium, title)
        st.pyplot(fig)

        # Display Profit/Loss Data
        st.write("### Profit/Loss Data")
        df = pd.DataFrame({"Price": results["prices"], "Profit/Loss": results["profit_loss"]}).set_index("Price")
        st.write(df)

if __name__ == "__main__":
    main()
