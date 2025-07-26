import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from inventory.models import (
    Supplier, ItemRecord, Batch, InventoryTransaction, StorageZone, StorageLocation,
    CategoryChoices, GradeChoices, UOMChoices, TransactionTypeChoices, QAStatusChoices,
    Customer
)

class Command(BaseCommand):
    help = 'Import real data from CSV files into the ERP system (Version 2)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default='Public/data',
            help='Directory containing the CSV data files'
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        
        if not os.path.exists(data_dir):
            self.stdout.write(
                self.style.ERROR(f'Data directory {data_dir} does not exist')
            )
            return

        self.stdout.write(
            self.style.SUCCESS('Starting comprehensive data import process...')
        )

        try:
            with transaction.atomic():
                # Step 1: Create storage infrastructure
                self.create_storage_infrastructure()
                
                # Step 2: Import suppliers
                self.import_suppliers()
                
                # Step 3: Import customers
                self.import_customers()
                
                # Step 4: Import items and batches from stock files
                self.import_stock_data(data_dir)
                
                # Step 5: Import PBR equipment (special format)
                self.import_pbr_equipment(data_dir)
                
                # Step 6: Import transaction data
                self.import_transaction_data(data_dir)
                
                self.stdout.write(
                    self.style.SUCCESS('Comprehensive data import completed successfully!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during data import: {str(e)}')
            )
            raise

    def create_storage_infrastructure(self):
        """Create basic storage zones and locations"""
        self.stdout.write('Creating storage infrastructure...')
        
        # Create storage zones
        zones_data = [
            {
                'zone_id': 'ZONE-CHEM',
                'zone_name': 'Chemical Storage Zone',
                'temperature_range': '20-25°C',
                'humidity_controlled': True,
                'hazard_compatibility': 'Flammable, Corrosive, Oxidizer, Reactive',
                'default_for_category': 'Chemical'
            },
            {
                'zone_id': 'ZONE-BIO',
                'zone_name': 'Biological Storage Zone',
                'temperature_range': '2-8°C',
                'humidity_controlled': True,
                'hazard_compatibility': 'Biohazard',
                'default_for_category': 'Biological'
            },
            {
                'zone_id': 'ZONE-EQUIP',
                'zone_name': 'Equipment Storage Zone',
                'temperature_range': '20-25°C',
                'humidity_controlled': False,
                'hazard_compatibility': 'None',
                'default_for_category': 'Equipment'
            },
            {
                'zone_id': 'ZONE-CONSUM',
                'zone_name': 'Consumables Storage Zone',
                'temperature_range': '20-25°C',
                'humidity_controlled': False,
                'hazard_compatibility': 'None',
                'default_for_category': 'Consumables'
            }
        ]
        
        for zone_data in zones_data:
            zone, created = StorageZone.objects.get_or_create(
                zone_id=zone_data['zone_id'],
                defaults=zone_data
            )
            if created:
                self.stdout.write(f'Created storage zone: {zone.zone_name}')
        
        # Create storage locations
        locations_data = [
            {'location_id': 'LOC-CHEM-01', 'zone_id': 'ZONE-CHEM', 'rack_shelf': 'Rack 1, Shelf A', 'max_capacity': '1000 items'},
            {'location_id': 'LOC-CHEM-02', 'zone_id': 'ZONE-CHEM', 'rack_shelf': 'Rack 1, Shelf B', 'max_capacity': '1000 items'},
            {'location_id': 'LOC-BIO-01', 'zone_id': 'ZONE-BIO', 'rack_shelf': 'Refrigerator 1', 'max_capacity': '500 items'},
            {'location_id': 'LOC-EQUIP-01', 'zone_id': 'ZONE-EQUIP', 'rack_shelf': 'Rack 2, Shelf A', 'max_capacity': '200 items'},
            {'location_id': 'LOC-CONSUM-01', 'zone_id': 'ZONE-CONSUM', 'rack_shelf': 'Rack 3, Shelf A', 'max_capacity': '2000 items'},
        ]
        
        for loc_data in locations_data:
            zone = StorageZone.objects.get(zone_id=loc_data['zone_id'])
            location, created = StorageLocation.objects.get_or_create(
                location_id=loc_data['location_id'],
                defaults={
                    'zone_id': zone,
                    'rack_shelf': loc_data['rack_shelf'],
                    'max_capacity': loc_data['max_capacity'],
                    'active': True
                }
            )
            if created:
                self.stdout.write(f'Created storage location: {location.location_id}')

    def import_suppliers(self):
        """Import suppliers from the data"""
        self.stdout.write('Importing suppliers...')
        
        suppliers_data = [
            {
                'supplier_id': 'SUP-CALGON',
                'supplier_name': 'Calgon Scientific',
                'address': 'Vinayaka Building, Ponekkara, AIMS P.O. Edapally, Kochi, Kerala, 682 041\nPh-+914842802330/2352\nEmail: info@calgonscientific.com\nhttp://www.calgonscientific.com',
                'country_of_origin': 'IN',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'supplier_id': 'SUP-ILE',
                'supplier_name': 'ILE',
                'address': 'ILE Laboratory Equipment\nThiruvananthapuram, Kerala',
                'country_of_origin': 'IN',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'supplier_id': 'SUP-SABARI',
                'supplier_name': 'Sabari Scientific Supplies',
                'address': 'Sreepankajam Building, Police Quarters Road, Nemom, Thiruvananthapuram - 695020\nPh-9447863355, 9746438384\nEmail: sabarilabsupplies@gmail.com\nhttp://www.sabariscientificsupplies.com',
                'country_of_origin': 'IN',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'supplier_id': 'SUP-HIMEDIA',
                'supplier_name': 'Himedia',
                'address': 'Himedia Laboratories Pvt. Ltd.\nMumbai, Maharashtra',
                'country_of_origin': 'IN',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'supplier_id': 'SUP-SOFTGEL',
                'supplier_name': 'Softgel Healthcare Pvt. Ltd.',
                'address': 'No.20/1,Vandalur-Kelambakkam road,Pudupakkam village,Chengalpettu district,Tamil Nadu 603103\nContact: 9441936241',
                'country_of_origin': 'IN',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'supplier_id': 'SUP-ALGAMO',
                'supplier_name': 'Algamo S.R.O',
                'address': 'Czech Republic',
                'country_of_origin': 'CZ',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'supplier_id': 'SUP-YASHAM',
                'supplier_name': 'Yasham Speciality Ingredients Pvt. Ltd.',
                'address': '401A 4th floor, Satyadev, Plot No. 6A, Veera Indl Estate, Off Veera Desai road, Andheri (West), mumbai-400053, Maharashtra',
                'country_of_origin': 'IN',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'supplier_id': 'SUP-LGEM',
                'supplier_name': 'Lgem',
                'address': 'Lgem Equipment Supplier',
                'country_of_origin': 'IN',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'supplier_id': 'SUP-DURAN',
                'supplier_name': 'Duran',
                'address': 'Duran Glass Equipment',
                'country_of_origin': 'DE',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            }
        ]
        
        for supplier_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                supplier_id=supplier_data['supplier_id'],
                defaults=supplier_data
            )
            if created:
                self.stdout.write(f'Created supplier: {supplier.supplier_name}')

    def import_customers(self):
        """Import customers from transaction data"""
        self.stdout.write('Importing customers...')
        
        customers_data = [
            {
                'customer_code': 'CUS-AMALA',
                'customer_name': 'Amala Cancer Research Center',
                'address_line1': 'Amala Nagar, Thrissur',
                'address_line2': 'Kerala 680555',
                'city': 'Thrissur',
                'state': 'Kerala',
                'postal_code': '680555',
                'country': 'IN',
                'contact_person': 'Dr KK Janardhanan',
                'phone': '9876543210',
                'email': 'janardhanan@amala.in',
                'customer_type': 'Clinical',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'customer_code': 'CUS-SYNT',
                'customer_name': 'Synthite Industries Private Limited',
                'address_line1': 'Synthite Valley, Kadayiruppu, Kolenchery',
                'address_line2': 'Eranakulam 682311',
                'city': 'Eranakulam',
                'state': 'Kerala',
                'postal_code': '682311',
                'country': 'IN',
                'contact_person': 'Yadhu Krishna',
                'phone': '977841232',
                'email': 'info@synthite.com',
                'customer_type': 'Commercial',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            },
            {
                'customer_code': 'CUS-ALGAMO',
                'customer_name': 'ALGAMO sro',
                'address_line1': 'Mostek 227, 544 75 MOSTEK',
                'address_line2': 'Czech Republic',
                'city': 'Mostek',
                'state': 'Czech Republic',
                'postal_code': '54475',
                'country': 'CZ',
                'contact_person': 'Martin',
                'phone': '+420602127411',
                'email': 'info@algamo.cz',
                'customer_type': 'Commercial',
                'approved': True,
                'approved_on': datetime(2022, 1, 1).date()
            }
        ]
        
        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                customer_code=customer_data['customer_code'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(f'Created customer: {customer.customer_name}')

    def import_stock_data(self, data_dir):
        """Import stock data from all category files"""
        self.stdout.write('Importing stock data...')
        
        # Define file mappings
        file_mappings = {
            'LP3aEquipment.csv': 'Equipment',
            'LP3bChemicals.csv': 'Chemical',
            'LP3cPBR1.csv': 'Biological',
            'LP3dGlasswares.csv': 'Plasticwares',
            'LP3ePlasticwares.csv': 'Plasticwares',
            'LP3fDisposables.csv': 'Consumables',
            'LP3gStationery.csv': 'Stationery',
            'LP3hBiological_samples.csv': 'Biological',
            'LP3iOthers.csv': 'Consumables',
            'LP3jElectricals.csv': 'Electrical',
            'LP3kmiscellaneous.csv': 'Consumables'
        }
        
        for filename, category in file_mappings.items():
            filepath = os.path.join(data_dir, f'LPS2.Stock details -Pluviago (2) (1)_{filename}')
            if os.path.exists(filepath):
                self.import_category_data(filepath, category)
            else:
                self.stdout.write(f'Warning: File {filepath} not found')

    def import_category_data(self, filepath, category):
        """Import data from a specific category file"""
        self.stdout.write(f'Importing {category} data from {os.path.basename(filepath)}...')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        self.process_stock_row(row, category)
                    except Exception as e:
                        self.stdout.write(f'Error processing row: {row.get("Name", "Unknown")} - {str(e)}')
                        continue
                        
        except Exception as e:
            self.stdout.write(f'Error reading file {filepath}: {str(e)}')

    def process_stock_row(self, row, category):
        """Process a single stock row"""
        # Skip empty rows
        if not row.get('Name') or row['Name'].strip() == '':
            return
            
        # Extract data from row
        item_name = row['Name'].strip()
        grade = row.get('Grade', '').strip()
        product_code = row.get('Product code', '').strip()
        lot_no = row.get('Lot No.', '').strip()
        quantity = row.get('Qty', '').strip()
        unit = row.get('Unit', '').strip()
        brand = row.get('Brand', '').strip()
        supplier_name = row.get('Supplier', '').strip()
        received_date = row.get('Received on', '').strip()
        mfg_date = row.get('Mfg. Date/QC* release date', '').strip()
        expiry_date = row.get('Exp./Retest* Date', '').strip()
        opened_date = row.get('Opened on', '').strip()
        finished_date = row.get('Finished on', '').strip()
        coa = row.get('COA', '').strip()
        spec = row.get('Spec', '').strip()
        sds = row.get('SDS', '').strip()
        comments = row.get('Comments', '').strip()
        invoice_no = row.get('Invoice No.', '').strip()
        invoice_date = row.get('Invoice date', '').strip()
        
        # Create or get supplier
        supplier = self.get_or_create_supplier(supplier_name)
        
        # Create item record
        item_record_id = self.generate_item_id(category, item_name)
        item_record = self.get_or_create_item_record(
            item_record_id, item_name, category, grade, product_code
        )
        
        # Create batch if lot number exists
        if lot_no:
            batch = self.get_or_create_batch(
                lot_no, item_record, supplier, quantity, unit,
                received_date, mfg_date, expiry_date, opened_date, finished_date
            )
            
            # Create inventory transaction for receipt
            if received_date:
                self.create_receipt_transaction(
                    item_record, supplier, batch, quantity, unit,
                    received_date, invoice_no, invoice_date, coa, spec, sds
                )

    def import_pbr_equipment(self, data_dir):
        """Import PBR equipment data (special format)"""
        self.stdout.write('Importing PBR equipment data...')
        
        # Import PBR.csv
        pbr_file = os.path.join(data_dir, 'LPS2.Stock details -Pluviago (2) (1)_PBR.csv')
        if os.path.exists(pbr_file):
            self.import_pbr_file(pbr_file)
        
        # Import PBR1.csv (already handled in stock data, but with special processing)
        pbr1_file = os.path.join(data_dir, 'LPS2.Stock details -Pluviago (2) (1)_LP3cPBR1.csv')
        if os.path.exists(pbr1_file):
            self.import_pbr1_file(pbr1_file)

    def import_pbr_file(self, filepath):
        """Import PBR equipment file"""
        self.stdout.write('Importing PBR equipment...')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        self.process_pbr_row(row)
                    except Exception as e:
                        self.stdout.write(f'Error processing PBR row: {str(e)}')
                        continue
                        
        except Exception as e:
            self.stdout.write(f'Error reading PBR file: {str(e)}')

    def process_pbr_row(self, row):
        """Process PBR equipment row"""
        item_name = row.get('Item', '').strip()
        if not item_name:
            return
            
        quantity = row.get('Qty', '').strip()
        unit = row.get('Unit', '').strip()
        brand = row.get('Brand', '').strip()
        supplier_name = row.get('Supplier', '').strip()
        purchased_date = row.get('Purchased on', '').strip()
        finished_date = row.get('Finished on ', '').strip()
        comments = row.get('Comments', '').strip()
        
        # Create or get supplier
        supplier = self.get_or_create_supplier(supplier_name)
        
        # Create item record
        item_record_id = self.generate_item_id('Equipment', item_name)
        item_record = self.get_or_create_item_record(
            item_record_id, item_name, 'Equipment', '', ''
        )
        
        # Create batch
        batch_id = f"PBR-{item_name[:10].upper().replace(' ', '')}-{purchased_date[:10]}" if purchased_date else f"PBR-{item_name[:10].upper().replace(' ', '')}"
        
        batch = self.get_or_create_batch(
            batch_id, item_record, supplier, quantity, unit,
            purchased_date, '', '', '', finished_date
        )
        
        # Create transaction
        if purchased_date:
            self.create_receipt_transaction(
                item_record, supplier, batch, quantity, unit,
                purchased_date, '', '', False, False, False
            )

    def import_pbr1_file(self, filepath):
        """Import PBR1 components file"""
        self.stdout.write('Importing PBR1 components...')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        self.process_pbr1_row(row)
                    except Exception as e:
                        self.stdout.write(f'Error processing PBR1 row: {str(e)}')
                        continue
                        
        except Exception as e:
            self.stdout.write(f'Error reading PBR1 file: {str(e)}')

    def process_pbr1_row(self, row):
        """Process PBR1 component row"""
        item_name = row.get('Item', '').strip()
        if not item_name:
            return
            
        quantity = row.get('Qty', '').strip()
        unit = row.get('Unit', '').strip()
        brand = row.get('Brand', '').strip()
        supplier_name = row.get('Supplier', '').strip()
        purchased_date = row.get('Purchased on', '').strip()
        finished_date = row.get('Finished on ', '').strip()
        comments = row.get('Comments', '').strip()
        invoice_no = row.get('Invoice no.', '').strip()
        invoice_date = row.get('Invoice date', '').strip()
        
        # Create or get supplier
        supplier = self.get_or_create_supplier(supplier_name)
        
        # Create item record
        item_record_id = self.generate_item_id('Equipment', item_name)
        item_record = self.get_or_create_item_record(
            item_record_id, item_name, 'Equipment', '', ''
        )
        
        # Create batch
        batch_id = f"PBR1-{item_name[:10].upper().replace(' ', '')}-{purchased_date[:10]}" if purchased_date else f"PBR1-{item_name[:10].upper().replace(' ', '')}"
        
        batch = self.get_or_create_batch(
            batch_id, item_record, supplier, quantity, unit,
            purchased_date, '', '', '', finished_date
        )
        
        # Create transaction
        if purchased_date:
            self.create_receipt_transaction(
                item_record, supplier, batch, quantity, unit,
                purchased_date, invoice_no, invoice_date, False, False, False
            )

    def get_or_create_supplier(self, supplier_name):
        """Get or create supplier by name"""
        if not supplier_name or supplier_name.strip() == '':
            # Create a default supplier
            supplier, created = Supplier.objects.get_or_create(
                supplier_id='SUP-DEFAULT',
                defaults={
                    'supplier_name': 'Default Supplier',
                    'address': 'Default Address',
                    'country_of_origin': 'IN',
                    'approved': True
                }
            )
            return supplier
            
        # Try to find existing supplier
        supplier = Supplier.objects.filter(
            supplier_name__icontains=supplier_name.split()[0]
        ).first()
        
        if not supplier:
            # Create new supplier
            supplier_id = f'SUP-{supplier_name[:10].upper().replace(" ", "")}'
            supplier, created = Supplier.objects.get_or_create(
                supplier_id=supplier_id,
                defaults={
                    'supplier_name': supplier_name,
                    'address': f'Address for {supplier_name}',
                    'country_of_origin': 'IN',
                    'approved': True
                }
            )
            if created:
                self.stdout.write(f'Created new supplier: {supplier_name}')
        
        return supplier

    def generate_item_id(self, category, item_name):
        """Generate item record ID based on category and name"""
        # Extract first word from item name for subtype
        subtype = item_name.split()[0][:10].upper()
        
        # Generate unique code
        import hashlib
        code = hashlib.md5(item_name.encode()).hexdigest()[:6].upper()
        
        return f"{category[:3].upper()}-{subtype}-{code}"

    def get_or_create_item_record(self, item_record_id, item_name, category, grade, product_code):
        """Get or create item record"""
        item_record, created = ItemRecord.objects.get_or_create(
            item_record_id=item_record_id,
            defaults={
                'item_name': item_name,
                'category': category,
                'subtype': item_name.split()[0],
                'grade': grade if grade else '',
                'unit_of_measure': 'g' if 'gm' in item_name.lower() else 'ml' if 'ml' in item_name.lower() else 'pcs',
                'hazard_class': 'None',
                'contamination_risk': 'Low',
                'critical_to_product': False
            }
        )
        
        if created:
            self.stdout.write(f'Created item record: {item_name}')
        
        return item_record

    def get_or_create_batch(self, lot_no, item_record, supplier, quantity, unit, 
                           received_date, mfg_date, expiry_date, opened_date, finished_date):
        """Get or create batch"""
        # Parse dates
        received_dt = self.parse_date(received_date)
        mfg_dt = self.parse_date(mfg_date)
        expiry_dt = self.parse_date(expiry_date)
        opened_dt = self.parse_date(opened_date)
        finished_dt = self.parse_date(finished_date)
        
        # Parse quantity
        try:
            qty = float(quantity) if quantity else 0
        except:
            qty = 0
            
        # Determine QA status
        qa_status = 'Approved'  # Default to approved for existing stock
        
        batch, created = Batch.objects.get_or_create(
            batch_id=lot_no,
            defaults={
                'item_record_id': item_record,
                'supplier_code': supplier,
                'batch_source': 'External',
                'batch_type': 'Production',
                'quantity_received': qty,
                'received_date': received_dt or timezone.now().date(),
                'expiry_date': expiry_dt,
                'qa_status': qa_status,
                'subtype': item_record.subtype
            }
        )
        
        if created:
            self.stdout.write(f'Created batch: {lot_no} for {item_record.item_name}')
        
        return batch

    def create_receipt_transaction(self, item_record, supplier, batch, quantity, unit,
                                 received_date, invoice_no, invoice_date, coa, spec, sds):
        """Create receipt transaction"""
        # Parse dates
        received_dt = self.parse_date(received_date)
        invoice_dt = self.parse_date(invoice_date)
        
        # Parse quantity
        try:
            qty = float(quantity) if quantity else 0
        except:
            qty = 0
            
        # Generate transaction ID
        transaction_id = f"TXN-{received_dt.strftime('%Y%m%d')}-{batch.batch_id[:6]}" if received_dt else f"TXN-{timezone.now().strftime('%Y%m%d')}-{batch.batch_id[:6]}"
        
        # Check if transaction already exists
        if InventoryTransaction.objects.filter(transaction_id=transaction_id).exists():
            return
            
        # Create transaction
        transaction = InventoryTransaction.objects.create(
            transaction_id=transaction_id,
            transaction_datetime=timezone.now(),
            transaction_user='system_import',
            transaction_type='RCV-PUR',
            item_code=item_record,
            product_code=batch.batch_id,
            product_name=item_record.item_name,
            batch_id=batch,
            quantity=qty,
            unit=unit or item_record.unit_of_measure,
            supplier_code=supplier,
            supplier_name=supplier.supplier_name,
            mfg_date=batch.received_date,
            expiry_date=batch.expiry_date,
            coa_provided=coa == 'ü',
            sds_provided=sds == 'ü',
            spec_match=spec == 'ü',
            qa_status=batch.qa_status,
            invoice_no=invoice_no,
            invoice_date=invoice_dt,
            comments=f'Imported from stock data - {batch.batch_id}'
        )
        
        self.stdout.write(f'Created transaction: {transaction_id}')

    def parse_date(self, date_str):
        """Parse date string to datetime object"""
        if not date_str or date_str.strip() == '':
            return None
            
        date_str = date_str.strip()
        
        # Handle various date formats
        date_formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%d-%m-%y',
            '%d/%m/%y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
                
        return None

    def import_transaction_data(self, data_dir):
        """Import incoming and outgoing transaction data"""
        self.stdout.write('Importing transaction data...')
        
        # Import incoming transactions
        incoming_file = os.path.join(data_dir, 'AS.1.List Incoming _Out Going... (1)_Incoming_details.csv')
        if os.path.exists(incoming_file):
            self.import_incoming_transactions(incoming_file)
        
        # Import outgoing transactions
        outgoing_file = os.path.join(data_dir, 'AS.1.List Incoming _Out Going... (1)_Outgoing_details.csv')
        if os.path.exists(outgoing_file):
            self.import_outgoing_transactions(outgoing_file)

    def import_incoming_transactions(self, filepath):
        """Import incoming transaction data"""
        self.stdout.write('Importing incoming transactions...')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        self.process_incoming_row(row)
                    except Exception as e:
                        self.stdout.write(f'Error processing incoming row: {str(e)}')
                        continue
                        
        except Exception as e:
            self.stdout.write(f'Error reading incoming file: {str(e)}')

    def process_incoming_row(self, row):
        """Process incoming transaction row"""
        # Extract data
        product_name = row.get('Product Name', '').strip()
        quantity = row.get('Qty. Received', '').strip()
        batch_no = row.get('Batch  No', '').strip()
        product_code = row.get('Product code', '').strip()
        mfg_date = row.get('Mfg.Date', '').strip()
        expiry_date = row.get('Expiry Date', '').strip()
        manufacturer = row.get('Manufacturer name', '').strip()
        supplier_name = row.get('     Sample Received From', '').strip()
        received_date = row.get('Received Date', '').strip()
        invoice_no = row.get('Invoice no:', '').strip()
        invoice_date = row.get('Invoice date ', '').strip()
        comment = row.get('Comment', '').strip()
        
        if not product_name:
            return
            
        # Create or get supplier
        supplier = self.get_or_create_supplier(supplier_name)
        
        # Create item record
        item_record_id = self.generate_item_id('Biological', product_name)
        item_record = self.get_or_create_item_record(
            item_record_id, product_name, 'Biological', '', product_code
        )
        
        # Create batch if batch number exists
        if batch_no:
            batch = self.get_or_create_batch(
                batch_no, item_record, supplier, quantity, 'Kg',
                received_date, mfg_date, expiry_date, '', ''
            )
            
            # Create transaction
            if received_date:
                self.create_receipt_transaction(
                    item_record, supplier, batch, quantity, 'Kg',
                    received_date, invoice_no, invoice_date, True, True, True
                )

    def import_outgoing_transactions(self, filepath):
        """Import outgoing transaction data"""
        self.stdout.write('Importing outgoing transactions...')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        self.process_outgoing_row(row)
                    except Exception as e:
                        self.stdout.write(f'Error processing outgoing row: {str(e)}')
                        continue
                        
        except Exception as e:
            self.stdout.write(f'Error reading outgoing file: {str(e)}')

    def process_outgoing_row(self, row):
        """Process outgoing transaction row"""
        # Extract data
        product_name = row.get('Product Name', '').strip()
        quantity = row.get('Qty. Sent', '').strip()
        batch_no = row.get('Batch  No', '').strip()
        mfg_date = row.get('Mfg.Date', '').strip()
        expiry_date = row.get('Expiry .Date', '').strip()
        manufacturer = row.get('Manufacturer name', '').strip()
        customer_name = row.get('     Sample Sent to', '').strip()
        sent_date = row.get('Sent Date', '').strip()
        courier_details = row.get('Courier details', '').strip()
        
        if not product_name or not customer_name:
            return
            
        # Get or create customer
        customer = self.get_or_create_customer(customer_name)
        
        # Get item record
        item_record = ItemRecord.objects.filter(item_name__icontains=product_name).first()
        if not item_record:
            # Create item record if not exists
            item_record_id = self.generate_item_id('Biological', product_name)
            item_record = self.get_or_create_item_record(
                item_record_id, product_name, 'Biological', '', ''
            )
        
        # Get batch if batch number exists
        batch = None
        if batch_no:
            batch = Batch.objects.filter(batch_number=batch_no).first()
        
        # Create outgoing transaction
        if sent_date:
            self.create_outgoing_transaction(
                item_record, customer, batch, quantity, sent_date, courier_details
            )

    def get_or_create_customer(self, customer_name):
        """Get or create customer by name"""
        # Try to find existing customer
        customer = Customer.objects.filter(
            customer_name__icontains=customer_name.split()[0]
        ).first()
        
        if not customer:
            # Create new customer
            customer_code = f'CUS-{customer_name[:10].upper().replace(" ", "")}'
            customer, created = Customer.objects.get_or_create(
                customer_code=customer_code,
                defaults={
                    'customer_name': customer_name,
                    'address_line1': f'Address for {customer_name}',
                    'city': 'Unknown',
                    'state': 'Unknown',
                    'postal_code': '000000',
                    'country': 'IN',
                    'contact_person': 'Contact Person',
                    'phone': '0000000000',
                    'customer_type': 'Research',
                    'approved': True
                }
            )
            if created:
                self.stdout.write(f'Created new customer: {customer_name}')
        
        return customer

    def create_outgoing_transaction(self, item_record, customer, batch, quantity, sent_date, courier_details):
        """Create outgoing transaction"""
        # Parse date
        sent_dt = self.parse_date(sent_date)
        
        # Parse quantity
        try:
            qty = -float(quantity) if quantity else 0  # Negative for outgoing
        except:
            qty = 0
            
        # Generate transaction ID
        transaction_id = f"TXN-{sent_dt.strftime('%Y%m%d')}-OUT-{item_record.item_record_id[:6]}" if sent_dt else f"TXN-{timezone.now().strftime('%Y%m%d')}-OUT-{item_record.item_record_id[:6]}"
        
        # Check if transaction already exists
        if InventoryTransaction.objects.filter(transaction_id=transaction_id).exists():
            return
            
        # Create transaction
        transaction = InventoryTransaction.objects.create(
            transaction_id=transaction_id,
            transaction_datetime=timezone.now(),
            transaction_user='system_import',
            transaction_type='SHIP-CUS',
            item_code=item_record,
            product_code=batch.batch_number if batch else '',
            product_name=item_record.item_name,
            batch_id=batch,
            quantity=qty,
            unit=item_record.unit_of_measure,
            recipient_code=customer,
            recipient_company=customer.customer_name,
            recipient_contact=customer.contact_person,
            dispatch_method='Courier',
            courier_name=courier_details,
            comments=f'Outgoing shipment - {customer.customer_name}'
        )
        
        self.stdout.write(f'Created outgoing transaction: {transaction_id}') 