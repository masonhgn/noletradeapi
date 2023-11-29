import os
from pymongo import MongoClient
import datetime

# Get the MongoDB URI from the environment variable
mongo_uri = os.getenv('MONGO_URI')

# create client to connect to the MongoDB database
client = MongoClient(mongo_uri)

# access database
db = client.flask_db

'''
FUNCTION OF THIS SCRIPT
- gather all active trading strategies for all users
- filter to isolate the strategies whose next execution days are today
- execute trades for those strategies, corresponding to each user's tradier api key
- set each trading strategy's next execution day to today + frequency, making sure it lands on a trading day
'''



def fetch_active_strategies():
    print('fetching all active strategies')
    '''gets all active TradingStrategy objects for all users whose execution days are today'''
    today = str(datetime.date.today())
    print(f'Fetching all active strategies for {today}')

    # Get all active strategies with an execution date equal to today
    active_strategies = db.trading_strategies.find({'active': True, 'execution_date': today})

    for strategy in active_strategies:
        execute_strategy(strategy)



def execute_strategy(strategy):
    '''actually executes an individual trading strategy, sets new execution day'''
    strategy_id = strategy['_id']
    user_id = strategy['user_id']
    name = strategy['name']
    frequency = strategy['frequency']
    tradier_token = strategy['tradier_token']

    print(f'Executing strategy "{name}" (ID: {strategy_id}) for user {user_id}')




fetch_active_strategies()
