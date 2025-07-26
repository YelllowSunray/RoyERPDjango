# Pluviago ERP System

A comprehensive Enterprise Resource Planning (ERP) system designed for pharmaceutical and biotechnology companies, with a focus on inventory management, quality assurance, and traceability.

## 🌟 Features

### Master Data Management
- **Item Records**: Complete product catalog with specifications, hazard classifications, and traceability requirements
- **Supplier Management**: Vendor information, certifications, and approval workflows
- **Customer Management**: Customer profiles, shipping requirements, and QA approval processes
- **Product Management**: Finished product definitions with version control and specifications
- **Storage Management**: Warehouse zones and locations with environmental controls

### Inventory Management
- **Transaction Ledger**: Complete audit trail of all inventory movements
- **Batch Tracking**: Full batch-level traceability with expiry management
- **Storage Assignment**: Automated storage location assignment based on hazard compatibility
- **Stock Levels**: Real-time inventory tracking and low stock alerts

### Quality Assurance
- **QA Review System**: Document verification and batch approval workflows
- **Document Management**: COA, SDS, and specification tracking
- **Compliance Tracking**: Regulatory compliance and audit trail maintenance
- **Unit-Level QA**: Individual unit inspection and disposition

### Reports and Analytics
- **Dashboard**: Real-time overview of system status and key metrics
- **Inventory Reports**: Stock levels, expiry tracking, and movement analysis
- **QA Reports**: Review status, compliance metrics, and document tracking
- **Traceability Reports**: Complete chain of custody for all materials

## 🏗️ System Architecture

### Database Schema
The system follows the A2.1, A2.2, and A2.3 document specifications:

- **A2.1 - Master Product Data Structures**: Defines all master data tables and relationships
- **A2.2 - QA Review Table**: Quality assurance workflows and document verification
- **A2.3 - Master Inventory Transaction Ledger**: Complete transaction tracking and audit trail

### Key Models
- `ItemRecord`: Product specifications and traceability requirements
- `Supplier`: Vendor information and approval status
- `Customer`: Customer profiles and shipping requirements
- `Batch`: Batch-level tracking with expiry and QA status
- `InventoryTransaction`: Complete transaction history
- `QAReview`: Quality assurance workflows and document verification
- `StorageZone` & `StorageLocation`: Warehouse management

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 4.0+
- SQLite (for development) or PostgreSQL (for production)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd erp_project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the system**
   - Main application: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/

### Sample Data
To populate the system with sample data for testing:
```bash
python manage.py populate_sample_data
```

## 📋 Usage Guide

### Dashboard
The main dashboard provides:
- Summary statistics (total items, suppliers, customers, batches)
- Recent transactions
- Pending QA reviews
- Expiring batches alerts
- Low stock warnings

### Master Data Management

#### Items
- Navigate to **Items** in the sidebar
- View all items with search and filter capabilities
- Click on an item to see detailed information
- Use the admin interface for creating new items

#### Suppliers
- Navigate to **Suppliers** in the sidebar
- View approved and pending suppliers
- Access supplier details and related products
- Manage supplier approvals and reviews

#### Customers
- Navigate to **Customers** in the sidebar
- View customer profiles and shipping requirements
- Manage customer approvals and QA requirements

### Inventory Transactions

#### Viewing Transactions
- Navigate to **Transactions** in the sidebar
- Use search and filters to find specific transactions
- View transaction details including QA status and document verification

#### Creating Transactions
- Click **New Transaction** button
- Select transaction type (receipt, issue, transfer, etc.)
- Fill in required information
- Submit for processing

### Quality Assurance

#### QA Reviews
- Navigate to **QA Reviews** in the sidebar
- View pending and completed reviews
- Access review details and document verification status

#### Creating QA Reviews
- Click **New QA Review** button
- Select batch and verify documents
- Record review outcomes and comments

### Reports

#### Inventory Report
- Navigate to **Reports > Inventory Report**
- View current stock levels and batch information
- Track inventory movements and trends

#### Expiry Report
- Navigate to **Reports > Expiry Report**
- View batches expiring within 30 and 60 days
- Plan inventory rotation and disposal

## 🔧 Configuration

### Settings
Key configuration options in `settings.py`:
- Database configuration
- Static files settings
- Admin interface customization
- Security settings

### Customization
The system is designed to be easily customizable:
- Add new transaction types
- Modify QA workflows
- Extend master data fields
- Customize reports and dashboards

## 📊 Data Flow

### Receipt Process
1. **Create Item Record** (if new item)
2. **Receive Material** (create transaction)
3. **QA Review** (verify documents and specifications)
4. **Storage Assignment** (assign to appropriate location)
5. **Batch Creation** (create batch record)

### Issue Process
1. **Select Item and Batch**
2. **Create Issue Transaction**
3. **Update Stock Levels**
4. **Record Usage Information**

### Quality Assurance
1. **Document Verification** (COA, SDS, specifications)
2. **Batch Inspection** (visual and specification checks)
3. **QA Review Creation** (record findings and outcomes)
4. **Approval/Rejection** (update batch status)

## 🔒 Security and Compliance

### User Management
- Role-based access control
- User authentication and authorization
- Audit trail for all user actions

### Data Integrity
- Foreign key constraints
- Validation rules
- Transaction rollback capabilities

### Compliance Features
- Complete audit trail
- Document version control
- Regulatory reporting capabilities
- GMP compliance tracking

## 🛠️ Development

### Adding New Features
1. Create models in `inventory/models.py`
2. Add views in `inventory/views.py`
3. Create templates in `inventory/templates/`
4. Update URLs in `inventory/urls.py`
5. Add admin interface in `inventory/admin.py`

### Testing
```bash
python manage.py test inventory
```

### Database Migrations
```bash
python manage.py makemigrations inventory
python manage.py migrate
```

## 📞 Support

For technical support or questions:
- Check the documentation
- Review the admin interface
- Contact the development team

## 📄 License

This project is proprietary software developed for Pluviago Biotech.

---

**Pluviago ERP System** - Comprehensive inventory and quality management for pharmaceutical and biotechnology companies. 