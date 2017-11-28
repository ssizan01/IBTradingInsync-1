import concurrent.futures

TIMEOUT = 60

def do_stuff_with_stock_symbol(symbol):
    symbol = symbols["symbol"]
    clientId = symbols["clientId"]
    #_call_api(client, symbol)

if __name__ == '__main__':
    symbols = [{"clientId": "1", "symbol": "GOOGL"}]

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(symbols)) as executor:
        results = {executor.submit(do_stuff_with_stock_symbol, symbol, TIMEOUT): symbol for symbol in symbols}

        for future in concurrent.futures.as_completed(results):
            symbol = results[future]
            try:
                data = future.result()
            except Exception as exc:
                print('{} generated an exception: {}'.format(symbol, exc))
            else:
                print('stock symbol: {}, result: {}'.format(symbol, data))