
from flask import Blueprint, request, jsonify
from utils.db import db
from models.dashboard import Dashboard
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User  

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/create', methods=['POST'])
@jwt_required(optional=True)                    
def create_dashboard():

    data = request.json
    user_email = get_jwt_identity() 
    user = User.query.filter_by(email=user_email).first()  

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    print(data)
    dashboard_name = data.get('dashboardName')
    predeterminado = data.get('predeterminado', True) 
    description = data.get('description', '')  

    if not dashboard_name:
        return jsonify({'msg': 'Name is required'}), 400 

    new_dashboard = Dashboard(user_id=user.id, name=dashboard_name, predeterminado=predeterminado, description=description)

    db.session.add(new_dashboard)
    db.session.commit()

    return jsonify({"msg": "Dashboard created successfully", "id": new_dashboard.id}), 201


@dashboard_bp.route('/read', methods=['GET'])
@jwt_required()  
def read_dashboards():
    user_email = get_jwt_identity()  
    user = User.query.filter_by(email=user_email).first()  

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    dashboards = Dashboard.query.filter_by(user_id=user.id).all()  

    
    if not dashboards:
        return jsonify({'msg': 'No dashboards found'}), 404

    
    dashboards_data = []
    for dashboard in dashboards:
        dashboards_data.append({
            'id': dashboard.id,
            'name': dashboard.name,
            'predeterminado': dashboard.predeterminado,
            'description': dashboard.description
        })

    return jsonify({'dashboards': dashboards_data}), 200

@dashboard_bp.route('/update/<int:dashboard_id>', methods=['PUT'])
@jwt_required()  
def update_dashboard(dashboard_id):
    
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()

    
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    
    dashboard = Dashboard.query.filter_by(id=dashboard_id, user_id=user.id).first()

    
    if not dashboard:
        return jsonify({'msg': 'Dashboard not found or does not belong to user'}), 404

    
    data = request.json
    name = data.get('name', dashboard.name)  
    predeterminado = data.get('predeterminado', dashboard.predeterminado)  
    description = data.get('description', dashboard.description)  
    dashboard.name = name
    dashboard.predeterminado = predeterminado
    dashboard.description = description

    db.session.commit()

    return jsonify({'msg': 'Dashboard updated successfully'}), 200



@dashboard_bp.route('/delete/<int:dashboard_id>', methods=['DELETE'])
@jwt_required()  
def delete_dashboard(dashboard_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    dashboard = Dashboard.query.filter_by(id=dashboard_id, user_id=user.id).first()

    if not dashboard:
        return jsonify({'msg': 'Dashboard not found or does not belong to user'}), 404

    
    db.session.delete(dashboard)
    db.session.commit()

    return jsonify({'msg': 'Dashboard deleted successfully'}), 200







