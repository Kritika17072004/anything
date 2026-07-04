import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(
    page_title="Stock Price Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Price Dashboard")
st.write("Fetch stock market data using Yahoo Finance (yfinance).")

# Sidebar
ticker = st.sidebar.text_input(
    "Enter Stock Ticker",
    value="AAPL"
).upper()

period = st.sidebar.selectbox(
    "Select Time Period",
    (
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "max"
    ),
    format_func=lambda x: {
        "1mo": "1 Month",
        "3mo": "3 Months",
        "6mo": "6 Months",
        "1y": "1 Year",
        "2y": "2 Years",
        "5y": "5 Years",
        "max": "Max"
    }[x]
)

# Download data
data = yf.download(
    ticker,
    period=period,
    progress=False,
    auto_adjust=True
)

if data.empty:
    st.error("No data found. Please check the ticker symbol.")
    st.stop()

st.subheader(f"{ticker} Closing Price")

fig = px.line(
    data,
    x=data.index,
    y="Close",
    title=f"{ticker} Stock Price ({period})"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Display latest metrics
latest = data.iloc[-1]
previous = data.iloc[-2] if len(data) > 1 else latest

change = latest["Close"] - previous["Close"]
pct_change = (change / previous["Close"]) * 100 if previous["Close"] != 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "Latest Close",
    f"${latest['Close']:.2f}"
)

col2.metric(
    "Daily Change",
    f"{change:.2f}",
    f"{pct_change:.2f}%"
)

col3.metric(
    "Volume",
    f"{int(latest['Volume']):,}"
)

st.subheader("Historical Data")
st.dataframe(data)
