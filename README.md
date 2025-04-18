#  Household Services Application - V2

A multi-role, end-to-end household service platform built using **Flask**, **VueJS**, **SQLite**, **Redis**, **Celery**, and **Bootstrap**. This app provides a complete solution for connecting customers with verified service professionals and enables admin-level monitoring and batch task automation.

---

##  Features

###  Role-Based Access
- **Admin** (Superuser - no registration required)
- **Service Professionals** (register, get verified by admin)
- **Customers** (register and book services)

---

###  Admin Functionalities
- Login & Admin Dashboard
- Manage and monitor customers and service professionals
- Approve/reject professional registrations after profile doc verification
- Create, update, delete services with base pricing
- Block/unblock users based on reviews or fraud detection
- Trigger CSV export of service records

---

###  Service Professional Functionalities
- Login/Register
- View & Accept/Reject service requests
- View own accepted services
- Mark service as completed (wait for customer to close it)
- View ratings and reviews

---

###  Customer Functionalities
- Login/Register
- Search services by name or pin code
- Create and manage service requests
- Close requests and leave reviews after completion

---

##  Tech Stack

| Layer       | Tech Used                            |
|-------------|--------------------------------------|
| Backend     | Flask + Flask-Login (Session-based auth) |
| Frontend    | Vue.js + Bootstrap                   |
| Database    | SQLite                               |
| Caching     | Redis                                |
| Task Queue  | Celery (uses Redis as broker)        |
| Async Jobs  | Daily reminders, Monthly reports, CSV export |

---

##  Authentication & Authorization

- Handled using **Flask-Login**.
- Each user has a `role` (admin, customer, professional).
- Admin has root access; others must register/login.

---

##  Batch Jobs

### 1. **Daily Reminder**
- Sends reminders to service professionals for pending tasks via Mail/SMS/Google Chat.

### 2. **Monthly Report**
- Auto-generates monthly activity reports for customers via HTML or PDF and sends via email on the 1st of each month.

### 3. **CSV Export**
- Admin can trigger a background job to export all closed service requests as CSV.
- Alert sent to admin upon completion.

---

##  Installation & Setup

###  Prerequisites

- Python 3.9+
- Node.js + npm
- Redis server, Celery, Celery beats
- Mailhog

---

### Setup
## Frontend
```bash
git clone  https://github.com/INCURSIA/Household_Services_Advance.git
cd frontend
npm install
npm run serve
```
## Backend
```bash
#open a diffrent terminal to run backend
pip install -r requirements.txt
python main.py
```
## Backend Jobs
```bash
#wsl terminal
redis-server # 1st terminal
celery -A website.celery worker --loglevel=info # 2nd terminal 
celery -A website.celery beat --loglevel=info # 3rd terminal
```
## Mail hog
```bash
#wsl terminal 
./MailHog # will run on http://localhost:8025

