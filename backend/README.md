# Grand Gold Multi-Region Multi-Currency Backend

Backend implementation for The Grand Gold & Diamonds multi-branch jewellery e-commerce platform.

## Setup Instructions

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

#### Local PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE grandgold_db;
CREATE USER grandgold_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE grandgold_db TO grandgold_user;
\q
```

### 4. Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your actual configuration values.

### 5. Run Migrations

After Saleor project is initialized:

```bash
# Create migrations for custom apps
python manage.py makemigrations regions
python manage.py makemigrations currency
python manage.py makemigrations branches

# Run migrations
python manage.py migrate
```

## Project Structure

- `saleor_extensions/` - Custom Django apps extending Saleor
  - `regions/` - Region management (UK, UAE, India)
  - `currency/` - Multi-currency support
  - `branches/` - Branch/store management
  - `inventory/` - Multi-branch inventory
  - `pricing/` - Region & branch-specific pricing
  - `taxes/` - Region-specific tax compliance
  - `fulfillment/` - Branch fulfillment logic
  - `orders/` - Order extensions
  - `payments/` - Region-specific payment gateways
  - `reports/` - Analytics and reporting
  - `permissions/` - Role-based access control
  - `audit/` - Audit logging

## Railway Deployment

See the main plan document for Railway deployment instructions.

