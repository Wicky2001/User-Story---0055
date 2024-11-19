from flask import Flask, jsonify, request, render_template,make_response
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth
from database import (
    get_all_users,
    find_user_by_id,
    find_user_by_username,
    add_user,
    update_user,
    delete_user,
    verify_api_key,
)

app = Flask(__name__)
api = Api(app)
auth = HTTPTokenAuth(scheme="Bearer")

@auth.verify_token
def verify_api_key_wrapper(request_api_key):
    return True if verify_api_key(request_api_key) else None

class Users(Resource):
    @auth.login_required
    def get(self):
        user_id = request.args.get("user_id")
        username = request.args.get("username")

        if not user_id and not username:
            return {"message": "Please provide either user_id or username"}, 400

        if user_id:
            user = find_user_by_id(user_id)
        elif username:
            user = find_user_by_username(username)

        if user:
            return jsonify(user)
        else:
            return {"message": "User not found"}, 404

    @auth.login_required
    def post(self):
        data = request.get_json()
        if not data or not data.get("user_id") or not data.get("username"):
            return {"message": "Missing user_id or username"}, 400

        add_user(data["user_id"], data["username"])
        return {"message": "User added successfully"}, 201

    @auth.login_required
    def put(self):
        data = request.get_json()
        if not data or not data.get("user_id") or not data.get("username"):
            return {"message": "Missing user_id or username"}, 400

        updated = update_user(data["user_id"], data["username"])
        if updated:
            return {"message": "User updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    @auth.login_required
    def delete(self):
        user_id = request.args.get("user_id")
        if not user_id:
            return {"message": "Missing user_id"}, 400

        deleted = delete_user(user_id)
        if deleted:
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

class GetAllUsers(Resource):
    @auth.login_required
    def get(self):
        return jsonify(get_all_users())

class Home(Resource):
    def get(self):
        # Generate the HTML content using render_template
        html = render_template('index.html')
        
        # Create a response with correct Content-Type
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html'
        return response

api.add_resource(Users, "/users")
api.add_resource(GetAllUsers, "/allUsers")
api.add_resource(Home, "/")

if __name__ == "__main__":
    app.run(debug=True)
