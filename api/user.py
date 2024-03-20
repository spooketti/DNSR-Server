import jwt
from flask import Blueprint, request, jsonify, current_app, Response, make_response
from flask_restful import Api, Resource
from authToken import token_required
from init import db

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')


# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):
        @token_required
        def post(self):
            body = request.get_json()

            name = body.get('name')
            uid = body.get('uid')
            password = body.get('password')
            role = body.get('role')

            if uid is not None:
                new_user = User(name=name, uid=uid, password=password, role=role)

            user = new_user.create()
            if user:
                return user.read()
            
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400
        

        @token_required
        def get(self):
            users = User.query.all()
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)

        
        def put(self, user_id):
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            body = request.get_json()
            user.name = body.get('name', user.name)
            user.uid = body.get('uid', user.uid)
            db.session.commit()
            return user.read(), 200

        def delete(self):
            body = request.get_json()
            uid = body.get('uid')
            password = body.get('password')

            user = User.query.filter_by(_uid=uid).first()
            if user is None or not user.is_password(password):
                return {'message': f'User {uid} not found'}, 404
            
            json = user.read()

            if user:
                try:
                    user.delete() 
                except Exception as e:
                    return {
                        "error": "Something went wrong!",
                        "message": str(e)
                    }, 500
            # 204 is the status code for delete with no json response
            return f"Deleted user: {json}", 204 # use 200 to test with Postman
    


    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400

                uid = body.get('uid')
                password = body.get('password')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token_payload = {
                            "_uid": user._uid,
                            "role": user.role 
                        }
                        token = jwt.encode(
                            token_payload,
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'
                                )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500
            


    class Login(Resource):
        def post(self):
            data = request.get_json()

            uid = data.get('uid')
            password = data.get('password')

            if not uid or not password:
                response = {'message': 'Invalid creds'}
                return make_response(jsonify(response), 401)

            user = User.query.filter_by(_uid=uid).first()

            if user and user.is_password(password):
         
                response = {
                    'message': 'Logged in successfully',
                    'user': {
                        'name': user.name,  
                        'id': user.id
                    }
                }
                return make_response(jsonify(response), 200)

            response = {'message': 'Invalid id or pass'}
            return make_response(jsonify(response), 401)
        
            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(Login, '/login')
