from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from inventory.models import (
    Supplier, ItemRecord, Product, ProductVersion, SupplierProduct, Batch,
    StorageZone, StorageLocation, Customer, QAReview, QAReviewUnit, InventoryTransaction
)

class Command(BaseCommand):
    help = 'Populate the database with sample data for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Storage Zones
        self.create_storage_zones()
        
        # Create Suppliers
        self.create_suppliers()
        
        # Create Items
        self.create_items()
        
        # Create Products
        self.create_products()
        
        # Create Supplier Products
        self.create_supplier_products()
        
        # Create Customers
        self.create_customers()
        
        # Create Batches
        self.create_batches()
        
        # Create QA Reviews
        self.create_qa_reviews()
        
        # Create Transactions
        self.create_transactions()
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_storage_zones(self):
        zones = [
            {
                'zone_id': 'ZONE-CHEM-001',
                'zone_name': 'Chemical Storage Zone 1',
                'temperature_range': '20-25°C',
                'humidity_controlled': True,
                'hazard_compatibility': 'Flammable, Corrosive',
                'default_for_category': 'Chemical'
            },
            {
                'zone_id': 'ZONE-BIO-001',
                'zone_name': 'Biological Storage Zone 1',
                'temperature_range': '2-8°C',
                'humidity_controlled': True,
                'hazard_compatibility': 'Biohazard',
                'default_for_category': 'Biological'
            },
            {
                'zone_id': 'ZONE-PACK-001',
                'zone_name': 'Packaging Storage Zone 1',
                'temperature_range': '15-30°C',
                'humidity_controlled': False,
                'hazard_compatibility': 'None',
                'default_for_category': 'Packaging'
            }
        ]
        
        for zone_data in zones:
            zone, created = StorageZone.objects.get_or_create(
                zone_id=zone_data['zone_id'],
                defaults=zone_data
            )
            if created:
                self.stdout.write(f'Created storage zone: {zone.zone_name}')
        
        # Create storage locations
        locations = [
            {'location_id': 'LOC-CHEM-A1', 'zone_id': 'ZONE-CHEM-001', 'rack_shelf': 'Rack 1, Shelf A', 'max_capacity': '100 bottles'},
            {'location_id': 'LOC-CHEM-A2', 'zone_id': 'ZONE-CHEM-001', 'rack_shelf': 'Rack 1, Shelf B', 'max_capacity': '100 bottles'},
            {'location_id': 'LOC-BIO-A1', 'zone_id': 'ZONE-BIO-001', 'rack_shelf': 'Rack 1, Shelf A', 'max_capacity': '50 bottles'},
            {'location_id': 'LOC-PACK-A1', 'zone_id': 'ZONE-PACK-001', 'rack_shelf': 'Rack 1, Shelf A', 'max_capacity': '200 boxes'},
        ]
        
        for loc_data in locations:
            zone = StorageZone.objects.get(zone_id=loc_data['zone_id'])
            location, created = StorageLocation.objects.get_or_create(
                location_id=loc_data['location_id'],
                defaults={
                    'zone_id': zone,
                    'rack_shelf': loc_data['rack_shelf'],
                    'max_capacity': loc_data['max_capacity']
                }
            )
            if created:
                self.stdout.write(f'Created storage location: {location.location_id}')

    def create_suppliers(self):
        suppliers = [
            {
                'supplier_id': 'SUP-ALGAMO',
                'supplier_name': 'Algamo S.R.O.',
                'business_unit': '',
                'address': 'Czech Republic',
                'country_of_origin': 'CZ',
                'certifications': 'GMP, ISO-9001',
                'approved': True,
                'approved_on': timezone.now().date(),
                'last_reviewed_on': timezone.now().date(),
                'review_frequency': '1 year',
                'notes': 'Reliable supplier for biological materials'
            },
            {
                'supplier_id': 'SUP-CHEMCO',
                'supplier_name': 'Chemical Co. Ltd.',
                'business_unit': '',
                'address': 'Germany',
                'country_of_origin': 'DE',
                'certifications': 'ISO-9001, ISO-14001',
                'approved': True,
                'approved_on': timezone.now().date(),
                'last_reviewed_on': timezone.now().date(),
                'review_frequency': '6 months',
                'notes': 'High-quality chemical supplier'
            },
            {
                'supplier_id': 'SUP-PACKAGING',
                'supplier_name': 'Packaging Solutions Inc.',
                'business_unit': '',
                'address': 'USA',
                'country_of_origin': 'US',
                'certifications': 'ISO-9001',
                'approved': True,
                'approved_on': timezone.now().date(),
                'last_reviewed_on': timezone.now().date(),
                'review_frequency': '1 year',
                'notes': 'Packaging materials supplier'
            }
        ]
        
        for supplier_data in suppliers:
            supplier, created = Supplier.objects.get_or_create(
                supplier_id=supplier_data['supplier_id'],
                defaults=supplier_data
            )
            if created:
                self.stdout.write(f'Created supplier: {supplier.supplier_name}')

    def create_items(self):
        items = [
            {
                'item_record_id': 'CHE-SOL-ETH-001',
                'item_name': 'Ethanol 99.9%',
                'unit_of_measure': 'L',
                'category': 'Chemical',
                'subtype': 'Solvent',
                'grade': 'USP',
                'hazard_class': 'Flammable',
                'chemical_family': 'Alcohols',
                'contamination_risk': 'Medium',
                'critical_to_product': True,
                'qa_required': True,
                'traceability_level': 'Batch-level',
                'sds_mandatory': True,
                'coa_mandatory': True,
                'spec_required': True
            },
            {
                'item_record_id': 'BIO-RM-ALG-001',
                'item_name': 'Algae Extract',
                'unit_of_measure': 'kg',
                'category': 'Biological',
                'subtype': 'Raw Material',
                'grade': 'USP',
                'hazard_class': 'None',
                'chemical_family': '',
                'contamination_risk': 'High',
                'critical_to_product': True,
                'qa_required': True,
                'traceability_level': 'Full',
                'sds_mandatory': False,
                'coa_mandatory': True,
                'spec_required': True
            },
            {
                'item_record_id': 'PACK-BOT-50ML-001',
                'item_name': '50ml Bottle',
                'unit_of_measure': 'pcs',
                'category': 'Packaging',
                'subtype': 'Bottle',
                'grade': '',
                'hazard_class': 'None',
                'chemical_family': '',
                'contamination_risk': 'Low',
                'critical_to_product': False,
                'qa_required': False,
                'traceability_level': 'None',
                'sds_mandatory': False,
                'coa_mandatory': False,
                'spec_required': False
            }
        ]
        
        for item_data in items:
            item, created = ItemRecord.objects.get_or_create(
                item_record_id=item_data['item_record_id'],
                defaults=item_data
            )
            if created:
                self.stdout.write(f'Created item: {item.item_name}')

    def create_products(self):
        products = [
            {
                'product_id': 'PRD-BIO-001',
                'product_name': 'Astaxanthin 5% Softgel',
                'product_source': 'Internal',
                'category': 'Biological',
                'subtype': 'Finished Product',
                'spec_version_linked': 'SPEC-2025-V1',
                'product_label_name': 'Astaxanthin 5% - 60 capsules',
                'default_unit_of_sale': '1 Bottle',
                'shelf_life_months': 24,
                'qa_required': True,
                'traceability_required': 'Batch-level'
            }
        ]
        
        for product_data in products:
            product, created = Product.objects.get_or_create(
                product_id=product_data['product_id'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.product_name}')

    def create_supplier_products(self):
        supplier_products = [
            {
                'item_code_id': 'CHE-SOL-ETH-001',
                'supplier_name_id': 'SUP-CHEMCO',
                'manufacturer_name': 'Chemical Co. Ltd.',
                'grade': 'USP',
                'product_code': 'ETH-99.9-1L',
                'packaging_description': '1L bottle',
                'batch_code_format_known': True,
                'batch_code_quality': 'High',
                'traceability_level': 'Batch-level',
                'coa_mandatory': True,
                'sds_mandatory': True,
                'is_default': True,
                'approved': True,
                'last_reviewed_on': timezone.now().date(),
                'review_frequency': '6 months'
            },
            {
                'item_code_id': 'BIO-RM-ALG-001',
                'supplier_name_id': 'SUP-ALGAMO',
                'manufacturer_name': 'Algamo S.R.O.',
                'grade': 'USP',
                'product_code': 'ALG-EXT-1KG',
                'packaging_description': '1kg container',
                'batch_code_format_known': True,
                'batch_code_quality': 'High',
                'traceability_level': 'Full',
                'coa_mandatory': True,
                'sds_mandatory': False,
                'is_default': True,
                'approved': True,
                'last_reviewed_on': timezone.now().date(),
                'review_frequency': '6 months'
            }
        ]
        
        for sp_data in supplier_products:
            supplier_product, created = SupplierProduct.objects.get_or_create(
                item_code_id=sp_data['item_code_id'],
                supplier_name_id=sp_data['supplier_name_id'],
                defaults=sp_data
            )
            if created:
                self.stdout.write(f'Created supplier product: {supplier_product.item_code.item_name} - {supplier_product.supplier_name.supplier_name}')

    def create_customers(self):
        customers = [
            {
                'customer_code': 'CUS-AMALA',
                'customer_name': 'Amala Cancer Research Center',
                'address_line1': 'Amala Nagar, Thrissur',
                'address_line2': 'Kerala 680555',
                'city': 'Thrissur',
                'state': 'Kerala',
                'postal_code': '680555',
                'country': 'IN',
                'contact_person': 'Dr. Janardhanan',
                'phone': '9876543210',
                'email': 'janardhanan@amala.in',
                'customer_type': 'Research',
                'gstin': '32ABCDE1234F1Z5',
                'preferred_courier': 'Professional Courier',
                'qa_required_before_ship': True,
                'approved': True,
                'approved_on': timezone.now().date(),
                'remarks': 'Research institution - special handling required'
            }
        ]
        
        for customer_data in customers:
            customer, created = Customer.objects.get_or_create(
                customer_code=customer_data['customer_code'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(f'Created customer: {customer.customer_name}')

    def create_batches(self):
        batches = [
            {
                'batch_id': 'BATCH-CHE-SOL-ETH-001-20240720-001',
                'item_record_id': ItemRecord.objects.get(item_record_id='CHE-SOL-ETH-001'),
                'subtype': 'Solvent',
                'quantity_received': 10.0,
                'received_date': timezone.now().date() - timedelta(days=30),
                'expiry_date': timezone.now().date() + timedelta(days=365),
                'qa_status': 'Approved',
                'storage_location': 'LOC-CHEM-A1'
            },
            {
                'batch_id': 'BATCH-BIO-RM-ALG-001-20240720-001',
                'item_record_id': ItemRecord.objects.get(item_record_id='BIO-RM-ALG-001'),
                'subtype': 'Raw Material',
                'quantity_received': 5.0,
                'received_date': timezone.now().date() - timedelta(days=15),
                'expiry_date': timezone.now().date() + timedelta(days=730),
                'qa_status': 'Approved',
                'storage_location': 'LOC-BIO-A1'
            }
        ]
        
        for batch_data in batches:
            batch, created = Batch.objects.get_or_create(
                batch_id=batch_data['batch_id'],
                defaults=batch_data
            )
            if created:
                self.stdout.write(f'Created batch: {batch.batch_id}')

    def create_qa_reviews(self):
        qa_reviews = [
            {
                'qa_review_id': 'QA-20240720-001',
                'batch_number_id': Batch.objects.get(batch_id='BATCH-CHE-SOL-ETH-001-20240720-001'),
                'item_code_id': ItemRecord.objects.get(item_record_id='CHE-SOL-ETH-001'),
                'supplier_code_id': Supplier.objects.get(supplier_id='SUP-CHEMCO'),
                'coa_match': True,
                'sds_match': True,
                'spec_match': True,
                'coa_attached': True,
                'sds_attached': True,
                'label_attached': True,
                'spec_attached': True,
                'document_match': 'Yes',
                'review_outcome': 'Approved',
                'qa_reviewer': 'admin',
                'review_date': timezone.now().date(),
                'comments': 'All documents verified and approved'
            },
            {
                'qa_review_id': 'QA-20240720-002',
                'batch_number_id': Batch.objects.get(batch_id='BATCH-BIO-RM-ALG-001-20240720-001'),
                'item_code_id': ItemRecord.objects.get(item_record_id='BIO-RM-ALG-001'),
                'supplier_code_id': Supplier.objects.get(supplier_id='SUP-ALGAMO'),
                'coa_match': True,
                'sds_match': False,
                'spec_match': True,
                'coa_attached': True,
                'sds_attached': False,
                'label_attached': True,
                'spec_attached': True,
                'document_match': 'Partial',
                'review_outcome': 'Approved',
                'qa_reviewer': 'admin',
                'review_date': timezone.now().date(),
                'comments': 'Approved - SDS not required for this material'
            }
        ]
        
        for qa_data in qa_reviews:
            qa_review, created = QAReview.objects.get_or_create(
                qa_review_id=qa_data['qa_review_id'],
                defaults=qa_data
            )
            if created:
                self.stdout.write(f'Created QA review: {qa_review.qa_review_id}')

    def create_transactions(self):
        transactions = [
            {
                'transaction_id': 'TXN-20240720-001',
                'transaction_datetime': timezone.now() - timedelta(days=30),
                'transaction_user': 'admin',
                'transaction_type': 'RCV-PUR',
                'item_code_id': ItemRecord.objects.get(item_record_id='CHE-SOL-ETH-001'),
                'product_code': 'ETH-99.9-1L',
                'product_name': 'Ethanol 99.9%',
                'batch_id': Batch.objects.get(batch_id='BATCH-CHE-SOL-ETH-001-20240720-001'),
                'quantity': 10.0,
                'unit': 'L',
                'supplier_code_id': Supplier.objects.get(supplier_id='SUP-CHEMCO'),
                'supplier_name': 'Chemical Co. Ltd.',
                'invoice_no': 'INV-2024-001',
                'invoice_date': timezone.now().date() - timedelta(days=30),
                'coa_provided': True,
                'sds_provided': True,
                'label_applied': True,
                'storage_zone_id': StorageZone.objects.get(zone_id='ZONE-CHEM-001'),
                'storage_location_id': StorageLocation.objects.get(location_id='LOC-CHEM-A1'),
                'qa_status': 'Approved',
                'qa_review_id': QAReview.objects.get(qa_review_id='QA-20240720-001'),
                'coa_match': True,
                'sds_match': True,
                'spec_match': True,
                'mfg_date': timezone.now().date() - timedelta(days=35),
                'expiry_date': timezone.now().date() + timedelta(days=365),
                'comments': 'Initial receipt of ethanol batch'
            },
            {
                'transaction_id': 'TXN-20240720-002',
                'transaction_datetime': timezone.now() - timedelta(days=15),
                'transaction_user': 'admin',
                'transaction_type': 'RCV-PUR',
                'item_code_id': ItemRecord.objects.get(item_record_id='BIO-RM-ALG-001'),
                'product_code': 'ALG-EXT-1KG',
                'product_name': 'Algae Extract',
                'batch_id': Batch.objects.get(batch_id='BATCH-BIO-RM-ALG-001-20240720-001'),
                'quantity': 5.0,
                'unit': 'kg',
                'supplier_code_id': Supplier.objects.get(supplier_id='SUP-ALGAMO'),
                'supplier_name': 'Algamo S.R.O.',
                'invoice_no': 'INV-2024-002',
                'invoice_date': timezone.now().date() - timedelta(days=15),
                'coa_provided': True,
                'sds_provided': False,
                'label_applied': True,
                'storage_zone_id': StorageZone.objects.get(zone_id='ZONE-BIO-001'),
                'storage_location_id': StorageLocation.objects.get(location_id='LOC-BIO-A1'),
                'qa_status': 'Approved',
                'qa_review_id': QAReview.objects.get(qa_review_id='QA-20240720-002'),
                'coa_match': True,
                'sds_match': False,
                'spec_match': True,
                'mfg_date': timezone.now().date() - timedelta(days=20),
                'expiry_date': timezone.now().date() + timedelta(days=730),
                'comments': 'Receipt of algae extract for production'
            },
            {
                'transaction_id': 'TXN-20240720-003',
                'transaction_datetime': timezone.now() - timedelta(days=5),
                'transaction_user': 'admin',
                'transaction_type': 'ISS-MFG',
                'item_code_id': ItemRecord.objects.get(item_record_id='CHE-SOL-ETH-001'),
                'product_code': 'ETH-99.9-1L',
                'product_name': 'Ethanol 99.9%',
                'batch_id': Batch.objects.get(batch_id='BATCH-CHE-SOL-ETH-001-20240720-001'),
                'quantity': 2.0,
                'unit': 'L',
                'used_in': 'BATCH-PRD-001',
                'used_by': 'Production Team',
                'used_date': timezone.now().date() - timedelta(days=5),
                'storage_zone_id': StorageZone.objects.get(zone_id='ZONE-CHEM-001'),
                'storage_location_id': StorageLocation.objects.get(location_id='LOC-CHEM-A1'),
                'qa_status': 'Approved',
                'comments': 'Issued for manufacturing batch PRD-001'
            }
        ]
        
        for txn_data in transactions:
            transaction, created = InventoryTransaction.objects.get_or_create(
                transaction_id=txn_data['transaction_id'],
                defaults=txn_data
            )
            if created:
                self.stdout.write(f'Created transaction: {transaction.transaction_id}') 