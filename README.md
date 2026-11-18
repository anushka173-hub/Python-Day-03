# Employee REST API

A REST API built using FastAPI, SQLAlchemy, and PostgreSQL. This project supports employee, department, leave, and authentication operations.

## 1. Prerequisites

Before running the project, install:

- Python 3.14+
- PostgreSQL
- Docker Desktop (for Docker execution)

## 2. Project Setup

Clone or download the project and navigate to the project directory:

```powershell
cd "D:\PYTHON\Python Day 03"
```

## 3. Local Execution

### Step 1: Create a virtual environment

```powershell
python -m venv venv
```

### Step 2: Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/YOUR_DATABASE
SECRET_KEY=YOUR_SECRET_KEY
```

Replace the placeholders with your PostgreSQL credentials and database name.

### Step 5: Run the application

```powershell
uvicorn app.main:app --reload
```

### Step 6: Access the API documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 4. Docker Execution

### Step 1: Start Docker Desktop

Make sure Docker Desktop is running.

### Step 2: Configure Docker environment variables

Create `.env.docker` in the project root:

```env
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@host.docker.internal:5432/YOUR_DATABASE
SECRET_KEY=YOUR_SECRET_KEY
```

**Note:** Use `host.docker.internal` instead of `localhost` because PostgreSQL is running on the Windows host, outside the Docker container.

### Step 3: Build the Docker image

```powershell
docker build -t employee-api .
```

### Step 4: Run the Docker container

```powershell
docker run -d --name employee-api-container -p 8000:8000 --env-file .env.docker employee-api
```

### Step 5: Check the running container

```powershell
docker ps
```

### Step 6: View application logs

```powershell
docker logs employee-api-container
```

### Step 7: Access Swagger UI

Open:

http://localhost:8000/docs

## 5. Docker Container Management

Stop the container:

```powershell
docker stop employee-api-container
```

Start an existing container:

```powershell
docker start employee-api-container
```

Remove a stopped container:

```powershell
docker rm employee-api-container
```

Remove the Docker image:

```powershell
docker rmi employee-api
```

## 6. Important Notes

- PostgreSQL must be running before starting the API.
- Local execution uses `localhost` in the database URL.
- Docker execution uses `host.docker.internal` to connect to PostgreSQL on Windows.
- Never commit `.env` or `.env.docker` files containing actual secrets.
- The `.dockerignore` file prevents environment files and unnecessary development files from being included in the Docker build context.
- Local execution and Docker execution both use the same application source code and database.

