import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
def collect_sp_500_tickers():
    """ gathers all S&P 500 tickers from wikipedia page on S&P 500"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)
    df = table[0]
    tickers = df['Symbol'].tolist()
    return tickers



def create_10_day_momentum_map():
    tickers = collect_sp_500_tickers()
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")

    momentum_map = {}
    print(len(tickers))
    for ticker in tickers:
        #get the last 10 trading days of closing prices
        data = yf.download(ticker, start=start_date, end=end_date)
        if len(data) < 10: continue
        last_10_days = data['Close'].values.tolist()[-10:]
        momentum = (last_10_days[-1] - last_10_days[0]) / last_10_days[-1]
        momentum_map[ticker] = momentum
    #print(momentum_map)
    return momentum_map



def top_x_momentum(x):
    #data_map = sorted(create_10_day_momentum_map(), key=lambda x:x[1], reverse = True)
    sorted_map = {k: v for k, v in sorted(create_10_day_momentum_map().items(), key=lambda item: item[1], reverse = True)}
    first_5_items = dict(list(sorted_map.items())[:x])
    return first_5_items

