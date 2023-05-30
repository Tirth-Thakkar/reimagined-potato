import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import *
from flask_cors import cross_origin
from model.leaders1 import LeaderUser

leaderboard = Blueprint('leaderUser_api', __name__,
                   url_prefix='/api/leaderboardUser')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(leaderboard)

class LeaderBoardAPI:        
    class AddScore(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 1:
                return {'message': f'Name missing or too short'}, 400
            
            # validate uid
            score = int(body.get('score'))
            if score is None or score <= 0:
                return {'message': f'No username or score is too low'}, 400
            
            locations = body.get('locations')["list"]
            if locations is None or len(locations) <= 0:
                return {'message': f'No username or score is too low'}, 400
            
            tot_distance = int(body.get('tot_distance'))
            if tot_distance is None or tot_distance <= 0:
                return {'message': f'No username or score is too low'}, 400
            
            date = body.get('date')

            ''' #1: Key code block, setup USER OBJECT '''
            userMade = LeaderUser(name=name, score=score, locations=locations, tot_distance=tot_distance)

            # Checks if date of score exists, reformats it to mm-dd-yyyy
            if date is not None:
                try:
                    userMade.date = datetime.strptime(date, '%m-%d-%Y').date()
                except:
                    return {'message': f'Date obtained has a format error {date}, must be mm-dd-yyyy'}, 210
            
            userMade = userMade.create()
            # success returns json of user
            if userMade:
                return jsonify(userMade.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {score} is duplicate'}, 400

    class GetUnflitered(Resource):
        def get(self): # Read Method
            leaders = LeaderUser.query.all()    # read/extract all users from database
            json_ready = [leader.read() for leader in leaders]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps


    class Search(Resource):
        def post(self):
            body = request.get_json()
            name = body.get('name')
            if name is None or len(name) < 1:
                return {'message': f'Name missing or too short'}, 400
            
            leaders = LeaderUser.query.order_by(LeaderUser._score.desc()).all()
            user_scores = [leader.read() for leader in leaders if leader._name == name]
            if len(user_scores) > 0:
                return jsonify(user_scores)
            else: 
                return {'message': f'No user found with name {name}'}, 400
            
    class GetUsersHighestScore(Resource):
        def get(self):
            leaders = LeaderUser.query.order_by(LeaderUser._score.desc()).all()
            json_ready = [leader.read() for leader in leaders]
            return jsonify(json_ready)
    
    
    # building RESTapi endpoint
    api.add_resource(AddScore, '/score')
    api.add_resource(GetUnflitered, '/unfiltered')
    api.add_resource(Search, '/search')
    api.add_resource(GetUsersHighestScore, '/MaxScore')    

    