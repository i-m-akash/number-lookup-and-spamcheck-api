Here’s a complete and professional `README.md` file for your **Number Lookup and Spam Check REST API (Django)** assignment. This follows production-level standards, includes instructions, project description, features, and setup guide.

---

```markdown
# 📱 Number Lookup and Spam Check API

A production-ready RESTful API built with **Django** and **Django REST Framework**, designed to support mobile apps that identify spam callers and lookup contact information by phone number or name.

---

## 🚀 Features

- ✅ User registration with phone, name, password (optional email)
- ✅ JWT-based authentication (secure login required for all actions)
- ✅ Add personal contacts (auto-import assumed)
- ✅ Global database combining all users and contacts
- ✅ Search by name (starts with > contains)
- ✅ Search by phone number (exact matches)
- ✅ Spam marking (even for non-registered numbers)
- ✅ Visibility rules for email (only if registered + mutual contact)
- ✅ Spam likelihood calculation
- ✅ Sample data population script for testing

---

## 🛠️ Tech Stack

- **Backend Framework:** Django 4+, Django REST Framework
- **Database:** PostgreSQL (can be switched to SQLite for local testing)
- **ORM:** Django ORM
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Security:** Password hashing, Auth checks, Rate limiting recommended

---

## 📦 Installation

> Recommended: Use a virtual environment

```bash
git clone https://github.com/i-m-akash/number-lookup-and-spamcheck-api.git
cd number-lookup-and-spamcheck-api
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 📂 Environment Setup

Create a `.env` file in the project root:

```ini
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

(Optional: Use PostgreSQL by setting `DATABASE_URL` accordingly)

---

## 🔧 Running the App

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 📊 Populate Sample Data

```bash
python manage.py populate_sample_data
```

This command generates:
- Fake registered users
- Contact books with overlapping phone numbers
- Marked spam entries for realistic spam scoring

---

## 🧪 API Endpoints

| Method | Endpoint                         | Description                       |
|--------|----------------------------------|-----------------------------------|
| POST   | `/api/register/`                | Register new user                 |
| POST   | `/api/token/`                   | Login to get access token         |
| GET    | `/api/search/name/?q=John`      | Search by name                    |
| GET    | `/api/search/phone/?q=98765`    | Search by phone number            |
| POST   | `/api/mark-spam/`               | Mark a number as spam             |
| GET    | `/api/profile/<phone>/`         | View user details (with filters)  |

> 📌 All endpoints require JWT token in headers unless registering or logging in.

---

## 🔐 Authentication Headers

Include this header for all authenticated routes:

```http
Authorization: Bearer <your-access-token>
```

---

## ✅ Production Considerations

- Input validation
- Rate limiting (via Django Ratelimit or DRF Throttling)
- Pagination on search results
- Indexing `name` and `phone_number` for fast search
- Email only returned on mutual contacts

---

## 📁 Folder Structure

```bash
number_lookup_api/
│
├── manage.py
├── core/                # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── commands/
│       └── populate_sample_data.py
├── requirements.txt
└── README.md
```
