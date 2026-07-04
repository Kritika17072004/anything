import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Yahoo Finance Stock Dashboard")

st.sidebar.header("Settings")

ticker = st.sidebar.text_input(
    "Ticker Symbol",
    value="AAPL"
).upper().strip()

period = st.sidebar.selectbox(
    "Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    ]
)


@st.cache_data(show_spinner=False)
def load_data(symbol, period):
    df = yf.download(
        symbol,
        period=period,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        return None

    # Fix for latest yfinance MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    return df


with st.spinner("Fetching data..."):
    data = load_data(ticker, period)

if data is None:
    st.error("No data found. Please check the ticker symbol.")
    st.stop()

required_columns = ["Date", "Close"]

for col in required_columns:
    if col not in data.columns:
        st.error(f"Missing required column: {col}")
        st.write(data.columns.tolist())
        st.stop()

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data["Date"],
        y=data["Close"],
        mode="lines",
        name="Close Price"
    )
)

fig.update_layout(
    title=f"{ticker} Closing Price ({period})",
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

latest = data.iloc[-1]
previous = data.iloc[-2] if len(data) > 1 else latest

change = latest["Close"] - previous["Close"]
percent = (change / previous["Close"]) * 100 if previous["Close"] != 0 else 0

c1, c2, c3 = st.columns(3)

c1.metric(
    "Latest Close",
    f"${latest['Close']:.2f}"
)

c2.metric(
    "Daily Change",
    f"{change:.2f}",
    f"{percent:.2f}%"
)

if "Volume" in data.columns:
    c3.metric(
        "Volume",
        f"{int(latest['Volume']):,}"
    )
else:
    c3.metric(
        "Volume",
        "N/A"
    )

st.subheader("Historical Data")

st.dataframe(
    data,
    use_container_width=True
)
