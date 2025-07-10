# EyeKarthii Store 👓

A modern, responsive e-commerce web application for selling eyewear products. Built with simplicity, performance, and user-friendly design in mind.

---

## 🧰 Table of Contents

- [Demo](#-demo)  
- [Features](#-features)  
- [Tech Stack](#-tech-stack)  
- [Setup & Run](#-setup--run)  
- [Project Structure](#-project-structure)  
- [Usage](#-usage)  
- [Contributing](#-contributing)  
- [License](#-license)  

---

## 📺 Demo

- **Live Preview:** _[Add your live deployment link here]_  
- **Screenshots:**  
  - Product listing  
  - Cart page  
  - Orders page  

---

## ✨ Features

- 📦 **Product Listing** – Responsive grid with product images, names, prices, descriptions  
- 🛒 **Shopping Cart** – Add/remove items, view total, place orders  
- 📃 **Order Management** – View past orders with status and details  
- 🎨 **Modern UI** – Light/Dark mode toggle, clean design, accessible typography  
- 🔐 **User Auth** – Login/register, profile, logout  
- ✅ **Mobile-first** – Fully responsive layout for desktops, tablets, mobile  

---

## 🛠 Tech Stack

- **Backend:** Python (Flask / Django) or Node.js (Express) – choose your stack  
- **Frontend:** HTML5, CSS3 (custom or Bootstrap), JavaScript  
- **Templating:** Jinja2 (Flask/Django) or EJS (Express)  
- **Database:** MongoDB / PostgreSQL / MySQL  
- **Deployment:** Heroku / Vercel / AWS / DigitalOcean  

---

## 🚀 Setup & Run

1. **Clone the repo**  
   ```bash
   git clone https://github.com/karthii33/EyeKarthii.git
   cd EyeKarthii
2. **Install dependencies**

bash
Copy
Edit
# For Python/Flask
pip install -r requirements.txt

# For Node.js/Express
npm install
3. **Configure environment variables**
Create a .env file:

ini
Copy
Edit
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_uri
4 .**Initialize database**

bash
Copy
Edit
# Flask example
flask db upgrade
flask seed

# Node.js example
npm run migrate
npm run seed
5. **Start the server**

bash
Copy
Edit
# Flask
flask run

# Node
npm start
6. Visit: Open http://localhost:5000 in your browser

#📁 Project Structure
csharp
Copy
Edit
EyeKarthii/
│
├── templates/         # HTML templates
│   ├── layout.html    # Shared layout
│   ├── index.html     # Product listing
│   ├── cart.html
│   ├── orders.html
│   └── auth/          # login, register, profile
│
├── static/
│   ├── css/
│   └── js/            # Client-side scripts (e.g. mode-toggle)
│
├── models/            # ORM models (Product, User, Order)
├── routes/            # Route handlers
├── utils/             # Helper functions
└── app.py             # Flask or Express app entrypoint

