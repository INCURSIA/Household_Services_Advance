from flask_mail import Message
from flask import current_app, render_template_string
from datetime import datetime
from website.models import Professional, User, ServiceRequest
from website import celery
import os, csv

@celery.task
def send_daily_reminder():
    """ Sends daily reminders to professionals about pending service requests. """
    from website import db, mail
    with current_app.app_context():
        professionals = Professional.query.all()
        for professional in professionals:
            pending_request = ServiceRequest.query.filter_by(
                professional_email=professional.email, status='Pending'
            ).first()
            
            if pending_request:
                msg = Message(
                    subject="Reminder: Pending Service Requests",
                    sender="noreply@example.com",
                    recipients=[professional.email],
                    body="You have pending service requests. Please review them."
                )
                mail.send(msg)
        
        print(f"✅ Daily reminder sent at {datetime.now()}")

@celery.task
def send_monthly_report():
    """ Sends a monthly report to customers about their service requests. """
    from website import db, mail
    with current_app.app_context():
        customers = User.query.all()
        for customer in customers:
            total_requests = ServiceRequest.query.filter_by(user_email=customer.email).count()
            completed_requests = ServiceRequest.query.filter_by(user_email=customer.email, status="Completed").count()
            pending_requests = total_requests - completed_requests

            html_body = render_template_string(
                """
                <html>
                    <head>
                        <style>
                            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; text-align: center; }
                            .container { max-width: 600px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); margin: auto; }
                            h2 { color: #2c3e50; }
                            ul { text-align: left; padding: 0; list-style: none; }
                            li { background: #ecf0f1; padding: 10px; margin: 5px 0; border-radius: 5px; }
                            .footer { margin-top: 20px; font-size: 14px; color: #7f8c8d; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h2>📊 Monthly Activity Report</h2>
                            <p>Hello <strong>{{ name }}</strong>,</p>
                            <p>Here is your service activity summary for this month:</p>
                            <ul>
                                <li><strong>Total Services Requested:</strong> {{ total }}</li>
                                <li><strong>Completed Services:</strong> {{ completed }}</li>
                                <li><strong>Pending Services:</strong> {{ pending }}</li>
                            </ul>
                            <p>Thank you for using our service! 🚀</p>
                            <div class="footer">This is an automated email. Please do not reply.</div>
                        </div>
                    </body>
                </html>
                """,
                name=customer.full_name,
                total=total_requests,
                completed=completed_requests,
                pending=pending_requests
            )

            msg = Message(
                subject="Monthly Activity Report",
                sender="noreply@example.com",
                recipients=[customer.email],
                html=html_body
            )
            mail.send(msg)
        
        print(f"✅ Monthly report sent at {datetime.now()}")

@celery.task
def export_closed_requests(admin_email):
    """Exports closed service requests to CSV and sends an email alert."""
    from website import db, mail
    with current_app.app_context():
        try:
            # Fetch closed service requests
            closed_requests = ServiceRequest.query.filter_by(status="Closed").all()

            # Define CSV file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"closed_requests_{timestamp}.csv"
            filepath = os.path.join("website/static/exports", filename)

            # Ensure export folder exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # Write data to CSV
            with open(filepath, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Service ID", "Customer ID", "Professional ID", "Date of Request", "Remarks"])

                for request in closed_requests:
                    writer.writerow([request.id, request.user_email, request.professional_email, request.date_created, request.remarks])

            # Send email alert with download link
            msg = Message(
                subject="Service Requests Exported",
                sender="noreply@example.com",
                recipients=[admin_email],
                body=f"The export has been completed. You can download it from:\n\n{current_app.config['BASE_URL']}/static/exports/{filename}"
            )
            mail.send(msg)

            print(f"✅ CSV Export Done: {filename}")
            return filepath
        except Exception as e:
            print(f"❌ CSV Export Failed: {e}")
            return None