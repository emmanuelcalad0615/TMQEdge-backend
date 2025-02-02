from flask import jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies
from app import app, jwt


@app.route("/debug-cookies")
def debug_cookies():
    print("Cookies recibidas:", request.cookies)  # Deberías ver access_token_cookie
    return jsonify({"cookies": dict(request.cookies)})

@app.after_request
def add_cors_headers(response):
    # response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')  # Para cookies
    return response

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    response = jsonify({'msg': 'Token has expired'})
    response.delete_cookie('access_token')
    return redirect('/')

@app.route('/register')
def register():
    return send_from_directory('templates', 'register.html') 


if __name__ == '__main__':
    app.run(debug=True)