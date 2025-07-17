import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport

@st.cache_data
def load_data():
    """Load the list of S&P 500 companies from Wikipedia.

    Returns
    -------
    data : pd.DataFrame
        DataFrame containing the list of S&P 500 companies.
    """
    url = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data = pd.read_html(url)[0]
    return data

data = load_data()

df_grouped_by_sector = data.groupby('GICS Sector')

st.title("S&P500 overview")

pr = ProfileReport(data)

st.markdown("This is a comprehensive report of the all companies that are included in the S&P500 index.")
st_profile_report(pr)

selected_sectors = st.sidebar.multiselect("Sector", sorted(list(data['GICS Sector'].unique())))

filtered_dataframe = data[data['GICS Sector'].isin(selected_sectors)]
st.header("General dataframe")
st.write(f"Here you can see the data regarding the companies belonging to selected sectors." +
         f"\nThe dataframe consists of {filtered_dataframe.shape[0]} rows and {filtered_dataframe.shape[1]} columns.")

st.dataframe(filtered_dataframe)

@st.cache_data
def convert_to_download(df):
    """
    Convert a DataFrame to a UTF-8 encoded CSV byte stream.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be converted.

    Returns
    -------
    bytes
        CSV representation of the DataFrame, encoded in UTF-8.
    """
    csv_file = df.to_csv(index=False).encode("utf-8")
    return csv_file


filtered_csv = convert_to_download(filtered_dataframe)

st.download_button(
    label="Download CSV",
    data=filtered_csv,
    file_name="data.csv"
)

spx_data = yf.download(
    tickers=list(filtered_dataframe.Symbol[:10]),
    period="ytd",
    group_by="ticker"
)

def price_plot(symbol):
    """Plots the closing price of the passed symbol.

    Parameters
    ----------
    symbol : str
        Symbol representing selected company in string format.

    Returns
    -------
        None
    """
    df = pd.DataFrame(spx_data[symbol])

    fig, ax = plt.subplots()

    ax.fill_between(df.index, df.Close, color="crimson", alpha=0.5)
    ax.plot(df.index, df.Close, color="crimson", alpha=0.9)
    ax.set_title(f"Price plot of {symbol}", fontweight="bold")
    ax.set_xlabel("Date", fontweight="bold")
    ax.set_ylabel("Price", fontweight="bold")

    st.pyplot(fig)


number_of_plots = st.sidebar.slider("Select number of plots", 1, 10)

st.header("Plots")
st.write("Show the specified number of plots of the selected sectors.")

if st.button("Show plots"):
    for symbol in filtered_dataframe.Symbol[:number_of_plots]:
        price_plot(symbol)