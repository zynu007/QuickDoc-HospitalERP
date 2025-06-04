# 🩺 QuickDoc – Doctor Appointment Booking System

QuickDoc is a full-stack web application for booking doctor appointments online. 
It features role-based dashboards, Google Calendar sync, blog functionality for doctors, and a responsive modern UI.
Designed to simulate a real-world health tech platform, QuickDoc was built as part of a full-stack learning journey using Django and Vue.js.

---

## 🚀 Features

### 🔐 Authentication & Roles
- Secure login, signup, and logout
- Role-based access: **Patient** and **Doctor**
- Only registered users can access core functionality

### 🗓 Appointment Booking
- Patients can search and filter doctors by specialization
- Book appointments directly from dashboard
- Google Calendar sync: Booked slots are auto-added to the doctor's linked calendar via OAuth

### 📰 Doctor Blog Platform
- Doctors can create, edit, delete blog posts
- Draft saving and later publishing supported
- Blog filtering by health topics (e.g., heart, cancer, diabetes)

### 📊 Dashboards
- Separate views and access for Patients, Doctors, Admins
- Doctors see their appointments, blogs, and calendar
- Patients manage bookings and browse doctor list

### 🎨 UI/UX
- Vue.js powered frontend with Material UI styling
- Responsive design for mobile/tablet/desktop
- Reusable UI components like cards, filters, and modals

---

## 🧰 Tech Stack

| Layer        | Tech                              |
|--------------|-----------------------------------|
| Frontend     | HTML, CSS, Bootstrap, JavaScript, Vue.js |
| Backend      | Django (Python)                   |
| Database     | MySQL                             |
| APIs & Auth  | Google OAuth2, Google Calendar API |
| Server       | Gunicorn + Whitenoise             |
| Deployment   | Render.com                        |
| Environment  | `python-dotenv` for env variables |

---

## 🧪 Requirements

See `requirements.txt` for full list. Key dependencies:

- `Django==5.1.6`
- `mysqlclient`
- `google-auth`, `google-api-python-client`
- `requests`, `requests-oauthlib`
- `gunicorn`, `whitenoise`
- `python-dotenv`

Install dependencies with:

```bash
pip install -r requirements.txt
