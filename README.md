# Austrian Library HUFS

This project is a web-based library management system for the Austrian Library at Hankuk University of Foreign Studies (HUFS). It features a Django backend and a React frontend.

## Project Structure

```text
.
├── backend/            # Django Backend
│   ├── common/         # Common utilities
│   ├── config/         # Django core configuration
│   ├── library/        # Library management logic
│   ├── manager/        # Admin/Manager views
│   ├── members/        # User and authentication
│   └── manage.py       # Django management script
├── frontend/           # React Frontend (Vite)
│   ├── src/
│   │   ├── assets/     # Images and static assets
│   │   ├── api/        # API client configuration
│   │   └── ...         # React components
│   └── package.json    # Frontend dependencies and scripts
├── docs/               # Documentation and tasks
├── requirements.txt    # Unified Python dependencies
└── README.md           # This file
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (for production/local DB)

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   cd backend
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Development

The frontend is configured with `concurrently` to run both the frontend and backend development servers if needed. See `frontend/package.json` for details.

## Tech Stack

- **Frontend**: React, Vite, Axios, Zustand
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL (Neon DB)
- **Deployment**: Vercel (Frontend), Render (Backend)
