from flask import Blueprint, request, jsonify, session
from flask_login import login_user, LoginManager
from .models import User, Professional
from . import db
from flask_cors import cross_origin

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
@cross_origin(origins=["http://localhost:8080", "http://127.0.0.1:8080"], supports_credentials=True)
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
        return jsonify({"error": "Missing credentials"}), 400


    if role == "Customer":
        user = User.query.filter_by(email=email, role="Customer").first()
    elif role == "Professional":
        user = Professional.query.filter_by(email=email, role="Professional", approved=True).first()
    elif role == "Admin":
        user = User.query.filter_by(email=email, role="Admin").first()
    else:
        return jsonify({"error": "Invalid role"}), 400

    if not user:  
        return jsonify({"error": "Invalid email or password"}), 401
    print(f"User found: {user.email}, Status: {user.status}")  
    if user.status and user.status.lower() == "blocked":  
        return jsonify({"error": "Your account is blocked. Contact admin."}), 403

    if user.password == password:
        login_user(user, remember=True)
        session['role'] = role
        return jsonify({"message": "Login successful", "role": role, "user_id": user.email}), 200
    return jsonify({"error": "Invalid email or password"}), 401


@auth.route('/api/signup', methods=['POST'])
@cross_origin(origins=["http://localhost:8080", "http://127.0.0.1:8080"], supports_credentials=True)
def api_signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')  
    full_name = data.get('full_name')
    role = data.get('role')

    if not email or not password or not full_name or not role:
        return jsonify({"error": "Missing fields"}), 400

    if role == "Customer":
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 409

        new_user = User(email=email, password=password, full_name=full_name, role="Customer")
        db.session.add(new_user)

    elif role == "Professional":
        if Professional.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 409

        service_name = data.get('service_name')
        address = data.get('address')

        new_professional = Professional(
            email=email,
            password=password,  
            full_name=full_name,
            role="Professional",
            service_name=service_name,
            address=address,
            approved=False  
        )
        db.session.add(new_professional)

    else:
        return jsonify({"error": "Invalid role"}), 400

    db.session.commit()
    return jsonify({"message": "Signup successful. Awaiting approval if Professional."}), 201
