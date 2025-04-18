from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import Professional, ServiceRequest
from . import db

proff = Blueprint("proff", __name__)


@proff.route("/professional_dashboard")
@login_required
def professional_dashboard():
    active_requests = ServiceRequest.query.filter_by(professional_email=current_user.email, status="Assigned").all()
    pending_requests = ServiceRequest.query.filter_by(professional_email=current_user.email, status="Pending").all()
    completed_requests = ServiceRequest.query.filter_by(professional_email=current_user.email, status="Closed").all()

    return jsonify({
        "pending_requests": [r.to_dict() for r in pending_requests],
        "active_requests": [r.to_dict() for r in active_requests],
        "completed_requests": [r.to_dict() for r in completed_requests]
    })


@proff.route("/accept_request/<int:request_id>", methods=["POST"])
@login_required
def accept_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if service_request:
        service_request.professional_email = current_user.email
        service_request.status = "Assigned"
        db.session.commit()
        return jsonify({"message": "Service request has been accepted!"}), 200
    return jsonify({"error": "Service request not found"}), 404


@proff.route("/reject_request/<int:request_id>", methods=["POST"])
@login_required
def reject_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if service_request:
        service_request.status = "Rejected"
        db.session.commit()
        return jsonify({"message": "Service request has been rejected!"}), 200
    return jsonify({"error": "Service request not found"}), 404


@proff.route("/close_request/<int:request_id>", methods=["POST"])
@login_required
def close_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    
    if service_request.professional_email == current_user.email:
        service_request.status = "Closed"
        db.session.commit()
        return jsonify({"message": "Service request closed successfully!"}), 200

    
    if service_request.user_email == current_user.email:
        service_request.status = "Closed"
        db.session.commit()
        return jsonify({"message": "Service request closed successfully!"}), 200

    return jsonify({"error": "Not authorized to close this request"}), 403


@proff.route("/my_profile", methods=["GET", "POST"])
@login_required
def professional_profile():
    if request.method == "POST":
        data = request.get_json()
        full_name = data.get("full_name")
        email = data.get("email")
        service_name = data.get("service_name")

        professional = Professional.query.filter_by(email=current_user.email).first()
        if professional:
            professional.full_name = full_name
            professional.email = email
            professional.service_name = service_name
            db.session.commit()
            return jsonify({"message": "Profile updated successfully"}), 200
        return jsonify({"error": "Error updating profile"}), 400

    return jsonify({
        "full_name": current_user.full_name,
        "email": current_user.email,
        "service_name": current_user.service_name,
    })

@proff.route("/professional_ratings", methods=["GET"])
@login_required
def get_professional_ratings():
    professional_id = current_user.email  

    
    ratings = db.session.query(ServiceRequest.rating, db.func.count(ServiceRequest.rating)).filter(
        ServiceRequest.professional_email == professional_id, 
        ServiceRequest.rating.isnot(None)
    ).group_by(ServiceRequest.rating).all()

    # Convert ratings to a specific format
    rating_counts = {str(rate): count for rate, count in ratings}

    # ENSURE ALL RATINGS ARE INCLUDED
    full_ratings = {
        "5": rating_counts.get("5", 0),
        "4": rating_counts.get("4", 0),
        "3": rating_counts.get("3", 0),
        "2": rating_counts.get("2", 0),
        "1": rating_counts.get("1", 0)
    }

    return jsonify(full_ratings)