import pandas as pd

from sklearn.linear_model import LinearRegression

def init_regressor(ticker, df):
	regr = LinearRegression()
	if df.loc[df['Ticker'] == ticker, 'CDI'].isna().any():
		regr.fit(df.loc[df['Ticker'] == ticker, 'Valor'].values.reshape(-1, 1), 
        	df.loc[df['Ticker'] == ticker, 'IPCA'].values)
	else:
		regr.fit(df.loc[df['Ticker'] == ticker, 'Valor'].values.reshape(-1, 1), 
        	df.loc[df['Ticker'] == ticker, 'CDI'].values)

	return regr

YIELD = pd.read_csv('data/yield.csv', index_col=0)
YIELD_REGR = {ticker: init_regressor(ticker, YIELD) for ticker in YIELD['Ticker'].unique()}

INFO = pd.read_csv('data/info.csv', index_col=0)
SYMBOLS = INFO['symbol'].unique()

market_price = lambda x : INFO.loc[INFO['symbol'] == x, 'regularMarketPrice'].values[0]
market_previous = lambda x : INFO.loc[INFO['symbol'] == x, 'regularMarketPreviousClose'].values[0]