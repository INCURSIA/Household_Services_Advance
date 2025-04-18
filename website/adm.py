from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User, Service, Professional, ServiceRequest
from flask import jsonify
from . import db
from flask import current_app
import json

adm = Blueprint('adm', __name__)

@adm.route('/dashboard', methods=['GET'])
def admin_dashboard():
    professionals = Professional.query.all()
    customers = User.query.filter_by(role='Customer').all()
    services = Service.query.all()

    professionals_data = [
        {"full_name": p.full_name, "email": p.email, "approved": p.approved, "status": "blocked" if p.status == "blocked" else "active"}
        for p in professionals
    ]

    customers_data = [
        {"full_name": c.full_name, "email": c.email,"status": "blocked" if c.status == "blocked" else "active"}
        for c in customers
    ]

    services_data = [
        {"id": s.id, "name": s.name, "base_price": s.base_price}
        for s in services
    ]

    return jsonify({
        "professionals": professionals_data,
        "customers": customers_data,
        "services": services_data
    })

@adm.route('/approve_professional/<string:email>', methods=['POST'])
def approve_professional(email):
    professional = Professional.query.filter_by(email=email).first()
    if professional:
        professional.approved = True
        db.session.commit()
        return jsonify({"message": f"Professional {email} approved"}), 200
    return jsonify({"error": "Professional not found"}), 404

@adm.route('/reject_professional/<string:email>', methods=['POST'])
def reject_professional(email):
    professional = Professional.query.filter_by(email=email).first()
    if professional:
        db.session.delete(professional)
        db.session.commit()
        return jsonify({"message": f"Professional {email} rejected"}), 200
    return jsonify({"error": "Professional not found"}), 404

@adm.route('/block_user/<string:email>', methods=['POST'])
def block_customer(email):
    customer = User.query.filter_by(email=email).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    customer.status = "blocked"
    db.session.commit()
    return jsonify({"message": f"Customer {email} blocked successfully"}), 200

@adm.route('/create_service', methods=['POST'])
def create_service():
    data = request.get_json()
    name = data.get('name')
    base_price = data.get('base_price')
    description = data.get('description')
    pin_code = data.get('pin_code')

    if not name or not base_price:
        return jsonify({"error": "Name and Base Price are required"}), 400
    
    new_service = Service(name=name, base_price=float(base_price), description=description, pin_code=int(pin_code))
    db.session.add(new_service)
    db.session.commit()

    
    current_app.redis_client.delete("services_list")

    return jsonify({"message": f"Service {name} created successfully"}), 201

@adm.route('/update_service/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    data = request.get_json()
    service.name = data.get('name', service.name)
    service.base_price = float(data.get('base_price', service.base_price))
    service.description = data.get('description', service.description)
    service.pin_code = int(data.get('pin_code', service.pin_code))

    db.session.commit()

    
    cache_key = "services_list"
    redis_client = current_app.redis_client

    
    cached_services = redis_client.get(cache_key)
    if cached_services:
        services_data = json.loads(cached_services)
        for s in services_data:
            if s["id"] == service.id:
                s["name"] = service.name
                s["base_price"] = service.base_price
                s["description"] = service.description
                s["pin_code"] = service.pin_code
        redis_client.set(cache_key, json.dumps(services_data))  # Update cache
    
    return jsonify({"message": f"Service {service.name} updated successfully"})

@adm.route('/delete_service/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()

        
        current_app.redis_client.delete("services_list")

        return jsonify({"message": f"Service {service.name} deleted"}), 200
    return jsonify({"error": "Service not found"}), 404

@adm.route('/clear_cache', methods=['POST'])
def clear_cache():
    current_app.redis_client.delete("services_list")
    return jsonify({"message": "Cache cleared"}), 200


@adm.route('/search_professional', methods=['GET'])
def search_professional():
    query = request.args.get('query', '')
    professionals = Professional.query.filter(
        (Professional.email.ilike(f"%{query}%")) | (Professional.full_name.ilike(f"%{query}%"))
    ).all()
    
    results = [{"email": p.email, "full_name": p.full_name,"status": p.status, "approved": p.approved} for p in professionals]
    return jsonify(results), 200

@adm.route('/admin_summary', methods=['GET'])
def admin_summary():
    summary = {
        "Pending": ServiceRequest.query.filter_by(status='Pending').count(),
        "Assigned": ServiceRequest.query.filter_by(status='Assigned').count(),
        "Closed": ServiceRequest.query.filter_by(status='Closed').count()
    }
    return jsonify(summary), 200


@adm.route('/export', methods=['POST'])
def export_requests():
    admin_email = 'admin@gmail.com'
    from website.tasks import export_closed_requests
    task = export_closed_requests.apply_async(args=[admin_email])

    print(f"Task sent: {task.id}")  # Log task ID
    print(f"Task queued? {task.state}")  # Check if the task is in the queue
    return jsonify({"message": "Export started"}), 202


@adm.route('/unblock_customer/<string:email>', methods=['POST'])
def unblock_customer(email):
    customer = User.query.filter_by(email=email).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    customer.status = "active"
    db.session.commit()
    return jsonify({"message": f"Customer {email} unblocked successfully"}), 200

@adm.route('/block_professional/<string:email>', methods=['POST'])
def block_professional(email):
    professional = Professional.query.filter_by(email=email).first()
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    
    professional.status = "blocked"
    db.session.commit()
    return jsonify({"message": f"Professional {email} blocked successfully"}), 200

@adm.route('/unblock_professional/<string:email>', methods=['POST'])
def unblock_professional(email):
    professional = Professional.query.filter_by(email=email).first()
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    
    professional.status = "active"
    db.session.commit()
    return jsonify({"message": f"Professional {email} unblocked successfully"}), 200

@adm.route('/get_services', methods=['GET'])
def get_services():
    cache_key = "services_list"
    redis_client = current_app.redis_client

    cached_services = redis_client.get(cache_key)
    if cached_services:
        print("Cache HIT")  
        return jsonify({"services": json.loads(cached_services)}), 200

    print("Cache MISS")  
    services = Service.query.all()
    services_data = [
        {"id": s.id, "name": s.name, "base_price": s.base_price, "description": s.description, "pin_code": s.pin_code}
        for s in services
    ]
    redis_client.setex(cache_key, 3600, json.dumps(services_data))
    print("Cache SET")  
    return jsonify({"services": services_data}), 200

