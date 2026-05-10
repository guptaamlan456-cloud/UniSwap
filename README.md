# UniSwap — Student Marketplace

> The marketplace built for international students leaving Malaysia.
> Buy and sell furniture, electronics, textbooks and more — with urgency countdowns for students flying home soon.

## Local Development Setup

### Prerequisites

- Python 3.11+
- MySQL Server (install from https://dev.mysql.com/downloads/mysql/)

### 1. Install Python Dependencies

```bash
py -m pip install -r requirements.txt
```

### 2. Set Up MySQL Database

1. Install MySQL Server
2. Create a database named `uniswap_db`
3. Create a user `uniswap_user` with password `your_password` (or update `.env`)

### 3. Configure Environment

Copy `.env.example` to `.env` and update values if needed:

```bash
copy .env.example .env
```

The default `.env` should include:

```env
FLASK_APP=run.py
FLASK_ENV=development

SECRET_KEY=super-secret-key-12345

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=uniswap_db
MYSQL_USER=uniswap_user
MYSQL_PASSWORD=your_password

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 4. Initialize Database

```bash
py -m flask db init
py -m flask db migrate
py -m flask db upgrade
```

### 5. Seed Sample Data

Run the seed script to add test users and sample listings:

```bash
py seed_data.py
```

Sample accounts created:
- amira@example.com / password123
- daniel@example.com / password123
- lina@example.com / password123

### 6. Run the App

```bash
py -m flask run
```

Open at: http://localhost:5000

## Features

- User registration and login
- Create listings with images (Cloudinary)
- Browse listings with urgency countdowns
- In-app messaging
- University filtering

## Tech Stack

- Backend: Python + Flask
- Database: MySQL
- ORM: SQLAlchemy
- Authentication: Flask-Login
- Frontend: Bootstrap 5
- Image Storage: Cloudinary