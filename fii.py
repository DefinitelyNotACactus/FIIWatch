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

TODAY = pd.Timestamp.today()

QUOTES = pd.read_csv('data/quotes.csv', index_col=0)
QUOTES = QUOTES.dropna()
QUOTES['date'] = pd.to_datetime(QUOTES['date'])
QUOTES_12MO = QUOTES[(TODAY - QUOTES.date).dt.days <= 365]
QUOTES_1MO = QUOTES[(TODAY - QUOTES.date).dt.days <= 30]

YIELD = pd.read_csv('data/yield.csv', index_col=0)
YIELD_REGR = {ticker: init_regressor(ticker, YIELD) for ticker in YIELD['Ticker'].unique()}

INFO = pd.read_csv('data/info2.csv', index_col=0)
SYMBOLS = INFO['symbol'].unique()

EARNINGS = pd.read_csv('data/earnings.csv', index_col=0)
EARNINGS['approvedOn'] = pd.to_datetime(EARNINGS['approvedOn'], errors='coerce')
EARNINGS_12MO = EARNINGS[12 * (TODAY.year - EARNINGS['approvedOn'].dt.year) + (TODAY.month - EARNINGS['approvedOn'].dt.month) <= 12]

market_price = lambda x : INFO.loc[INFO['symbol'] == x, 'regularMarketPrice'].values[0]
market_previous = lambda x : INFO.loc[INFO['symbol'] == x, 'regularMarketPreviousClose'].values[0]

delta_12mo = lambda x : QUOTES_12MO.loc[QUOTES_12MO['ticker'] == x, ['date', 'close']].sort_values(by='date')['close'].values[-1] - QUOTES_12MO.loc[QUOTES_12MO['ticker'] == x, ['date', 'close']].sort_values(by='date')['close'].values[0]
delta_1mo = lambda x : QUOTES_1MO.loc[QUOTES_1MO['ticker'] == x, ['date', 'close']].sort_values(by='date')['close'].values[-1] - QUOTES_1MO.loc[QUOTES_1MO['ticker'] == x, ['date', 'close']].sort_values(by='date')['close'].values[0]
relative_delta_12mo = lambda x : delta_12mo(x) / QUOTES_12MO.loc[QUOTES_12MO['ticker'] == x, ['date', 'close']].sort_values(by='date')['close'].values[0] * 100
relative_delta_1mo = lambda x : delta_1mo(x) / QUOTES_1MO.loc[QUOTES_1MO['ticker'] == x, ['date', 'close']].sort_values(by='date')['close'].values[0] * 100

pvp = lambda x : INFO.loc[INFO['symbol'] == x, 'regularMarketPrice'].values[0] / INFO.loc[INFO['symbol'] == x, 'patrimonio_cota'].values[0]

latest_payment = lambda x : EARNINGS.loc[EARNINGS['symbol'] == x, ['approvedOn', 'rate']].sort_values(by='approvedOn')['rate'].values[-1]
dy_12mo = lambda x : (EARNINGS_12MO.loc[EARNINGS_12MO['symbol'] == x, 'rate'].sum() / market_price(x)) * 100