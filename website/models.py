from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    email = db.Column(db.String(100), unique=True, nullable=False,primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False) 
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(10), default="active")
    def get_id(self):
        return self.email
    

def create_admin(app):
    with app.app_context():
        if not User.query.filter_by(email='admin@gmail.com').first():
            admin = User(
                email='admin@gmail.com',
                password='123456',  
                full_name='ADMIN',
                role='Admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
        else:
            print("Admin user already exists.")

class Professional(db.Model, UserMixin):
    email = db.Column(db.String(100), unique=True, nullable=False,primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    service_name = db.Column(db.String(100),db.ForeignKey('service.name'), nullable=True)  
    address = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    approved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(10), default="active")
    def get_id(self):
        return self.email

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    pin_code = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f"<Service {self.name}>"
        
    # Add this method
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "base_price": self.base_price,
            "description": self.description,
            "pin_code": self.pin_code,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S") if self.date_created else None
        }

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)  
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    professional_email = db.Column(db.String(100), db.ForeignKey('professional.email'), nullable=False)  
    status = db.Column(db.String(20), default='Pending')
    remarks = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='service_requests')
    service = db.relationship('Service', backref='service_requests')
    professional = db.relationship('Professional', backref='service_requests')

    def __repr__(self):
        return f'<ServiceRequest {self.id} - {self.status}>'

    def to_dict(self):
        return {
            "id": self.id,
            "user_email": self.user_email,
            "service_id": self.service_id,
            "professional_email": self.professional_email,
            "status": self.status,
            "remarks": self.remarks,
            "rating": self.rating,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        }