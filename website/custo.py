from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import Professional, ServiceRequest, Service
from datetime import datetime
from . import db

custo = Blueprint('custo', __name__)

@custo.route('/customer/dashboard', methods=['GET'])
@login_required
def customer_dashboard():
    try:
        if current_user.is_authenticated:
            query = request.args.get('query', '')  
            pin_code = request.args.get('pin_code', '')  
            
            services = Service.query
            if query:
                services = services.filter(Service.name.ilike(f'%{query}%'))
            if pin_code:
                services = services.filter_by(pin_code=pin_code)
            services = services.all()

            requests = ServiceRequest.query.filter_by(user_email=current_user.email).all()
            requested_count = ServiceRequest.query.filter_by(user_email=current_user.email, status='Pending').count()
            assigned_count = ServiceRequest.query.filter_by(user_email=current_user.email, status='Assigned').count()
            closed_count = ServiceRequest.query.filter_by(user_email=current_user.email, status='Closed').count()

            return jsonify({
                "services": [s.to_dict() for s in services],
                "requests": [r.to_dict() for r in requests],
                "status_data": {
                    "requested": requested_count,
                    "assigned": assigned_count,
                    "closed": closed_count
                }
            })
        else:
            return jsonify({"error": "User not authenticated"}), 401
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@custo.route('/request_service/<int:service_id>', methods=['POST'])
@login_required
def request_service(service_id):
    service = Service.query.get_or_404(service_id)
    professional = Professional.query.filter_by(service_name=service.name, status="active").first()
    if not professional:
        return jsonify({"error": "No professional available for this service"}), 400
    new_request = ServiceRequest(
        user_email=current_user.email,
        professional_email=professional.email,
        service_id=service.id,
        status='Pending',
        date_created=datetime.now()
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Service request created successfully!","assigned_professional": professional.email})

@custo.route('/my_requests', methods=['GET'])
@login_required
def my_requests():
    requests = ServiceRequest.query.filter_by(user_email=current_user.email).all()
    return jsonify({"requests": [r.to_dict() for r in requests]})

@custo.route('/close_request/<int:request_id>', methods=['POST'])
@login_required
def close_request(request_id):
    request_item = ServiceRequest.query.get(request_id)

    if not request_item:
        return jsonify({"error": "Service request not found"}), 404

    print(f"Request ID: {request_id}, Current User: {current_user.email}, Request Owner: {request_item.user_email}")  # Debugging

    if request_item.user_email != current_user.email:
        return jsonify({"error": "Unauthorized"}), 403  

    request_item.status = 'Closed'
    db.session.commit()

    return jsonify({"message": "Service request closed successfully!"})


@custo.route('/add_remark/<int:request_id>', methods=['POST'])
@login_required
def add_remark(request_id):
    request_item = ServiceRequest.query.get_or_404(request_id)
    if request_item.user_email != current_user.email or request_item.status != 'Closed':
        return jsonify({"error": "Remarks can only be added to your closed requests."}), 403

    data = request.json
    remark = data.get('remark')
    rating = data.get('rating')

    if rating is not None:
        if not (1 <= rating <= 5):
            return jsonify({"error": "Rating must be between 1 and 5."}), 400
        request_item.rating = rating

    request_item.remarks = remark
    db.session.commit()

    return jsonify({"message": "Remark and rating added successfully!"})

@custo.route('/customer_profile', methods=['GET', 'POST'])
@login_required
def customer_profile():
    user = current_user  
    if request.method == 'POST':
        data = request.json
        user.full_name = data.get('full_name', user.full_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        db.session.commit()
        return jsonify({"message": "Profile updated successfully!"})

    return jsonify({
        "full_name": user.full_name,
        "email": user.email,
        "phone_number": user.phone_number
    })

@custo.route('/customer_summary', methods=['GET'])
@login_required
def customer_summary():
    customer_email = current_user.email
    requested_count = ServiceRequest.query.filter_by(user_email=customer_email, status="Pending").count()
    assigned_count = ServiceRequest.query.filter_by(user_email=customer_email, status="Assigned").count()
    closed_count = ServiceRequest.query.filter_by(user_email=customer_email, status="Closed").count()
    
    return jsonify({
        "requested_count": requested_count,
        "assigned_count": assigned_count,
        "closed_count": closed_count
    })

@custo.route('/request_service_view/<int:service_id>', methods=['GET', 'POST'])
@login_required
def request_service_view(service_id):
    service = Service.query.get_or_404(service_id)
    professionals = Professional.query.filter_by(service_name=service.name, approved=True).all()  

    if request.method == 'POST':
        data = request.json
        professional_email = data.get('professional_email')
        professional = Professional.query.filter_by(email=professional_email, approved=True).first()

        if professional:
            new_request = ServiceRequest(
                user_email=current_user.email,
                service_id=service.id,
                professional_email=professional.email,
                status='Pending',
                date_created=datetime.now()
            )
            db.session.add(new_request)
            db.session.commit()
            return jsonify({"message": "Service request created successfully!"})

    return jsonify({
        "service": service.to_dict(),
        "professionals": [{"email": p.email, "full_name": p.full_name} for p in professionals]  
    })


