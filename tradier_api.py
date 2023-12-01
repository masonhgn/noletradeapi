import requests

class ApiBridge:
    def __init__(self, token, account_number):
        self.token = token
        self.account_number = account_number
    def check_status(self):
        response = requests.get('https://sandbox.tradier.com/v1/user/profile',
            params={},
            headers={'Authorization': 'Bearer '+self.token, 'Accept': 'application/json'}
        )
        json_response = response.json()
        return response.status_code == 200

    def get_account_info(self):
        response = requests.get('https://sandbox.tradier.com/v1/user/profile',
            params={},
            headers={'Authorization': 'Bearer '+self.token, 'Accept': 'application/json'}
        )
        json_response = response.json()
        print(response.status_code)
        print(json_response)

    def get_balance(self):
        response = requests.get('https://sandbox.tradier.com/v1/accounts/'+self.account_number+'/balances',
            params={},
            headers={'Authorization': 'Bearer '+self.token, 'Accept': 'application/json'}
        )
        if response.status_code != 200:
            print('api call during get_balance function call unsuccessful: ' + response.status_code)
            return None
        json_response = response.json()
        return json_response

    def get_cash_available(self):
        balance = self.getBalance()
        print(balance['cash_available'])

    def get_positions(self):
        response = requests.get('https://sandbox.tradier.com/v1/accounts/'+self.account_number+'/positions',
            params={},
            headers={'Authorization': 'Bearer '+self.token, 'Accept': 'application/json'}
        )
        json_response = response.json()
        print(response.status_code)
        return json_response

    def liquidate(self):
        positions = bridge.get_positions()['positions']
        if positions == 'null':
            print('there are not positions to liquidate.')
            return False
        for pos in positions:
            for p in positions[pos]:
                ticker = p['symbol']
                quantity = p['quantity']
                success = (self.market_order('sell', ticker, quantity)['order']['status'] == 'ok')
                if not success:
                    print('liquidate() ERROR: ' + quantity + ' shares of ' + ticker + ' have not been sold due to an unsuccessful market order.')
                    return False
        if self.get_positions()['positions'] == None: return True
        print('liquidate() ERROR: not all positions have been liquidated for some reason.')
        return False

    def limit_order(self, ticker, quantity, price):
        response = requests.post('https://sandbox.tradier.com/v1/accounts/'+self.account_number+'/orders',
            data={'class': 'equity', 'symbol': ticker, 'side': 'buy', 'quantity': quantity, 'type': 'limit', 'duration': 'day', 'price': price},
            headers={'Authorization': 'Bearer '+self.token, 'Accept': 'application/json'}
        )
        json_response = response.json()
        return json_response

    def market_order(self, side, ticker, quantity):
        response = requests.post('https://sandbox.tradier.com/v1/accounts/'+self.account_number+'/orders',
            data={'class': 'equity', 'symbol': ticker, 'side': side, 'quantity': quantity, 'type': 'market', 'duration': 'day'},
            headers={'Authorization': 'Bearer '+self.token, 'Accept': 'application/json'}
        )
        json_response = response.json()
        return json_response



bridge = ApiBridge('LUiHZ2fsw2f8lfptk0UTmLH5BnrX','VA43237255')

#print(bridge.get_balance())

#print(bridge.limit_order('AAPL', 30, '191'))
#bridge.market_order('AMZN', 10)
#positions = bridge.get_positions()['positions']
print(bridge.liquidate())

#def even_investment(tickers):

        