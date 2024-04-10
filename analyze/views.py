from django.shortcuts import render
import talib as ta
import pandas as pd
import datetime as dt
import yfinance as yf
from icecream import ic
from numpy import sqrt
import pandas_datareader.data as web
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from stockvista import forms

ic.includeContext = True


def analyzer(request) -> render:
    df: pd.DataFrame = pd.DataFrame()
    context = dict()
    if request.method == "POST":
        if "file" in request.FILES:
            csvFile = request.FILES.get("file")
            df = pd.read_csv(csvFile)
            context["company_name"] = str(csvFile)
        elif "getData" in request.POST:  # Checking if the online form button is pressed
            ticker = request.POST.get("ticker")
            company_name = yf.Ticker(ticker).info.get("longName")
            df = getDataset(
                ticker=ticker,
                start=request.POST.get("startDate"),
                end=request.POST.get("endDate"),
            )
            df: pd.DataFrame = df
            context["company_name"] = company_name
        ctx = calcIns(df)

        # Changing Date Format for easier understanding: (YYYY-MM-DD => DD/MMM/YY)
        df["Date"] = pd.to_datetime(df.Date).dt.strftime("%d/%b/%y")

        context.update(
            {
                "exists": df.shape > (0, 0),
                "data": df[["Date", "Open", "Close", "High", "Low"]].tail(15),
            }
        )
        context.update(ctx)
        context.update(figures(df))
    return render(request, "result_render.html", context)


def analyze(request) -> render:
    form = forms.TickerInput()
    date_fields = forms.DateInput()
    csv_form = forms.CSVForm()
    context = {
        "active": "analyze",
        "TickerInput": form,
        "DateInput": date_fields,
        "csvForm": csv_form,
    }
    return render(request, "analyze.html", context)


def figures(df: pd.DataFrame) -> dict:
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%b/%y")

    line_chart = px.line(
        x=df["Date"],
        y=df["Close"],
        labels={"x": "Date", "y": "Price"},
    )
    line_chart.update_layout(
        height=600,
        title_text="Stock Prices",
        xaxis_title="Date",
        showlegend=True,
    )

    EMA_chart = go.Figure()
    EMA_chart.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Closing Prices",
            line=dict(color="blue"),
        )
    )
    EMA_chart.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["EMA"],
            mode="lines",
            name="EMA_chart",
            line=dict(color="orange"),
        )
    )
    EMA_chart.update_layout(
        title="Stock Prices with Exponential Moving Average (EMA)",
        xaxis_title="Date",
        yaxis_title="Stock Price",
        showlegend=True,
        height=500,
    )

    candleFig = go.Figure(
        data=go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Candlestick",
        ),
    )
    candleFig.update_layout(
        height=600,
        title_text="Candlestick Chart",
        xaxis_title="Date",
        showlegend=True,
    )

    candleSMA_chart = go.Figure()
    candleSMA_chart.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Candlestick",
        )
    )
    candleSMA_chart.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA"],
            mode="lines",
            name="SMA",
            line=dict(color="orange"),
        )
    )
    candleSMA_chart.update_layout(
        height=600,
        title_text="Candlestick Chart with SMA",
        xaxis_title="Date",
        showlegend=True,
    )

    macd_rsi_chart: go.Figure = make_subplots(
        rows=2, cols=1, shared_xaxes=True, subplot_titles=("MACD", "RSI")
    )
    macd_rsi_chart.add_trace(
        go.Scatter(x=df["Date"], y=df["MACD"], mode="lines", name="MACD"), row=1, col=1
    )
    macd_rsi_chart.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["RSI"],
            mode="lines",
            name="RSI",
            line=dict(color="orange"),
        ),
        row=2,
        col=1,
    )
    macd_rsi_chart.update_layout(
        height=600,
        title_text="MACD and RSI Charts",
        xaxis_title="Date",
        showlegend=False,
    )

    adx_atr_chart: go.Figure = make_subplots(
        rows=2, cols=1, shared_xaxes=True, subplot_titles=("ADX", "ATR")
    )
    adx_atr_chart.add_trace(
        go.Scatter(x=df["Date"], y=df["ADX"], mode="lines", name="ADX"), row=1, col=1
    )
    adx_atr_chart.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["ATR"],
            mode="lines",
            name="ATR",
            line=dict(color="green"),
        ),
        row=2,
        col=1,
    )
    adx_atr_chart.update_layout(
        height=600,
        title_text="ADX and ATR Charts",
        xaxis_title="Date",
        showlegend=False,
    )

    bollinger_chart = go.Figure()
    bollinger_chart.add_trace(
        go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Close")
    )
    bollinger_chart.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Upper Band"],
            mode="lines",
            name="Upper Band",
            line=dict(color="red"),
        )
    )
    bollinger_chart.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Lower Band"],
            mode="lines",
            name="Lower Band",
            line=dict(color="blue"),
        )
    )
    bollinger_chart.update_layout(
        height=600, title_text="Bollinger Bands", xaxis_title="Date", showlegend=True
    )

    roc_chart = go.Figure()
    roc_chart.add_trace(
        go.Scatter(
            x=df["Date"].dropna(axis=0),
            y=df["ROC"].dropna(axis=0),
            mode="lines",
            name="ROC",
        )
    )
    roc_chart.update_layout(
        height=600,
        title_text="Price Rate of Change (ROC)",
        xaxis_title="Date",
        showlegend=True,
    )

    vol_chart = go.Figure()
    vol_chart.add_trace(
        go.Bar(
            x=df["Date"],
            y=df["Volume"].dropna(),
            name="Volume",
            marker=dict(color="purple"),
        )
    )
    vol_chart.update_layout(
        height=400,
        title_text="Volume Chart",
        xaxis_title="Date",
        yaxis_title="Volume",
        showlegend=True,
    )

    voltty = go.Figure()

    # Historical Volatility
    voltty.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Volatility"],
            mode="lines",
            name="Historical Volatility",
            line=dict(color="purple"),
        )
    )

    # Update layout
    voltty.update_layout(
        title="Historical Volatility of Stock",
        xaxis_title="Date",
        yaxis_title="Volatility",
        showlegend=True,
        height=500,
    )

    return {
        "line": line_chart.to_html(),
        "ema": EMA_chart.to_html(),
        "candleFig": candleFig.to_html(),
        "sma": candleSMA_chart.to_html(),
        "macd_rsi": macd_rsi_chart.to_html(),
        "adx_atr": adx_atr_chart.to_html(),
        "bollinger": bollinger_chart.to_html(),
        "change_rate": roc_chart.to_html(),
        "volume": vol_chart.to_html(),
        "voltty": voltty.to_html(),
    }


def getDataset(ticker: str, start: dt.datetime, end: dt.datetime) -> pd.DataFrame:
    try:
        df = yf.Ticker(ticker).history(start=start, end=end)
    except:
        yf.pdr_override()
        df = web.DataReader(ticker, start=start, end=end)
        ic(df)
    finally:
        df.reset_index(inplace=True)
        df.ffill(inplace=True)  # Filling days with empty data (Non business days)
    return df


def calcIns(df: pd.DataFrame) -> dict:
    ic()
    desc = df.describe()
    rows = ["min", "max", "mean"]
    info = pd.DataFrame(
        data=[desc.loc[i] for i in rows], index=rows, columns=desc.columns
    ).drop("Volume", axis=1)
    low = round(info.Low.loc["min"], 2)
    high = round(info.High.loc["max"], 2)
    open_avg = round(info.Open.loc["mean"], 2)
    high_avg = round(info.High.loc["mean"], 2)
    close_max = round(info.Close.loc["max"], 2)
    context = {
        "low": low,
        "high": high,
        "open_avg": open_avg,
        "high_avg": high_avg,
        "close_max": close_max,
    }

    df["Price Change"] = df["Close"].diff()
    df['Gain'] = df['Price Change'].apply(lambda x: x if x > 0 else 0)
    df['Loss'] = df['Price Change'].apply(lambda x: abs(x) if x < 0 else 0)

    n = 14
    df['Average Gain'] = df['Gain'].rolling(window=n, min_periods=1).mean()
    df['Average Loss'] = df['Loss'].rolling(window=n, min_periods=1).mean()

    ########    Trend Indicators    ########
    # Simple Moving Average (SMA)
    df["SMA"] = df["Close"].rolling(window=n).mean()

    # Exponential Moving Average (EMA)
    df["EMA"] = df["Close"].ewm(span=n, adjust=False).mean()

    # Moving Average Convergence Divergence (MACD)
    df["MACD"] = (
        df["Close"].ewm(span=12, adjust=False).mean()
        - df["Close"].ewm(span=26, adjust=False).mean()
    )

    # Relative Strength Index (RSI)
    df["RSI"] = 100 - (100 / (1 + df["Average Gain"] / df["Average Loss"]))

    # Average Directional Index (ADX)
    df["ADX"] = ta.ADX(df["High"], df["Low"], df["Close"], timeperiod=n)

    # Bollinger Bands
    # * Upper Bollinger Band
    df["Upper Band"] = df["SMA"] + 2 * df["Close"].rolling(window=n).std()
    # * Lower Bollinger Band
    df["Lower Band"] = df["SMA"] - 2 * df["Close"].rolling(window=n).std()

    # Volatility
    # Historical Volatility
    df["Volatility"] = df["Close"].pct_change().rolling(window=n).std() * sqrt(n)

    # Price Rate of Change (ROC)
    df["ROC"] = (df["Close"] - df["Close"].shift(n)) / df["Close"].shift(n) * 100

    # Average True Range (ATR)
    df["ATR"] = ta.ATR(df["High"], df["Low"], df["Close"], timeperiod=n)

    return context
