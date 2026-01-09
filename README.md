# Green Getaway 🌿

Green Getaway is a Django-based web application designed to promote eco-friendly travel and sustainable tourism. The 
platform allows users to explore green destinations and book trips including city strolls and nature retreats via user-friendly interface.
The Stripe API is integrated to enable secure payments.

---

## 🚀 Features

* User authentication (registration, login, logout, password reset)
* Browse eco-friendly destinations, view trip details (length, duration, level and price)
* Responsive and accessible UI
* Admin panel for managing content
* Secure backend built with Django

---

## 🛠️ Technologies Used

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** SQLite (can be replaced with PostgreSQL/MySQL)
* **Authentication:** Django built-in auth system

---

## 📦 Installation & Setup

Follow these steps to run the project locally:

1. **Clone the repository**

   ```bash
   git clone https://github.com/LisaOz/GreenGetaway.git
   cd GreenGetaway
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   venv\\Scripts\\activate (for Mac: source venv/bin/activate)
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. Open your browser and go to:

   ```
   http://127.0.0.1:8000/
   ```

---

## 🔐 Admin Panel

Access the Django admin panel at:

```
http://127.0.0.1:8000/admin/
```

Use the superuser credentials created earlier to log in.

---

## 🧪 Testing

Run tests using:

```bash
python manage.py test
```


## 🔒 Security Considerations

* Follows Django security best practices
* Uses environment variables for sensitive settings (recommended for production)
* Protects against common vulnerabilities such as CSRF and SQL injection

---

## 🌱 Future Enhancements

* Integration with maps and external eco-tourism APIs
* Role-based access (e.g. hosts, travellers)
* Deployment to cloud platforms (e.g. Heroku, AWS)

---

## 📚 References

* Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
* OWASP Top 10
* NIST Secure Software Development Framework

---

## 👤 Author

Developed by *LisaOz*

---

## 📄 License

This project is for educational purposes. It is licensed under the MIT License and may be freely used, modified, and distributed
