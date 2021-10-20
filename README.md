# binance-test
binance-test


# Questions:
1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.

Solution : 
Hit binance API for last 24hr to get list of all symbols and short it on volume . 
Filter on suffix "BTC"
pick top 5 and print 


2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.

Solution : 
Same as Q1 just short on count .
Filter on suffix "USDT"
pick top 5 and print 


3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?

Solution:
Call Q1 function
for each symbol hit depth API for limit-500
short the bid array in json response
short the ask array in json response
calculate total and print

4. What is the price spread for each of the symbols from Q2?

Solution:
Call Q1 function with "USDT"
for each symbol calculat ask- bid


5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.
6. Make the output of Q5 accessible by querying http://localhost:8080/metricsusing the Prometheus Metrics format.

Solution:
pip install prometheus_client

create start_http_server
call spread function in 10 sec and calulate delta



Tested Using Python3

IMPORTED PACKAGES:

pandas
requests
simplejson
prometheus-client
