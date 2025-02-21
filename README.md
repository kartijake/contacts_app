# Contacts App

This repository contains a full-stack application with a Django backend and a React frontend using Vite. The application is containerized for production using Docker and deployed using `docker-compose`.

---

## 📌 Prerequisites

Before setting up the project, ensure you have the following installed on your system:

- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) (optional)
- [Git](https://git-scm.com/downloads)

---

## 📌 Cloning the Repository

```sh
git clone https://github.com/kartijake/contacts_app.git
cd contacts_app
```

---

## 🛠 Setting Up the Backend (Django)

### Navigate to the API directory

```sh
cd api
```

### Create a Virtual Environment (Recommended)

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Create a .env File

Copy the provided `.env.example` file and rename it to `.env` in the `api` directory.

```sh
cp .env.example .env
```

Open the `.env` file and update the values as needed.

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Apply Migrations

```sh
python manage.py migrate
```

### Start the Development Server

```sh
python manage.py runserver
```

### API Documentation

The backend API documentation is available at:

- Swagger: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
- Redoc: [http](http://127.0.0.1:8000/api/redoc)[://127.0.0.1:8000/api/redoc](http://127.0.0.1:8000/redoc)

---

## 🎨 Setting Up the Frontend (React + Vite)

### Navigate to the Contacts directory

```sh
cd contacts
```

### Install Dependencies

```sh
npm install
```

### Create a .env File

Copy the provided `.env.example` file and rename it to `.env` in the `contacts` directory.

```sh
cp .env.example .env
```

Open the `.env` file and update the values as needed.

### Start the Development Server

```sh
npm run dev
```

The React app should now be accessible at [http://localhost:5173](http://localhost:5173)[.](http://localhost:5173)

### Build for Production

```sh
npm run build
```

### Preview build

```sh
npm run preview
```

### Screenshots

#### Frontend Application

![contacts_login](https://github.com/kartijake/contacts_app/blob/master/screenshots/contacts_1.png?raw=true)

---

![contacts_list](https://github.com/kartijake/contacts_app/blob/master/screenshots/contacts_2.png?raw=true)

---

![add_contacts](https://github.com/kartijake/contacts_app/blob/master/screenshots/contacts_3.png?raw=true)

Refer to these screenshots for a visual reference of the application.

#### Backend API Documentation

![api_doc](https://github.com/kartijake/contacts_app/blob/master/screenshots/apiDoc_1.png?raw=true)

---

![api_doc](https://github.com/kartijake/contacts_app/blob/master/screenshots/apiDoc_1.png?raw=true)

---

## 🚀 Running the Application in Production using Docker

### Install Docker and Docker Compose on a VPS

#### Step 1: Update System Packages

```sh
sudo apt update && sudo apt upgrade -y
```

#### Step 2: Install Docker

```sh
sudo apt install -y docker.io
```

#### Step 3: Enable and Start Docker

```sh
sudo systemctl enable docker
sudo systemctl start docker
```

#### Step 4: Install Docker Compose

```sh
sudo apt install -y docker-compose
```

### Build and Run the Application on the VPS

```sh
git clone https://github.com/kartijake/contacts_app.git
cd contacts_app/docker
docker-compose up --build -d
```

This will start both the backend and frontend services in production mode.

**Note:** Ensure you update the server IP or domain in `<root-dir>/docker/nginx/nginx.conf` before deploying.

### Stopping the Services

```sh
docker-compose down
```

---

## 🌎 Deploying to Production

### Recommended Cloud Platform: **AWS**

- **Backend:** Deploy Django API using **AWS Elastic Beanstalk** or **EC2**
- **Frontend:** Deploy React app on **AWS S3 + CloudFront**
- **Database:** The application uses SQLite as the database, so no external database setup is required.

### Steps for Deployment

1. **Setup Environment Variables:** Ensure `.env` files are properly configured.

2. **Deploy Django Backend:**

   - Use `gunicorn` as the production WSGI server
   - Configure Nginx as a reverse proxy

     **Note:** Check `<root-dir>/docker/nginx/nginx.conf` for reverse proxy sample.

3. **Deploy React Frontend:**
   - Build React using `npm run build`
   - Upload the `dist` folder to an S3 bucket
   - Use AWS CloudFront for fast global delivery
   - **Note:** You might need to adjust the CORS policies in S3.

### Use Docker for Deployment (optional)

- Push images to AWS Elastic Container Registry (ECR)
- Deploy using AWS ECS with Fargate

### Additional Considerations

- **Logging & Monitoring:** Use AWS CloudWatch for logs and monitoring
- **Security:** Set up proper IAM roles and security groups
- **CI/CD:** Implement GitHub Actions for automated deployment

---
