from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api
import os
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from TradingStrategy import TradingStrategy
from User import User
from Asset import Asset
import uuid
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with a secure secret key


client = MongoClient(os.environ.get('MONGO_URI'))

db = client.flask_db


jwt = JWTManager(app)
api = Api(app)



####### HOME ROUTE ##########
@app.route('/', methods=['GET'])
def home():
    return "Welcome to Emma's website. It is currently being used for something else. Please come back another time."



################# USER REGISTER ###################
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    try:
        user = User(data.get('username'), generate_password_hash(data.get('password'), method='scrypt'), data.get('tradier_token'), data.get('account_number'))
    except Exception as error:
        return jsonify('registration ERROR: ' + type(error).__name__)
    # Check if the username is already taken
    if db.users.find_one({'username': data['username']}):
        return jsonify({'message': 'Username already exists'}), 400
    
    # Create a new user record in the database
    user_data = user.serialize()

    result = db.users.insert_one(user_data)
    return jsonify({'message': 'User registered successfully'}), 201





################# USER LOGIN ###################
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': 'Invalid username or password'}), 401

    
@app.route('/api/activate/<string:strategy_id>', methods=['PUT'])
@jwt_required()
def activate_strategy(strategy_id):
    current_user = get_jwt_identity()

    # Find the strategy by its ID
    strategy = db.trading_strategies.find_one({'user_id': current_user, '_id': strategy_id})

    if not strategy:
        return jsonify({'message': 'Strategy not found'}), 404

    # Set the 'active' field for all the user's strategies to False
    db.trading_strategies.update_many({'user_id': current_user}, {'$set': {'active': False}})

    # Activate the selected strategy
    db.trading_strategies.update_one({'_id': strategy['_id']}, {'$set': {'active': True}})

    return jsonify({'message': 'Strategy activated successfully'}), 200



######## TRADING STRATEGY API ENDPOINT #############
class TradingStrategiesResource(Resource):
    @jwt_required()
    def get(self):
        '''returns all existing trading strategies created by the user'''
        current_user = get_jwt_identity()
        strategies = db.trading_strategies.find({'user_id': current_user})
        return jsonify([strategy for strategy in strategies])

    @jwt_required()
    def post(self):
        '''attempts to create a new trading strategy'''
        current_user = get_jwt_identity() #get current authenticated user
        data = request.json #convert to json

        exists = db.trading_strategies.find_one({'user_id': current_user, 'name': data['name']}) #try to find an strategy that already exists for the current user with the same name, (avoid duplication)
        if exists:
            print('ERROR! CANNOT CREATE NEW TRADING STRATEGY: STRATEGY NAME ALREADY EXISTS!')
            return {'message': 'Strategy name already exists'}, 400
        else:
            print('creating trading strategy......')
            data['user_id'] = current_user
            strategy = TradingStrategy(data['user_id'], data['name'], data['description'], data['type'], data['frequency'])
            data = strategy.serialize()
            result = db.trading_strategies.insert_one(data)

            if result.acknowledged:
                return {'message': 'Trading strategy created successfully: ' + data['_id']}, 201
            else:
                return {'message': 'Failed to create strategy'}, 500
            
    

    @jwt_required()
    def get_strategy(self, strategy_name):
        current_user = get_jwt_identity() #get current username that is authenticated
        strategy = db.trading_strategies.find_one({'user_id': current_user, 'name': strategy_name})
        if strategy:
            return jsonify(strategy), 200
        else:
            return {'message': 'Strategy not found'}, 404
        

######## ASSET API ENDPOINT #############
class AssetsResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity() #get current username that is authenticated
        assets = db.assets.find({'user_id': current_user}) #get all assets for the authenticated user
        return jsonify([asset for asset in assets]) #return them

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity() #get current authenticated user
        data = request.json #convert to json

        exists = db.assets.find_one({'user_id': current_user, 'name': data['name']}) #try to find an asset that already exists for the current user with the same name, (avoid duplication)
        if exists:
            print('ERROR! CANNOT CREATE NEW ASSET: ASSET NAME ALREADY EXISTS!')
            return {'message': 'Asset name already exists'}, 400
        else:
            print('creating asset......')
            GENERATED_ID = str(uuid.uuid4()) # generate unique id using uuid package

            data['user_id'] = current_user
            data['_id'] = GENERATED_ID
            result = db.assets.insert_one(data)

            if result.acknowledged:
                return {'message': 'Asset created successfully: ' + data['_id']}, 201
            else:
                return {'message': 'Failed to create asset'}, 500

    @jwt_required()
    def get_asset(self, asset_name):
        current_user = get_jwt_identity() #get current username that is authenticated
        asset = db.assets.find_one({'user_id': current_user, 'name': asset_name})
        if asset:
            return jsonify(asset), 200
        else:
            return {'message': 'Asset not found'}, 404

# Add API resource routes
api.add_resource(TradingStrategiesResource, '/api/trading_strategies')
api.add_resource(AssetsResource, '/api/assets')











if __name__ == '__main__':
    app.run(debug=True)




