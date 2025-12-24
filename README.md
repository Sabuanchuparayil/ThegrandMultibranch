# Grand Gold & Diamonds - Multi-Branch Jewellery E-Commerce Platform

A comprehensive multi-region, multi-currency jewellery e-commerce platform built with Saleor (headless commerce) and Next.js.

## 🌍 Features

- **Multi-Region Support**: UK, UAE, and India
- **Multi-Currency**: GBP, AED, and INR with real-time exchange rates
- **Multi-Branch Management**: Manage inventory and operations across multiple physical stores
- **Branch-Specific Pricing**: Gold rates and making charges per region/branch
- **Tax Management**: VAT (UK), GST (India), VAT (UAE) with region-specific rules
- **Inventory Management**: Branch-level stock tracking, transfers, and low stock alerts
- **Order Management**: Branch assignment, fulfillment, and click-and-collect
- **Customer Management**: Profiles, loyalty points, and engagement
- **Real-time Dashboards**: Executive and branch-level KPIs and analytics

## 🏗️ Architecture

### Backend
- **Framework**: Django (Saleor)
- **Database**: PostgreSQL
- **Cache/Queue**: Redis + Celery
- **API**: GraphQL
- **Storage**: AWS S3 for media files

### Frontend
- **Admin Dashboard**: Next.js 16+ with TypeScript
- **Storefront**: Next.js 16+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Apollo Client (GraphQL)

## 📁 Project Structure

```
grand-gold-multibranch/
├── backend/                    # Saleor backend
│   ├── saleor/                # Saleor core
│   ├── saleor_extensions/     # Custom extensions (20 modules)
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile              # Railway deployment
│   └── runtime.txt
├── frontend/
│   ├── admin/                # Admin dashboard
│   ├── storefront/           # Customer storefront
│   └── shared/               # Shared types
└── docs/                     # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Git

### Backend Setup

```bash
cd backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Saleor
pip install git+https://github.com/saleor/saleor.git

# Copy environment file
cp .env.example .env  # Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup

#### Admin Dashboard

```bash
cd frontend/admin
npm install
npm run dev
```

#### Storefront

```bash
cd frontend/storefront
npm install
npm run dev
```

## 📚 Documentation

- [Railway Setup Guide](./RAILWAY_AND_GITHUB_SETUP.md) - Complete deployment guide
- [Backend Modules](./docs/FINAL_IMPLEMENTATION_SUMMARY.md) - Backend architecture
- [GraphQL API](./backend/GRAPHQL_INTEGRATION_COMPLETE.md) - API documentation
- [Admin Dashboard](./frontend/admin/README_DASHBOARDS.md) - Dashboard guide
- [Storefront](./frontend/storefront/STOREFRONT_COMPLETE.md) - Storefront documentation

## 🔧 Configuration

### Environment Variables

See `.env.example` files for required environment variables:

- Database credentials
- AWS S3 configuration
- Payment gateway keys
- Email settings
- Currency/Gold rate API keys

## 🚂 Deployment

### Railway Deployment

See [RAILWAY_AND_GITHUB_SETUP.md](./RAILWAY_AND_GITHUB_SETUP.md) for complete deployment instructions.

Quick steps:
1. Push code to GitHub
2. Create Railway project
3. Add PostgreSQL and Redis
4. Deploy backend services
5. Configure environment variables
6. Run migrations

## 📊 Modules

### Backend Extensions (20 modules)

1. **Regions** - Multi-region support
2. **Currency** - Currency and exchange rates
3. **Branches** - Branch/store management
4. **Inventory** - Stock management
5. **Pricing** - Gold rates and pricing rules
6. **Taxes** - Tax configuration
7. **Orders** - Order extensions
8. **Products** - Jewellery attributes
9. **Fulfillment** - Shipping and dispatch
10. **Returns** - Returns and refunds
11. **Customers** - Customer management
12. **Promotions** - Coupons and campaigns
13. **CMS** - Content management
14. **Notifications** - Email/SMS/WhatsApp
15. **Payments** - Payment integrations
16. **Invoices** - Invoice generation
17. **Reports** - Analytics and reports
18. **Integrations** - External integrations
19. **Audit** - Audit logging
20. **Permissions** - RBAC system

### Frontend Applications

- **Admin Dashboard**: 12 module interfaces with forms and data tables
- **Storefront**: Product catalog, checkout, account management

## 🔐 Security

- Environment variables for sensitive data
- Django secret key generation
- CORS configuration
- Authentication and authorization
- Audit logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

[Your License Here]

## 📞 Support

For issues and questions, please open an issue in the GitHub repository.

---

**Built with ❤️ for Grand Gold & Diamonds**
