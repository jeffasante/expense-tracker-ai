# AI-Powered Expense Tracker API

A Django REST API with AI-powered expense categorization and insights generation for Ladder Financial Systems assessment.

## Assessment Requirements Fulfilled

**Core Expense Tracking API**
- RESTful endpoints for CRUD operations (amount, description, category, date)
- JWT-based user authentication
- Comprehensive error handling
- Proper request/response formats

**AI-Powered Features**
- **Expense Categorization**: Rule-based ML model with keyword matching
- **Manual Override**: Users can override AI predictions
- **Insights & Summaries**: Monthly/weekly spending, top categories, anomaly detection

**Testing**
- Unit tests for all endpoints including AI features
- Integration tests for complete workflows
- Deterministic AI tests with fixed predictions

**Documentation**
- Complete Swagger/OpenAPI 3.0 specification
- Detailed API documentation with examples
- Clear setup and usage instructions

## Quick Start

### Option 1: Docker (Recommended)
```bash
cd expense-tracker-ai
docker-compose up --build
```

### Quick Test Credentials
For immediate testing, use these pre-configured credentials:
```json
{
  "email": "test@example.com",
  "password": "testpass123"
}
```
**Access Points:**
- Demo Login: `http://localhost:8000/demo/login/`
- API Docs: `http://localhost:8000/api/docs/` (use JWT token from login)

### Option 2: Local Setup
```bash
./setup.sh
# OR manually:
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Option 3: Step by Step
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Setup database
python manage.py makemigrations
python manage.py migrate

# 4. Run server
python manage.py runserver
```

## API Documentation

- **Interactive Docs**: http://localhost:8000/api/docs/
- **OpenAPI Spec**: `/backend/docs/openapi.yaml`
- **Admin Panel**: http://localhost:8000/admin/

## Testing

```bash
# Run all tests
cd backend
python manage.py test

# Run specific test modules
python manage.py test users.tests
python manage.py test expenses.tests
python manage.py test ai.tests

# Run integration tests
cd ..
python -m pytest tests/test_endpoints.py
```

## Architecture & Design

### Modular Structure
```
backend/
├── config/          # Django project settings
├── users/           # Authentication & user management
├── expenses/        # Core expense CRUD operations
├── ai/              # AI categorization & insights pipeline
└── docs/            # API documentation
```

### AI Pipeline Design
- **Categorizer**: Rule-based keyword matching with fallback
- **Insights Generator**: Statistical analysis for summaries and anomalies
- **Scalable**: Easy to swap ML models or add new AI features
- **Deterministic**: Consistent results for testing

### Key Design Decisions
1. **JWT Authentication**: Stateless, scalable auth
2. **Rule-based AI**: Simple, explainable, fast categorization
3. **Modular Apps**: Clean separation of concerns
4. **Comprehensive Testing**: Unit + integration coverage
5. **Docker Support**: Easy deployment and development

## Key Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Expenses
- `GET /api/expenses/` - List expenses (with filtering)
- `POST /api/expenses/` - Create expense
- `GET /api/expenses/{id}/` - Get expense details
- `PUT /api/expenses/{id}/` - Update expense
- `DELETE /api/expenses/{id}/` - Delete expense

### AI Features
- `POST /api/ai/categorize/` - Categorize expense description
- `POST /api/ai/auto-categorize/` - Auto-categorize existing expense
- `GET /api/ai/insights/` - Get spending insights and anomalies

## Example Usage

### 1. Register & Login
```bash
# Quick Login (test credentials)
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Or register new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user","password":"pass123","password_confirm":"pass123"}'
```

### 2. Create Expense
```bash
curl -X POST http://localhost:8000/api/expenses/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":"58.00","description":"Waakye at chop bar","category":"food","date":"2024-01-15"}'
```

### 3. AI Categorization
```bash
curl -X POST http://localhost:8000/api/ai/categorize/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description":"Uber ride to airport"}'
```

### 4. Get Insights
```bash
curl -X GET http://localhost:8000/api/ai/insights/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **AI/ML**: Scikit-learn, NumPy, Pandas
- **Documentation**: drf-spectacular (OpenAPI 3.0)
- **Database**: SQLite (development), PostgreSQL ready
- **Testing**: Django TestCase, REST Framework test client
- **Deployment**: Docker, Docker Compose

## AI Features Explained

### Expense Categorization
- **Method**: Rule-based keyword matching
- **Categories**: Food, Transport, Shopping, Entertainment, Bills, Healthcare, Education, Travel, Other
- **Confidence Scoring**: Based on keyword matches
- **Fallback**: Defaults to 'other' category
- **Override**: Users can manually correct predictions

### Insights & Analytics
- **Monthly Summaries**: Total spending, expense count, averages
- **Top Categories**: Ranked by spending amount
- **Anomaly Detection**: Statistical outliers using z-score
- **Spending Trends**: Week-over-week analysis

## Production Considerations

### Security
- JWT token expiration and refresh
- User input validation and sanitization
- CORS configuration
- Environment variable management

### Scalability
- Modular AI pipeline (easy to swap models)
- Database indexing on user and date fields
- Pagination for large datasets
- Caching opportunities for insights

### Monitoring
- Comprehensive error handling
- Logging for AI predictions
- API performance metrics
- User activity tracking

---

**Built for Ladder Financial Systems Backend Engineering Assessment**

*Demonstrates: Django expertise, AI/ML integration, API design, testing practices, and production-ready code structure.*