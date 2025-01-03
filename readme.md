# DevRecruit Project

DevRecruit is a full-stack application designed to streamline the recruitment process. This project consists of two main components:

1. **Backend**: A Django REST Framework-based API (`devrecruit-server`).
2. **Frontend**: A React and TypeScript web application (`devrecruit-client`).

## Project Structure
```
.
├── devrecruit-server
│   ├── Dockerfile
│   ├── manage.py
│   ├── db.sqlite3
│   └── (other Django files)
│
└── devrecruit-client
    ├── Dockerfile
    ├── package.json
    ├── tsconfig.json
    ├── public
    ├── src
    └── (other React files)

```

## Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/devrecruit.git
cd devrecruit
```

### 2. Build and Run the Application

Run the following command from the project root:
```bash
docker-compose up --build
```

This command will:
- Build and run the Django backend on `http://localhost:8000`.
- Build and serve the React frontend on `http://localhost:3000`.

### 3. Access the Application
- **Frontend**: Visit `http://localhost:3000`
- **Backend API**: Visit `http://localhost:8000`

## Development

### Backend Development
1. Navigate to the backend folder:
   ```bash
   cd devrecruit-server
   ```
2. Run the Django development server locally:
   ```bash
   python manage.py runserver
   ```
3. Access the API at `http://127.0.0.1:8000`.

### Frontend Development
1. Navigate to the frontend folder:
   ```bash
   cd devrecruit-client
   ```
2. Install dependencies (if not already installed):
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. Access the frontend at `http://localhost:3000`.

## Testing
### Backend Tests
Run the following command to execute tests for the backend:
```bash
python manage.py test
```

### Frontend Tests
Run the following command to execute tests for the frontend:
```bash
npm test
```

## Deployment
For production, the backend is served via Django's WSGI interface, and the frontend is served using Nginx. Ensure the `.env` files for both components are correctly configured before deployment.

## File Breakdown
### Backend
- `Dockerfile`: Instructions for building the backend Docker image.
- `manage.py`: Django's management script.

### Frontend
- `Dockerfile`: Instructions for building the frontend Docker image.
- `package.json`: Node.js dependencies and scripts.
- `tsconfig.json`: TypeScript configuration.

## Acknowledgments
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Docker](https://www.docker.com/)
