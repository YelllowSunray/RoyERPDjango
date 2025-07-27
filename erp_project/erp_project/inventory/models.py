from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
from datetime import datetime, timedelta

# Enum choices for various fields
class CategoryChoices(models.TextChoices):
    BIOLOGICAL = 'Biological', 'Biological'
    CHEMICAL = 'Chemical', 'Chemical'
    PACKAGING = 'Packaging', 'Packaging'
    PLASTICWARES = 'Plasticwares', 'Plasticwares'
    ELECTRICAL = 'Electrical', 'Electrical'
    EQUIPMENT = 'Equipment', 'Equipment'
    CONSUMABLES = 'Consumables', 'Consumables'
    STATIONERY = 'Stationery', 'Stationery'

class ChemicalSubtypeChoices(models.TextChoices):
    SOLVENT = 'Solvent', 'Solvent'
    FLAMMABLE_SOLID = 'Flammable Solid', 'Flammable Solid'
    COMPRESSED_GAS = 'Compressed Gas', 'Compressed Gas'
    OXIDIZER = 'Oxidizer', 'Oxidizer'
    CORROSIVE_ACID = 'Corrosive Acid', 'Corrosive Acid'
    CORROSIVE_BASE = 'Corrosive Base', 'Corrosive Base'
    REACTIVE = 'Reactive', 'Reactive'
    TOXIN = 'Toxin', 'Toxin'
    WASTE = 'Waste', 'Waste'
    PEROXIDE_FORMER = 'Peroxide-Former', 'Peroxide-Former'
    BIOHAZARD = 'Biohazard', 'Biohazard'
    NUTRIENT_INPUT = 'Nutrient Input', 'Nutrient Input'
    ACID = 'Acid', 'Acid'
    BASE = 'Base', 'Base'
    SALT = 'Salt', 'Salt'
    BUFFER = 'Buffer', 'Buffer'
    CATALYST = 'Catalyst', 'Catalyst'
    REAGENT = 'Reagent', 'Reagent'
    STANDARD = 'Standard', 'Standard'
    REFERENCE = 'Reference', 'Reference'
    INDICATOR = 'Indicator', 'Indicator'
    DYE = 'Dye', 'Dye'
    STABILIZER = 'Stabilizer', 'Stabilizer'
    PRESERVATIVE = 'Preservative', 'Preservative'
    ANTIOXIDANT = 'Antioxidant', 'Antioxidant'
    EMULSIFIER = 'Emulsifier', 'Emulsifier'
    THICKENER = 'Thickener', 'Thickener'
    FLAVORING = 'Flavoring', 'Flavoring'
    COLORING = 'Coloring', 'Coloring'
    SWEETENER = 'Sweetener', 'Sweetener'
    NUTRIENT = 'Nutrient', 'Nutrient'
    VITAMIN = 'Vitamin', 'Vitamin'
    MINERAL = 'Mineral', 'Mineral'
    AMINO_ACID = 'Amino Acid', 'Amino Acid'
    PEPTIDE = 'Peptide', 'Peptide'
    PROTEIN = 'Protein', 'Protein'
    ENZYME = 'Enzyme', 'Enzyme'
    HORMONE = 'Hormone', 'Hormone'
    ANTIBIOTIC = 'Antibiotic', 'Antibiotic'
    ANTIVIRAL = 'Antiviral', 'Antiviral'
    ANTIFUNGAL = 'Antifungal', 'Antifungal'
    ANTIPARASITIC = 'Antiparasitic', 'Antiparasitic'
    IMMUNOSUPPRESSANT = 'Immunosuppressant', 'Immunosuppressant'
    IMMUNOSTIMULANT = 'Immunostimulant', 'Immunostimulant'
    ANALGESIC = 'Analgesic', 'Analgesic'
    ANTIINFLAMMATORY = 'Anti-inflammatory', 'Anti-inflammatory'
    ANTIPYRETIC = 'Antipyretic', 'Antipyretic'
    ANTIHISTAMINE = 'Antihistamine', 'Antihistamine'
    DECONGESTANT = 'Decongestant', 'Decongestant'
    EXPECTORANT = 'Expectorant', 'Expectorant'
    LAXATIVE = 'Laxative', 'Laxative'
    ANTIDIARRHEAL = 'Antidiarrheal', 'Antidiarrheal'
    ANTACID = 'Antacid', 'Antacid'
    ANTIEMETIC = 'Antiemetic', 'Antiemetic'
    DIURETIC = 'Diuretic', 'Diuretic'
    VASODILATOR = 'Vasodilator', 'Vasodilator'
    VASOCONSTRICTOR = 'Vasoconstrictor', 'Vasoconstrictor'
    BRONCHODILATOR = 'Bronchodilator', 'Bronchodilator'
    MUSCLE_RELAXANT = 'Muscle Relaxant', 'Muscle Relaxant'
    SEDATIVE = 'Sedative', 'Sedative'
    STIMULANT = 'Stimulant', 'Stimulant'
    ANXIOLYTIC = 'Anxiolytic', 'Anxiolytic'
    ANTIDEPRESSANT = 'Antidepressant', 'Antidepressant'
    ANTIPSYCHOTIC = 'Antipsychotic', 'Antipsychotic'
    MOOD_STABILIZER = 'Mood Stabilizer', 'Mood Stabilizer'
    ANTICONVULSANT = 'Anticonvulsant', 'Anticonvulsant'
    ANTIARRHYTHMIC = 'Antiarrhythmic', 'Antiarrhythmic'
    ANTICOAGULANT = 'Anticoagulant', 'Anticoagulant'
    THROMBOLYTIC = 'Thrombolytic', 'Thrombolytic'
    HEMOSTATIC = 'Hemostatic', 'Hemostatic'
    PLASMA_EXPANDER = 'Plasma Expander', 'Plasma Expander'
    ELECTROLYTE = 'Electrolyte', 'Electrolyte'
    ALKALINIZING = 'Alkalizing', 'Alkalizing'
    ACIDIFYING = 'Acidifying', 'Acidifying'
    OSMOTIC_DIURETIC = 'Osmotic Diuretic', 'Osmotic Diuretic'
    CARBONIC_ANHYDRASE_INHIBITOR = 'Carbonic Anhydrase Inhibitor', 'Carbonic Anhydrase Inhibitor'
    ALDOSTERONE_ANTAGONIST = 'Aldosterone Antagonist', 'Aldosterone Antagonist'
    BETA_BLOCKER = 'Beta Blocker', 'Beta Blocker'
    ALPHA_BLOCKER = 'Alpha Blocker', 'Alpha Blocker'
    CALCIUM_CHANNEL_BLOCKER = 'Calcium Channel Blocker', 'Calcium Channel Blocker'
    ACE_INHIBITOR = 'ACE Inhibitor', 'ACE Inhibitor'
    ARB = 'ARB', 'Angiotensin Receptor Blocker'
    RENIN_INHIBITOR = 'Renin Inhibitor', 'Renin Inhibitor'
    STATIN = 'Statin', 'Statin'
    FIBRATE = 'Fibrate', 'Fibrate'
    NIACIN = 'Niacin', 'Niacin'
    BILE_ACID_SEQUESTRANT = 'Bile Acid Sequestrant', 'Bile Acid Sequestrant'
    PCSK9_INHIBITOR = 'PCSK9 Inhibitor', 'PCSK9 Inhibitor'
    INSULIN = 'Insulin', 'Insulin'
    SULFONYLUREA = 'Sulfonylurea', 'Sulfonylurea'
    BIGUANIDE = 'Biguanide', 'Biguanide'
    THIAZOLIDINEDIONE = 'Thiazolidinedione', 'Thiazolidinedione'
    DPP4_INHIBITOR = 'DPP-4 Inhibitor', 'DPP-4 Inhibitor'
    GLP1_AGONIST = 'GLP-1 Agonist', 'GLP-1 Agonist'
    SGLT2_INHIBITOR = 'SGLT2 Inhibitor', 'SGLT2 Inhibitor'
    ALPHA_GLUCOSIDASE_INHIBITOR = 'Alpha Glucosidase Inhibitor', 'Alpha Glucosidase Inhibitor'
    MEGLITINIDE = 'Meglitinide', 'Meglitinide'

class BiologicalSubtypeChoices(models.TextChoices):
    RAW_MATERIAL = 'Raw Material', 'Raw Material'
    ADDITIVE = 'Additive', 'Additive'
    CARRIER = 'Carrier', 'Carrier'
    FINISHED_PRODUCT = 'Finished Product', 'Finished Product'

class PackagingSubtypeChoices(models.TextChoices):
    BOTTLE = 'Bottle', 'Bottle'
    CAP = 'Cap', 'Cap'
    LABEL = 'Label', 'Label'
    BLISTER = 'Blister', 'Blister'
    DESICCANT = 'Desiccant', 'Desiccant'
    POUCH = 'Pouch', 'Pouch'
    BOX = 'Box', 'Box'

class PlasticwaresSubtypeChoices(models.TextChoices):
    TUBE = 'Tube', 'Tube'
    RACK = 'Rack', 'Rack'
    PIPETTE = 'Pipette', 'Pipette'
    CONTAINER = 'Container', 'Container'
    TIP_BOX = 'Tip Box', 'Tip Box'
    PLATE = 'Plate', 'Plate'

class ElectricalSubtypeChoices(models.TextChoices):
    SENSOR = 'Sensor', 'Sensor'
    CONNECTOR = 'Connector', 'Connector'
    PANEL = 'Panel', 'Panel'
    WIRING = 'Wiring', 'Wiring'
    CONTROLLER = 'Controller', 'Controller'

class EquipmentSubtypeChoices(models.TextChoices):
    MACHINE = 'Machine', 'Machine'
    TOOL = 'Tool', 'Tool'
    FILTER = 'Filter', 'Filter'
    PUMP = 'Pump', 'Pump'
    GLASSWARE = 'Glassware', 'Glassware'
    VALVE = 'Valve', 'Valve'

class ConsumablesSubtypeChoices(models.TextChoices):
    GLOVE = 'Glove', 'Glove'
    MASK = 'Mask', 'Mask'
    BATTERY = 'Battery', 'Battery'
    WIPE = 'Wipe', 'Wipe'
    APRON = 'Apron', 'Apron'
    CLEANING_AGENT = 'Cleaning Agent', 'Cleaning Agent'

class StationerySubtypeChoices(models.TextChoices):
    NOTEBOOK = 'Notebook', 'Notebook'
    MARKER = 'Marker', 'Marker'
    FILE = 'File', 'File'
    TAPE = 'Tape', 'Tape'
    BINDER = 'Binder', 'Binder'

class ChemicalFamilyChoices(models.TextChoices):
    # Oxidizers
    PEROXIDES = 'Peroxides', 'Peroxides'
    NITRATES = 'Nitrates', 'Nitrates'
    CHLORATES = 'Chlorates', 'Chlorates'
    
    # Solvents/Flammables
    ALCOHOLS = 'Alcohols', 'Alcohols'
    KETONES = 'Ketones', 'Ketones'
    HYDROCARBONS = 'Hydrocarbons', 'Hydrocarbons'
    
    # Corrosive Acids
    HYDROCHLORIC_ACID = 'Hydrochloric Acid (HCl)', 'Hydrochloric Acid (HCl)'
    NITRIC_ACID = 'Nitric Acid (HNO₃)', 'Nitric Acid (HNO₃)'
    CITRIC_ACID = 'Citric Acid', 'Citric Acid'
    
    # Corrosive Bases
    SODIUM_HYDROXIDE = 'Sodium Hydroxide (NaOH)', 'Sodium Hydroxide (NaOH)'
    POTASSIUM_HYDROXIDE = 'Potassium Hydroxide (KOH)', 'Potassium Hydroxide (KOH)'
    AMMONIA = 'Ammonia', 'Ammonia'
    
    # Peroxide-Formers
    DIETHYL_ETHER = 'Diethyl Ether', 'Diethyl Ether'
    TETRAHYDROFURAN = 'Tetrahydrofuran (THF)', 'Tetrahydrofuran (THF)'
    
    # Toxins/Poisons
    CYANIDES = 'Cyanides', 'Cyanides'
    AFLATOXINS = 'Aflatoxins', 'Aflatoxins'
    ARSENIC_COMPOUNDS = 'Arsenic Compounds', 'Arsenic Compounds'
    
    # Biohazards
    BACTERIA = 'Bacteria', 'Bacteria'
    VIRUSES = 'Viruses', 'Viruses'
    BLOODBORNE_PATHOGENS = 'Bloodborne Pathogens', 'Bloodborne Pathogens'

class GradeChoices(models.TextChoices):
    ACS = 'ACS', 'ACS'
    USP = 'USP', 'USP'
    FCC = 'FCC', 'FCC'
    LAB = 'Lab', 'Lab'
    TECH = 'Tech', 'Tech'
    CUSTOM = 'Custom', 'Custom'

class HazardClassChoices(models.TextChoices):
    FLAMMABLE = 'Flammable', 'Flammable'
    OXIDIZER = 'Oxidizer', 'Oxidizer'
    CORROSIVE = 'Corrosive', 'Corrosive'
    TOXIC = 'Toxic', 'Toxic'
    REACTIVE = 'Reactive', 'Reactive'
    NONE = 'None', 'None'

class ContaminationRiskChoices(models.TextChoices):
    LOW = 'Low', 'Low'
    MEDIUM = 'Medium', 'Medium'
    HIGH = 'High', 'High'

class TraceabilityLevelChoices(models.TextChoices):
    NONE = 'None', 'None'
    BASIC = 'Basic', 'Basic'
    BATCH_LEVEL = 'Batch-level', 'Batch-level'
    FULL = 'Full', 'Full'

class UOMChoices(models.TextChoices):
    KG = 'kg', 'kg'
    G = 'g', 'g'
    L = 'L', 'L'
    ML = 'ml', 'ml'
    BOTTLE = 'bottle', 'bottle'
    PCS = 'pcs', 'pcs'
    BOX = 'box', 'box'

class TransactionTypeChoices(models.TextChoices):
    RCV_PUR = 'RCV-PUR', 'Purchase Receipt'
    RCV_INT = 'RCV-INT', 'Internal Production Receipt'
    RCV_PACK = 'RCV-PACK', 'Packaging Material Receipt'
    RCV_ENG = 'RCV-ENG', 'Receive Engineering/Asset'
    RCV_MIS = 'RCV-MIS', 'Receive Miscellaneous Non-Tracked'
    ISS_MISC = 'ISS-MISC', 'Issue Miscellaneous'
    ADJ_CYCLE = 'ADJ-CYCLE', 'Cycle Count Adjustment'
    RCV_FG = 'RCV-FG', 'Receive Finished Goods from CM'
    ISS_MFG = 'ISS-MFG', 'Issue to Manufacturing'
    ISS_QC = 'ISS-QC', 'Issue to QC'
    ISS_RND = 'ISS-RND', 'Issue to R&D'
    XFER = 'XFER', 'Internal Transfer'
    RET_VND = 'RET-VND', 'Return to Vendor'
    RET_INT = 'RET-INT', 'Internal Return'
    ADJ_GAIN = 'ADJ-GAIN', 'Adjustment - Gain'
    ADJ_LOSS = 'ADJ-LOSS', 'Adjustment - Loss'
    SCRAP = 'SCRAP', 'Scrap/Disposal'
    SHIP_CUS = 'SHIP-CUS', 'Customer Shipment'
    SHIP_CM = 'SHIP-CM', 'Shipment to Contract Manufacturer'
    BLOCK = 'BLOCK', 'QA Hold/Blocked'
    RELEASE = 'RELEASE', 'Released from Hold'
    SAMPLE_IN = 'SAMPLE-IN', 'Sample Received'
    SAMPLE_OUT = 'SAMPLE-OUT', 'Sample Issued'

class QAStatusChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    APPROVED = 'Approved', 'Approved'
    QUARANTINED = 'Quarantined', 'Quarantined'
    REJECTED = 'Rejected', 'Rejected'

class ReviewOutcomeChoices(models.TextChoices):
    APPROVED = 'Approved', 'Approved'
    CONDITIONAL = 'Conditional', 'Conditional'
    REJECTED = 'Rejected', 'Rejected'
    ESCALATED = 'Escalated', 'Escalated'

class CustomerTypeChoices(models.TextChoices):
    RESEARCH = 'Research', 'Research'
    CLINICAL = 'Clinical', 'Clinical'
    COMMERCIAL = 'Commercial', 'Commercial'
    CM = 'CM', 'Contract Manufacturer'
    INTERNAL = 'Internal', 'Internal'

class ReviewFrequencyChoices(models.TextChoices):
    SIX_MONTHS = '6 months', '6 months'
    ONE_YEAR = '1 year', '1 year'
    ON_CHANGE = 'On change', 'On change'

# Add missing enums after existing ones
class DisposalMethodChoices(models.TextChoices):
    NEUTRALIZED = 'Neutralized', 'Neutralized'
    INCINERATED = 'Incinerated', 'Incinerated'
    RETURNED = 'Returned', 'Returned'
    LANDFILL = 'Landfill', 'Landfill'
    RECYCLED = 'Recycled', 'Recycled'
    COMPOSTED = 'Composted', 'Composted'
    AUTOCLAVED = 'Autoclaved', 'Autoclaved'
    CHEMICAL_TREATMENT = 'Chemical Treatment', 'Chemical Treatment'
    BIOLOGICAL_TREATMENT = 'Biological Treatment', 'Biological Treatment'
    THERMAL_TREATMENT = 'Thermal Treatment', 'Thermal Treatment'

class DispatchMethodChoices(models.TextChoices):
    COURIER = 'Courier', 'Courier'
    HAND_DELIVERY = 'Hand Delivery', 'Hand Delivery'
    POSTAL = 'Postal', 'Postal'
    EXPRESS = 'Express', 'Express'
    REFRIGERATED = 'Refrigerated', 'Refrigerated'
    FROZEN = 'Frozen', 'Frozen'
    CONTROLLED_TEMPERATURE = 'Controlled Temperature', 'Controlled Temperature'
    HAZARDOUS_MATERIAL = 'Hazardous Material', 'Hazardous Material'
    AIR_FREIGHT = 'Air Freight', 'Air Freight'
    SEA_FREIGHT = 'Sea Freight', 'Sea Freight'
    ROAD_FREIGHT = 'Road Freight', 'Road Freight'

class DocumentMatchChoices(models.TextChoices):
    YES = 'Yes', 'Yes'
    PARTIAL = 'Partial', 'Partial'
    NO = 'No', 'No'

# Master Data Tables
class Supplier(models.Model):
    """Supplier Master Table - A2.1"""
    supplier_id = models.CharField(max_length=20, primary_key=True, help_text="Unique identifier for the supplier")
    supplier_name = models.CharField(max_length=200, help_text="Full legal name of the supplier")
    business_unit = models.CharField(max_length=100, blank=True, help_text="If internal supplier, name of internal entity")
    address = models.TextField(help_text="Address and contact details")
    country_of_origin = models.CharField(max_length=3, help_text="Country where goods are produced")
    certifications = models.CharField(max_length=500, blank=True, help_text="Enum list of active certifications")
    approved = models.BooleanField(default=False, help_text="QA Approval status")
    approved_on = models.DateField(null=True, blank=True, help_text="Date of approval")
    last_reviewed_on = models.DateField(null=True, blank=True, help_text="Date QA last reviewed this supplier")
    review_frequency = models.CharField(max_length=20, choices=ReviewFrequencyChoices.choices, default=ReviewFrequencyChoices.ONE_YEAR)
    next_review_due = models.DateField(null=True, blank=True, help_text="When next QA check is expected")
    notes = models.TextField(blank=True, help_text="Optional comments on performance or conditions")
    
    def save(self, *args, **kwargs):
        # Calculate next review due date (Logic C5)
        if self.last_reviewed_on and self.review_frequency:
            if self.review_frequency == ReviewFrequencyChoices.SIX_MONTHS:
                self.next_review_due = self.last_reviewed_on + timedelta(days=180)
            elif self.review_frequency == ReviewFrequencyChoices.ONE_YEAR:
                self.next_review_due = self.last_reviewed_on + timedelta(days=365)
            # For 'On change', next_review_due remains blank (manual only)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.supplier_id} - {self.supplier_name}"
    
    class Meta:
        db_table = 'supplier_master'

class ItemRecord(models.Model):
    """Item Records Table - A2.1 (Key Fields)"""
    item_record_id = models.CharField(max_length=50, primary_key=True, help_text="Unique internal ID formatted as [CAT]-[SUB]-[CODE]")
    item_name = models.CharField(max_length=200, help_text="Standardized name aligned with label and QA docs")
    unit_of_measure = models.CharField(max_length=10, choices=UOMChoices.choices, help_text="Standard unit of measurement")
    category = models.CharField(max_length=20, choices=CategoryChoices.choices, help_text="Inventory grouping")
    subtype = models.CharField(max_length=50, help_text="Functional role within the category")
    grade = models.CharField(max_length=10, choices=GradeChoices.choices, blank=True, help_text="Purity or spec level")
    hazard_class = models.CharField(max_length=20, choices=HazardClassChoices.choices, blank=True, help_text="Regulatory hazard from SDS")
    chemical_family = models.CharField(max_length=100, choices=ChemicalFamilyChoices.choices, blank=True, help_text="Subgroup within hazard category")
    contamination_risk = models.CharField(max_length=10, choices=ContaminationRiskChoices.choices, default=ContaminationRiskChoices.LOW, help_text="Risk level for QA and traceability")
    critical_to_product = models.BooleanField(default=False, help_text="Flag for QA and traceability enforcement")
    
    # Additional fields from documentation
    spec_verified = models.BooleanField(default=False, help_text="Whether specification has been verified")
    segregation_rule_required = models.BooleanField(default=False, help_text="Whether segregation rules are required")
    
    # Derived fields (calculated by logic)
    qa_required = models.BooleanField(default=False, help_text="System-derived from grade, subtype, contamination, criticality")
    traceability_level = models.CharField(max_length=20, choices=TraceabilityLevelChoices.choices, default=TraceabilityLevelChoices.NONE, help_text="Derived traceability scope")
    sds_mandatory = models.BooleanField(default=False, help_text="Safety Data Sheet required?")
    coa_mandatory = models.BooleanField(default=False, help_text="Certificate of Analysis required?")
    spec_required = models.BooleanField(default=False, help_text="Specification document required?")
    
    def save(self, *args, **kwargs):
        # Calculate derived fields before saving
        self.calculate_derived_fields()
        super().save(*args, **kwargs)
    
    def calculate_derived_fields(self):
        """Implement LOGIC.C1, C2, C3 from documentation"""
        # LOGIC.C1 - QA Required?
        self.qa_required = calculate_qa_required(
            self.grade, 
            self.critical_to_product, 
            self.contamination_risk, 
            self.traceability_level
        )
        
        # LOGIC.C2 - Traceability Level (simplified for now)
        if self.qa_required and self.contamination_risk == 'High':
            self.traceability_level = TraceabilityLevelChoices.FULL
        elif self.qa_required:
            self.traceability_level = TraceabilityLevelChoices.BATCH_LEVEL
        else:
            self.traceability_level = TraceabilityLevelChoices.NONE
        
        # LOGIC.C3 - Document Requirements
        self.coa_mandatory, self.sds_mandatory, self.spec_required = calculate_document_requirements(
            self.qa_required, 
            self.hazard_class, 
            self.traceability_level
        )
        
        # LOGIC.C4 - Segregation Rule Required?
        self.segregation_rule_required = self.hazard_class in ['Flammable', 'Corrosive', 'Oxidizer', 'Reactive']
    
    @classmethod
    def get_subtype_choices(cls, category):
        """Get appropriate subtype choices based on category"""
        if category == CategoryChoices.BIOLOGICAL:
            return BiologicalSubtypeChoices.choices
        elif category == CategoryChoices.CHEMICAL:
            return ChemicalSubtypeChoices.choices
        elif category == CategoryChoices.PACKAGING:
            return PackagingSubtypeChoices.choices
        elif category == CategoryChoices.PLASTICWARES:
            return PlasticwaresSubtypeChoices.choices
        elif category == CategoryChoices.ELECTRICAL:
            return ElectricalSubtypeChoices.choices
        elif category == CategoryChoices.EQUIPMENT:
            return EquipmentSubtypeChoices.choices
        elif category == CategoryChoices.CONSUMABLES:
            return ConsumablesSubtypeChoices.choices
        elif category == CategoryChoices.STATIONERY:
            return StationerySubtypeChoices.choices
        else:
            return []
    
    def __str__(self):
        return f"{self.item_record_id} - {self.item_name}"
    
    class Meta:
        db_table = 'item_records'

class Product(models.Model):
    """Product Table - A2.1"""
    product_id = models.CharField(max_length=50, primary_key=True, help_text="Unique product identifier")
    product_name = models.CharField(max_length=200, help_text="Display name for the product")
    product_source = models.CharField(max_length=20, default='Internal', help_text="Clearly declares origin")
    category = models.CharField(max_length=20, choices=CategoryChoices.choices, help_text="Product group (aligns with Item Category)")
    subtype = models.CharField(max_length=50, help_text="Functional role of product")
    spec_version_linked = models.CharField(max_length=50, blank=True, help_text="Version of specification approved for this product")
    product_label_name = models.CharField(max_length=200, blank=True, help_text="Name used for label printing")
    default_unit_of_sale = models.CharField(max_length=100, help_text="Standard unit for packaging and sale")
    shelf_life_months = models.IntegerField(help_text="Maximum usable duration for product batches")
    qa_required = models.BooleanField(default=True, help_text="Whether QA sign-off is needed for release")
    traceability_required = models.CharField(max_length=20, choices=TraceabilityLevelChoices.choices, default=TraceabilityLevelChoices.BATCH_LEVEL, help_text="Minimum level of traceability")
    
    def __str__(self):
        return f"{self.product_id} - {self.product_name}"
    
    class Meta:
        db_table = 'product_master'

class ProductVersion(models.Model):
    """Product Version Table - A2.1"""
    product_version_id = models.CharField(max_length=50, primary_key=True, help_text="Unique identifier for version of product")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Foreign key reference to Product Table")
    sku = models.CharField(max_length=50, blank=True, help_text="SKU for finished biological products")
    subtype = models.CharField(max_length=50, help_text="Functional role within product category")
    spec_version = models.CharField(max_length=50, blank=True, help_text="Specific version of specification applied")
    status = models.CharField(max_length=20, choices=[('Draft', 'Draft'), ('Active', 'Active'), ('Obsolete', 'Obsolete')], default='Draft')
    effective_start_date = models.DateField(help_text="Start date of version applicability")
    effective_end_date = models.DateField(null=True, blank=True, help_text="End date of version applicability")
    notes = models.TextField(blank=True, help_text="Optional revision history or comments")
    
    def __str__(self):
        return f"{self.product_version_id} - {self.product_id.product_name}"
    
    class Meta:
        db_table = 'product_version'

class SupplierProduct(models.Model):
    """Supplier-Product Table - A2.1"""
    item_code = models.ForeignKey(ItemRecord, on_delete=models.CASCADE, help_text="FK to Item Master")
    supplier_name = models.ForeignKey(Supplier, on_delete=models.CASCADE, help_text="Vendor supplying the product")
    manufacturer_name = models.CharField(max_length=200, blank=True, help_text="Actual manufacturer")
    grade = models.CharField(max_length=10, choices=GradeChoices.choices, blank=True, help_text="Should align with Item Record grade")
    product_code = models.CharField(max_length=100, blank=True, help_text="Catalog or internal manufacturer code")
    packaging_description = models.CharField(max_length=200, blank=True, help_text="Commercial packaging unit")
    catalog_url = models.URLField(blank=True, help_text="Supplier page for cross-verification")
    batch_code_format_known = models.BooleanField(default=False, help_text="Whether batch code structure is known and documented")
    batch_code_quality = models.CharField(max_length=10, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium')
    traceability_level = models.CharField(max_length=20, choices=TraceabilityLevelChoices.choices, default=TraceabilityLevelChoices.NONE)
    coa_mandatory = models.BooleanField(default=False, help_text="Certificate of Analysis must be provided")
    sds_mandatory = models.BooleanField(default=False, help_text="Safety Data Sheet required")
    spec_sheet_file_url = models.URLField(blank=True, help_text="Upload or link to product spec")
    is_default = models.BooleanField(default=False, help_text="Preferred vendor-product pair")
    preferred_vendor = models.BooleanField(default=False, help_text="Preferred vendor flag")
    spec_verified = models.BooleanField(default=False, help_text="Whether specification has been verified")
    approved = models.BooleanField(default=False, help_text="Has QA formally approved this supplier for the item?")
    last_reviewed_on = models.DateField(null=True, blank=True, help_text="Date of last QA validation")
    next_review_due = models.DateField(null=True, blank=True, help_text="When next QA check is expected")
    review_frequency = models.CharField(max_length=20, choices=ReviewFrequencyChoices.choices, default=ReviewFrequencyChoices.SIX_MONTHS)
    
    def save(self, *args, **kwargs):
        # Calculate derived fields before saving
        self.calculate_derived_fields()
        super().save(*args, **kwargs)
    
    def calculate_derived_fields(self):
        """Implement LOGIC.C5, C6, C7 from documentation"""
        # LOGIC.C5 - Review Due Date
        if self.last_reviewed_on and self.review_frequency:
            if self.review_frequency == '6 months':
                self.next_review_due = self.last_reviewed_on + timedelta(days=180)
            elif self.review_frequency == '1 year':
                self.next_review_due = self.last_reviewed_on + timedelta(days=365)
        
        # LOGIC.C6 - Default Supplier-Product
        if self.approved and self.preferred_vendor:
            self.is_default = True
        
        # LOGIC.C7 - Spec Sheet Verified?
        # This would be set by QA during review process
    
    def __str__(self):
        return f"{self.item_code.item_record_id} - {self.supplier_name.supplier_name}"
    
    class Meta:
        db_table = 'supplier_product'
        unique_together = ['item_code', 'supplier_name']

class StorageZone(models.Model):
    """Storage Zone Table - A2.1"""
    zone_id = models.CharField(max_length=20, primary_key=True, help_text="Unique code for warehouse zone")
    zone_name = models.CharField(max_length=100, help_text="Human-readable name")
    temperature_range = models.CharField(max_length=50, blank=True, help_text="Temperature range supported")
    humidity_controlled = models.BooleanField(default=False, help_text="Whether humidity is regulated")
    hazard_compatibility = models.CharField(max_length=500, blank=True, help_text="Types of hazards permitted in zone")
    default_for_category = models.CharField(max_length=20, choices=CategoryChoices.choices, blank=True, help_text="If this zone is the default for a category")
    
    def __str__(self):
        return f"{self.zone_id} - {self.zone_name}"
    
    class Meta:
        db_table = 'storage_zone'

class StorageLocation(models.Model):
    """Storage Location Table - A2.1"""
    location_id = models.CharField(max_length=20, primary_key=True, help_text="Unique code for individual storage point")
    zone_id = models.ForeignKey(StorageZone, on_delete=models.CASCADE, help_text="FK to Storage Zone Table")
    rack_shelf = models.CharField(max_length=100, blank=True, help_text="Physical sub-location information")
    max_capacity = models.CharField(max_length=100, blank=True, help_text="Capacity in volume or units")
    active = models.BooleanField(default=True, help_text="Whether this location is active for use")
    
    def __str__(self):
        return f"{self.location_id} - {self.zone_id.zone_name}"
    
    class Meta:
        db_table = 'storage_location'

class Batch(models.Model):
    """Batch Table - A2.1"""
    batch_id = models.CharField(max_length=100, primary_key=True, help_text="Unique ID for each received or created batch")
    item_record_id = models.ForeignKey(ItemRecord, on_delete=models.CASCADE, help_text="Link to item definition")
    subtype = models.CharField(max_length=50, help_text="Subtype classification for the batch")
    supplier_code = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, help_text="Source supplier")
    supplier_product_id = models.ForeignKey(SupplierProduct, on_delete=models.SET_NULL, null=True, blank=True, help_text="ID of the supplier product (if procured externally)")
    batch_source = models.CharField(max_length=50, choices=[('External', 'External'), ('Internal', 'Internal'), ('CM', 'Contract Manufacturer')], default='External', help_text="Source of the batch")
    batch_type = models.CharField(max_length=50, choices=[('Production', 'Production'), ('R&D', 'R&D'), ('Sample', 'Sample'), ('Return', 'Return')], default='Production', help_text="Type of batch")
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount of material received")
    received_date = models.DateField(help_text="When the batch was received")
    expiry_date = models.DateField(help_text="Batch expiration date")
    qa_status = models.CharField(max_length=20, choices=QAStatusChoices.choices, default=QAStatusChoices.PENDING, help_text="Current QA status")
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True, blank=True, help_text="Where the batch is currently stored")
    
    def __str__(self):
        return f"{self.batch_id} - {self.item_record_id.item_name}"
    
    class Meta:
        db_table = 'batch_master'

class Customer(models.Model):
    """Customer Master Table - A2.1"""
    customer_code = models.CharField(max_length=20, primary_key=True, help_text="Unique identifier for the customer or recipient entity")
    customer_name = models.CharField(max_length=200, help_text="Full legal name of the institution or company")
    address_line1 = models.CharField(max_length=200, help_text="Primary address (building, street)")
    address_line2 = models.CharField(max_length=200, blank=True, help_text="Additional address details")
    city = models.CharField(max_length=100, help_text="City of recipient")
    state = models.CharField(max_length=100, help_text="State or province")
    postal_code = models.CharField(max_length=20, help_text="Postal/ZIP code")
    country = models.CharField(max_length=3, help_text="Country of customer")
    contact_person = models.CharField(max_length=100, help_text="Default contact for this recipient")
    phone = models.CharField(max_length=20, help_text="Phone number for contact")
    email = models.EmailField(blank=True, help_text="Contact email address")
    customer_type = models.CharField(max_length=20, choices=CustomerTypeChoices.choices, help_text="Type of customer")
    gstin = models.CharField(max_length=20, blank=True, help_text="GST identification number (India-specific)")
    preferred_courier = models.CharField(max_length=100, blank=True, help_text="Default courier preference")
    qa_required_before_ship = models.BooleanField(default=True, help_text="Whether QA approval must be completed before shipping")
    approved = models.BooleanField(default=False, help_text="Flag to enable/disable dispatch to this customer")
    approved_on = models.DateField(null=True, blank=True, help_text="Date customer was approved")
    remarks = models.TextField(blank=True, help_text="Optional notes")
    
    def __str__(self):
        return f"{self.customer_code} - {self.customer_name}"
    
    class Meta:
        db_table = 'customer_master'

# QA Review Tables - A2.2
class QAReview(models.Model):
    """QA Review Table - A2.2 Section 1: BATCH-LEVEL QA REVIEW"""
    qa_review_id = models.CharField(max_length=20, primary_key=True, help_text="Unique ID for this QA review record")
    batch_number = models.ForeignKey(Batch, on_delete=models.CASCADE, help_text="Batch under review")
    item_code = models.ForeignKey(ItemRecord, on_delete=models.CASCADE, help_text="Product or chemical being reviewed")
    supplier_code = models.ForeignKey(Supplier, on_delete=models.CASCADE, help_text="Source supplier")
    sub_ingredient_log = models.CharField(max_length=100, blank=True, help_text="Reference ID or path to the QA Sub-Ingredient Log")
    coa_match = models.BooleanField(help_text="COA matches product and batch spec")
    sds_match = models.BooleanField(help_text="SDS provided and valid for batch")
    spec_match = models.BooleanField(help_text="Matches defined internal specification")
    coa_attached = models.BooleanField(help_text="Digital COA file is stored")
    sds_attached = models.BooleanField(help_text="Digital SDS is stored")
    label_attached = models.BooleanField(help_text="Digital label image is available")
    spec_attached = models.BooleanField(help_text="Product spec sheet attached")
    document_match = models.CharField(max_length=10, choices=DocumentMatchChoices.choices, help_text="All documents carry same batch code")
    review_outcome = models.CharField(max_length=20, choices=ReviewOutcomeChoices.choices, help_text="Final QA result")
    qa_reviewer = models.CharField(max_length=50, help_text="QA personnel performing review")
    review_date = models.DateField(help_text="Date of QA review")
    qa_file_link = models.CharField(max_length=500, blank=True, help_text="Folder or path to QA documents")
    inventory_txn_id = models.CharField(max_length=20, blank=True, help_text="Linked transaction in inventory log")
    comments = models.TextField(blank=True, help_text="Free text comments or notes")
    
    def __str__(self):
        return f"{self.qa_review_id} - {self.batch_number.batch_id}"
    
    class Meta:
        db_table = 'qa_review'

class QAReviewUnit(models.Model):
    """QA Review Table - A2.2 Section 2: UNIT-LEVEL QA REVIEW"""
    qa_review_id = models.ForeignKey(QAReview, on_delete=models.CASCADE, help_text="Link to corresponding batch-level QA record")
    inventory_txn_id = models.CharField(max_length=20, blank=True, help_text="Link to inventory transaction")
    unit_id = models.CharField(max_length=20, help_text="Identifier for the unit")
    batch_number = models.ForeignKey(Batch, on_delete=models.CASCADE, help_text="Batch to which this unit belongs")
    sub_ingredient_log = models.CharField(max_length=100, blank=True, help_text="Reference ID or path to the QA Sub-Ingredient Log")
    visual_check = models.CharField(max_length=10, choices=[('Passed', 'Passed'), ('Failed', 'Failed')], help_text="Labeling, damage, visual QA")
    spec_check = models.CharField(max_length=10, choices=[('Passed', 'Passed'), ('Failed', 'Failed')], blank=True, help_text="Unit-level QC spec confirmation")
    disposition = models.CharField(max_length=20, choices=QAStatusChoices.choices, help_text="Approved, Quarantined, or Rejected")
    reviewer = models.CharField(max_length=50, help_text="QA reviewer ID")
    reviewed_on = models.DateField(help_text="Date of check")
    notes = models.TextField(blank=True, help_text="Comments or observations")
    
    def __str__(self):
        return f"{self.qa_review_id.qa_review_id} - {self.unit_id}"
    
    class Meta:
        db_table = 'qa_review_unit'

# Inventory Transaction Ledger - A2.3
class InventoryTransaction(models.Model):
    """Master Inventory Transaction Ledger - A2.3"""
    transaction_id = models.CharField(max_length=20, primary_key=True, help_text="Unique identifier for each inventory transaction")
    transaction_datetime = models.DateTimeField(help_text="Timestamp when the transaction occurred")
    transaction_user = models.CharField(max_length=50, help_text="User performing the transaction")
    transaction_type = models.CharField(max_length=20, choices=TransactionTypeChoices.choices, help_text="Type of transaction movement")
    comments = models.TextField(blank=True, help_text="Remarks or notes on the transaction")
    
    # Supplier/Recipient Information
    supplier_code = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, help_text="Identifier for supplier")
    supplier_name = models.CharField(max_length=200, blank=True, help_text="Name of supplier")
    recipient_code = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, help_text="Code of customer or recipient")
    recipient_company = models.CharField(max_length=200, blank=True, help_text="Full name of recipient")
    
    # Invoice Information
    invoice_no = models.CharField(max_length=50, blank=True, help_text="Vendor invoice number")
    invoice_date = models.DateField(null=True, blank=True, help_text="Date of invoice")
    
    # Product Information
    product_code = models.CharField(max_length=100, help_text="Product or catalog code from supplier")
    item_code = models.ForeignKey(ItemRecord, on_delete=models.CASCADE, help_text="Internal product code")
    product_name = models.CharField(max_length=200, help_text="Name of the product")
    
    # Batch and Unit Information
    batch_id = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, help_text="Batch or lot ID")
    unit_id = models.CharField(max_length=20, blank=True, help_text="Unit-level unique ID")
    
    # Dates
    mfg_date = models.DateField(null=True, blank=True, help_text="Date of manufacture")
    expiry_date = models.DateField(null=True, blank=True, help_text="Expiry or retest date")
    opened_date = models.DateField(null=True, blank=True, help_text="When item/container was first opened")
    
    # Quantity and Units
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity moved")
    unit = models.CharField(max_length=10, choices=UOMChoices.choices, help_text="Unit of measure")
    
    # Document Status
    coa_provided = models.BooleanField(default=False, help_text="COA document was provided")
    sds_provided = models.BooleanField(default=False, help_text="SDS document was provided")
    label_applied = models.BooleanField(default=False, help_text="Internal label was applied")
    
    # Storage Information
    storage_zone = models.ForeignKey(StorageZone, on_delete=models.SET_NULL, null=True, blank=True, help_text="Main storage zone")
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True, blank=True, help_text="Specific shelf/bin location")
    
    # QA Information
    qa_status = models.CharField(max_length=20, choices=QAStatusChoices.choices, blank=True, help_text="Quality disposition status")
    qa_review_id = models.ForeignKey(QAReview, on_delete=models.SET_NULL, null=True, blank=True, help_text="Linked QA Review record ID")
    qa_file_link = models.CharField(max_length=500, blank=True, help_text="Path to QA review files")
    sub_ingredient_log_id = models.CharField(max_length=100, blank=True, help_text="Reference to sub-ingredient QA log")
    
    # Document Matching
    coa_match = models.BooleanField(default=False, help_text="Whether COA matched expected")
    sds_match = models.BooleanField(default=False, help_text="Whether SDS matched expected")
    spec_match = models.BooleanField(default=False, help_text="Whether item met specification")
    
    # Usage Information
    used_in = models.CharField(max_length=100, blank=True, help_text="Linked production batch or experiment")
    used_by = models.CharField(max_length=50, blank=True, help_text="Person who used the item")
    used_date = models.DateField(null=True, blank=True, help_text="Date item was used")
    finished_date = models.DateField(null=True, blank=True, help_text="Date item was finished")
    
    # Return and Adjustment Information
    return_status = models.CharField(max_length=20, blank=True, help_text="Flag for return tracking")
    adjustment_reason = models.CharField(max_length=200, blank=True, help_text="Reason for manual adjustment")
    
    # Equipment Information
    serial_number = models.CharField(max_length=50, blank=True, help_text="Equipment serial number")
    maintenance_due_date = models.DateField(null=True, blank=True, help_text="Next preventive maintenance")
    calibration_date = models.DateField(null=True, blank=True, help_text="Date of last calibration")
    condition = models.CharField(max_length=20, choices=[('Good', 'Good'), ('Needs Repair', 'Needs Repair')], blank=True, help_text="Condition of item or asset")
    physical_location = models.CharField(max_length=200, blank=True, help_text="Actual location of item")
    
    # Dispatch Information
    recipient_contact = models.CharField(max_length=100, blank=True, help_text="Recipient's contact person")
    dispatch_method = models.CharField(max_length=50, choices=DispatchMethodChoices.choices, blank=True, help_text="Mode of dispatch")
    dispatch_address = models.CharField(max_length=500, blank=True, help_text="Where item was shipped to")
    courier_name = models.CharField(max_length=100, blank=True, help_text="Courier service used")
    tracking_number = models.CharField(max_length=50, blank=True, help_text="Tracking ID from courier")
    
    # Disposal Information
    disposed_date = models.DateField(null=True, blank=True, help_text="Date of disposal")
    disposed_by = models.CharField(max_length=50, blank=True, help_text="User who discarded the item")
    disposed_as = models.CharField(max_length=50, choices=DisposalMethodChoices.choices, blank=True, help_text="Disposal method used")
    disposal_comments = models.TextField(blank=True, help_text="Notes on disposal reason")
    
    def __str__(self):
        return f"{self.transaction_id} - {self.item_code.item_name} - {self.transaction_type}"
    
    class Meta:
        db_table = 'inventory_transaction'
        ordering = ['-transaction_datetime']

# Helper functions for derived field calculations
def calculate_qa_required(grade, critical_to_product, contamination_risk, traceability_level):
    """Logic C1 - QA Required? calculation"""
    if grade in ['USP', 'FCC', 'ACS', 'Food']:
        return True
    if critical_to_product:
        return True
    if contamination_risk == 'High':
        return True
    if traceability_level in ['Batch-level', 'Full']:
        return True
    return False

def calculate_traceability_level(qa_required, contamination_risk, batch_code_format_known, spec_verified):
    """Logic C2 - Traceability Level calculation"""
    if not qa_required and contamination_risk == 'Low':
        return 'None'
    if qa_required and (contamination_risk == 'Medium' or not batch_code_format_known):
        return 'Basic'
    if qa_required and batch_code_format_known and not spec_verified:
        return 'Batch-level'
    if qa_required and batch_code_format_known and spec_verified:
        return 'Full'
    return 'None'

def calculate_document_requirements(qa_required, hazard_class, traceability_level):
    """Logic C3 - COA/SDS/Spec Required? calculation"""
    coa_required = qa_required or traceability_level in ['Batch-level', 'Full']
    sds_required = hazard_class is not None and hazard_class != 'None'
    spec_required = qa_required or traceability_level in ['Batch-level', 'Full']
    
    return coa_required, sds_required, spec_required
