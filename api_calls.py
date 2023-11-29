import requests

base_url = 'https://emmaeverding.com'


def new_user(username, password, tradier_token):
    url = f'{base_url}/api/register'

    data = {
        'username': username,  
        'password': password,   
        'tradier_token': tradier_token,
    }

    response = requests.post(url, json=data)
    print(response)

def login(username, password):
        url = f'{base_url}/api/login'

        data = {
            'username': username, 
            'password': password   
        }

        response = requests.post(url, json=data)
        token = response.json()['access_token']
        return token


def new_asset(access_token, user_id, name, description, purchase_date, appreciation, initial_value):
    url = f'{base_url}/api/assets'

    data = {
            'user_id': user_id,
            'name': name,
            'description': description,
            'purchase_date': purchase_date,
            'appreciation': appreciation,
            'initial_value': initial_value,
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, json=data, headers=headers)

    print(response)



def new_strat(access_token, user_id, name, description, type, frequency):
    url = f'{base_url}/api/trading_strategies'

    data = {
        'user_id': user_id,
        'name': name,
        'description': description,
        'type': type,
        'frequency': frequency,
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, json=data, headers=headers)
    print(response)

username = 'mason12345'

#new_user(username, '12345', 't5643gh65333h635')

token = login(username,'12345')

new_strat(token, username, 'other strat', 'default strategy description', 'reversion', '1d')
#new_asset(token, username, 'My house', 'the housing market is booming. time to buy!', '2007-12-05', -0.5, '250000')



