from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, set_refresh_cookies
from utils.db import db
from models.user import User
from models.dashboard import Dashboard
import bcrypt


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    name = data.get('name') 
    email = data.get('email') 
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'Username and password are required'}), 401
    
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 401

    hashed_password = password.encode('utf-8')
    sal = bcrypt.gensalt()
    encripted = bcrypt.hashpw(hashed_password, sal).decode('utf-8')

    new_user = User(email=email, name=name, password=encripted)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User successfully registered"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():

    token = request.cookies.get('access_token')
    if token:
        

        return jsonify({'msg': 'Theres an user logged in'}), 400

    data = request.json
    email = data.get('email') 
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):     
        return jsonify({'msg': 'Invalid password'}), 401
    
    access_token = create_access_token(identity=email)

    response = jsonify({'msg': 'Login successful'})
    set_access_cookies(response, access_token)
    print(token)

    return response, 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'msg': 'Logout successful'})
    response.delete_cookie('access_token')

    return response, 200

