import time
import requests
import pandas as data_processer
from prometheus_client import start_http_server, Gauge


class Solution:

    BINANCE_API_URL = 'https://api.binance.com/api'
    Health_URL = "/v3/ping"
    Symbol_URL = "/v3/ticker/24hr"
    BID_ASK_URL= "/v3/depth" 
    PRICE_SPREAD_URL = '/v3/ticker/bookTicker'



    def __init__(self):
        self.prometheus_metrics = Gauge('delta_value',
                        'Delta of Spread', ['symbol'])


    def print_symbols(self, sym, field):
        try:
          req = requests.get(self.BINANCE_API_URL + self.Symbol_URL)
        except Exception as exc:
          print ("API ERROR",exc)
          return
        datafm = data_processer.DataFrame(req.json())
        datafm = datafm[['symbol', field]]
        datafm = datafm[datafm.symbol.str.contains(r'(?!$){}$'.format(sym))]
        datafm[field] = data_processer.to_numeric(datafm[field], downcast='float', errors='coerce')
        datafm = datafm.sort_values(by=[field], ascending=False).head(5)
        return datafm

    def print_notional(self, sym, field):
 
        syms = self.print_symbols(sym, field)
        notion = {}
        if syms is None:
         return
        else:
         for sym in syms['symbol']:
            payload = { 'symbol' : sym, 'limit' : 500 }
            try:
             req = requests.get(self.BINANCE_API_URL + self.BID_ASK_URL, params=payload)
            except Exception as exc:
              print("API ERROR",exc)
              return
            for col in ["bids", "asks"]:
                datafm = data_processer.DataFrame(data=req.json()[col], columns=["price", "quantity"], dtype=float)
                datafm = datafm.sort_values(by=['price'], ascending=False).head(200)
                datafm['notional'] = datafm['price'] * datafm['quantity']
                datafm['notional'].sum()
                notion[sym + '_' + col] = datafm['notional'].sum()
        return notion

    def print_spread(self, sym, field):

        syms = self.print_symbols(sym, field)
        spread = {}
        if syms is None:
         return
        else:
         for sym in syms['symbol']:
            uri = { 'symbol' : sym }
            try:
              req = requests.get(self.BINANCE_API_URL + self.PRICE_SPREAD_URL, params=uri)
            except Exception as exc:
              print("API ERROR",exc)
              return
            price = req.json()
            spread[sym] = float(price['askPrice']) - float(price['bidPrice'])
        return spread


if __name__ == "__main__":

    solution = Solution()
    datafm=solution.print_symbols('BTC','volume')
    print(datafm)
    datafm=solution.print_symbols('USDT', 'count')
    print(datafm)
    datafm=solution.print_notional('BTC', 'volume')
    print(datafm)
    datafm=solution.print_spread('USDT', 'count')
    print(datafm)

    InfinitLoop=True
    try:
     start_http_server(8080)
    except Exception as exc:
              print("Server not started",exc)      
    while InfinitLoop:
        delta = {}
        old = solution.print_spread('USDT', 'count')
        time.sleep(10)
        new = solution.print_spread('USDT', 'count')
        for key in old:
            delta[key] = abs(old[key]-new[key])
        for key in delta:
            solution.prometheus_metrics.labels(key).set(delta[key])
            print(delta)
