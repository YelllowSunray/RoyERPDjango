from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Supplier, ItemRecord, Product, ProductVersion, SupplierProduct, Batch,
    StorageZone, StorageLocation, Customer, QAReview, QAReviewUnit, InventoryTransaction
)

# Master Data Admin
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['supplier_id', 'supplier_name', 'country_of_origin', 'approved', 'last_reviewed_on', 'review_frequency']
    list_filter = ['approved', 'country_of_origin', 'review_frequency']
    search_fields = ['supplier_id', 'supplier_name', 'business_unit']
    readonly_fields = ['approved_on', 'last_reviewed_on']
    fieldsets = (
        ('Basic Information', {
            'fields': ('supplier_id', 'supplier_name', 'business_unit', 'address', 'country_of_origin')
        }),
        ('QA Information', {
            'fields': ('certifications', 'approved', 'approved_on', 'last_reviewed_on', 'review_frequency')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )

@admin.register(ItemRecord)
class ItemRecordAdmin(admin.ModelAdmin):
    list_display = ['item_record_id', 'item_name', 'category', 'subtype', 'grade', 'qa_required', 'traceability_level']
    list_filter = ['category', 'grade', 'hazard_class', 'contamination_risk', 'qa_required', 'traceability_level']
    search_fields = ['item_record_id', 'item_name', 'chemical_family']
    readonly_fields = ['qa_required', 'traceability_level', 'sds_mandatory', 'coa_mandatory', 'spec_required']
    fieldsets = (
        ('Basic Information', {
            'fields': ('item_record_id', 'item_name', 'unit_of_measure', 'category', 'subtype')
        }),
        ('Quality Information', {
            'fields': ('grade', 'hazard_class', 'chemical_family', 'contamination_risk', 'critical_to_product')
        }),
        ('Derived Fields (System Calculated)', {
            'fields': ('qa_required', 'traceability_level', 'sds_mandatory', 'coa_mandatory', 'spec_required'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_name', 'category', 'subtype', 'shelf_life_months', 'qa_required']
    list_filter = ['category', 'subtype', 'qa_required', 'traceability_required']
    search_fields = ['product_id', 'product_name', 'product_label_name']
    fieldsets = (
        ('Basic Information', {
            'fields': ('product_id', 'product_name', 'product_source', 'category', 'subtype')
        }),
        ('Specification', {
            'fields': ('spec_version_linked', 'product_label_name', 'default_unit_of_sale', 'shelf_life_months')
        }),
        ('Quality Requirements', {
            'fields': ('qa_required', 'traceability_required')
        }),
    )

@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ['product_version_id', 'product_id', 'sku', 'status', 'effective_start_date', 'effective_end_date']
    list_filter = ['status', 'effective_start_date']
    search_fields = ['product_version_id', 'sku', 'product_id__product_name']
    fieldsets = (
        ('Version Information', {
            'fields': ('product_version_id', 'product_id', 'sku', 'subtype')
        }),
        ('Specification', {
            'fields': ('spec_version', 'status', 'effective_start_date', 'effective_end_date')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )

@admin.register(SupplierProduct)
class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ['item_code', 'supplier_name', 'grade', 'approved', 'is_default', 'last_reviewed_on']
    list_filter = ['approved', 'is_default', 'grade', 'batch_code_format_known', 'review_frequency']
    search_fields = ['item_code__item_name', 'supplier_name__supplier_name', 'product_code']
    readonly_fields = ['next_review_due']
    fieldsets = (
        ('Product Information', {
            'fields': ('item_code', 'supplier_name', 'manufacturer_name', 'grade', 'product_code')
        }),
        ('Packaging & Documentation', {
            'fields': ('packaging_description', 'catalog_url', 'spec_sheet_file_url')
        }),
        ('Batch & Traceability', {
            'fields': ('batch_code_format_known', 'batch_code_quality', 'traceability_level')
        }),
        ('QA Requirements', {
            'fields': ('coa_mandatory', 'sds_mandatory')
        }),
        ('Approval & Review', {
            'fields': ('is_default', 'approved', 'last_reviewed_on', 'next_review_due', 'review_frequency')
        }),
    )

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['batch_id', 'item_record_id', 'quantity_received', 'received_date', 'expiry_date', 'qa_status']
    list_filter = ['qa_status', 'received_date', 'expiry_date', 'subtype']
    search_fields = ['batch_id', 'item_record_id__item_name']
    readonly_fields = ['batch_id']
    fieldsets = (
        ('Batch Information', {
            'fields': ('batch_id', 'item_record_id', 'subtype', 'supplier_product_id')
        }),
        ('Quantity & Dates', {
            'fields': ('quantity_received', 'received_date', 'expiry_date')
        }),
        ('Status & Storage', {
            'fields': ('qa_status', 'storage_location')
        }),
    )

# Storage Admin
@admin.register(StorageZone)
class StorageZoneAdmin(admin.ModelAdmin):
    list_display = ['zone_id', 'zone_name', 'temperature_range', 'humidity_controlled', 'default_for_category']
    list_filter = ['humidity_controlled', 'default_for_category']
    search_fields = ['zone_id', 'zone_name']
    fieldsets = (
        ('Zone Information', {
            'fields': ('zone_id', 'zone_name')
        }),
        ('Environmental Controls', {
            'fields': ('temperature_range', 'humidity_controlled')
        }),
        ('Compatibility', {
            'fields': ('hazard_compatibility', 'default_for_category')
        }),
    )

@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ['location_id', 'zone_id', 'rack_shelf', 'max_capacity', 'active']
    list_filter = ['active', 'zone_id']
    search_fields = ['location_id', 'rack_shelf']
    fieldsets = (
        ('Location Information', {
            'fields': ('location_id', 'zone_id', 'rack_shelf')
        }),
        ('Capacity & Status', {
            'fields': ('max_capacity', 'active')
        }),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_code', 'customer_name', 'customer_type', 'city', 'country', 'approved']
    list_filter = ['customer_type', 'approved', 'country', 'qa_required_before_ship']
    search_fields = ['customer_code', 'customer_name', 'contact_person']
    readonly_fields = ['approved_on']
    fieldsets = (
        ('Basic Information', {
            'fields': ('customer_code', 'customer_name', 'customer_type')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'phone', 'email')
        }),
        ('Business Information', {
            'fields': ('gstin', 'preferred_courier')
        }),
        ('QA & Approval', {
            'fields': ('qa_required_before_ship', 'approved', 'approved_on')
        }),
        ('Notes', {
            'fields': ('remarks',)
        }),
    )

# QA Review Admin
@admin.register(QAReview)
class QAReviewAdmin(admin.ModelAdmin):
    list_display = ['qa_review_id', 'batch_number', 'item_code', 'supplier_code', 'review_outcome', 'review_date']
    list_filter = ['review_outcome', 'review_date', 'coa_match', 'sds_match', 'spec_match']
    search_fields = ['qa_review_id', 'batch_number__batch_id', 'item_code__item_name']
    readonly_fields = ['qa_review_id']
    fieldsets = (
        ('Review Information', {
            'fields': ('qa_review_id', 'batch_number', 'item_code', 'supplier_code', 'sub_ingredient_log')
        }),
        ('Document Matching', {
            'fields': ('coa_match', 'sds_match', 'spec_match', 'document_match')
        }),
        ('Document Attachments', {
            'fields': ('coa_attached', 'sds_attached', 'label_attached', 'spec_attached')
        }),
        ('Review Details', {
            'fields': ('review_outcome', 'qa_reviewer', 'review_date', 'qa_file_link', 'inventory_txn_id')
        }),
        ('Comments', {
            'fields': ('comments',)
        }),
    )

@admin.register(QAReviewUnit)
class QAReviewUnitAdmin(admin.ModelAdmin):
    list_display = ['unit_id', 'qa_review_id', 'batch_number', 'visual_check', 'disposition', 'reviewed_on']
    list_filter = ['visual_check', 'disposition', 'reviewed_on']
    search_fields = ['unit_id', 'qa_review_id__qa_review_id', 'batch_number__batch_id']
    fieldsets = (
        ('Unit Information', {
            'fields': ('qa_review_id', 'inventory_txn_id', 'unit_id', 'batch_number', 'sub_ingredient_log')
        }),
        ('Quality Checks', {
            'fields': ('visual_check', 'spec_check', 'disposition')
        }),
        ('Review Details', {
            'fields': ('reviewer', 'reviewed_on', 'notes')
        }),
    )

# Inventory Transaction Admin
@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'transaction_type', 'item_code', 'quantity', 'transaction_datetime', 'qa_status']
    list_filter = ['transaction_type', 'qa_status', 'transaction_datetime', 'coa_provided', 'sds_provided']
    search_fields = ['transaction_id', 'item_code__item_name', 'batch_id__batch_id', 'invoice_no']
    readonly_fields = ['transaction_id']
    date_hierarchy = 'transaction_datetime'
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_id', 'transaction_datetime', 'transaction_user', 'transaction_type', 'comments')
        }),
        ('Supplier/Recipient', {
            'fields': ('supplier_code', 'supplier_name', 'recipient_code', 'recipient_company')
        }),
        ('Invoice Information', {
            'fields': ('invoice_no', 'invoice_date')
        }),
        ('Product Information', {
            'fields': ('product_code', 'item_code', 'product_name')
        }),
        ('Batch & Unit Information', {
            'fields': ('batch_id', 'unit_id')
        }),
        ('Dates', {
            'fields': ('mfg_date', 'expiry_date', 'opened_date')
        }),
        ('Quantity & Units', {
            'fields': ('quantity', 'unit')
        }),
        ('Document Status', {
            'fields': ('coa_provided', 'sds_provided', 'label_applied')
        }),
        ('Storage Information', {
            'fields': ('storage_zone', 'storage_location')
        }),
        ('QA Information', {
            'fields': ('qa_status', 'qa_review_id', 'qa_file_link', 'sub_ingredient_log_id')
        }),
        ('Document Matching', {
            'fields': ('coa_match', 'sds_match', 'spec_match')
        }),
        ('Usage Information', {
            'fields': ('used_in', 'used_by', 'used_date', 'finished_date')
        }),
        ('Return & Adjustment', {
            'fields': ('return_status', 'adjustment_reason')
        }),
        ('Equipment Information', {
            'fields': ('serial_number', 'maintenance_due_date', 'calibration_date', 'condition', 'physical_location')
        }),
        ('Dispatch Information', {
            'fields': ('recipient_contact', 'dispatch_method', 'dispatch_address', 'courier_name', 'tracking_number')
        }),
        ('Disposal Information', {
            'fields': ('disposed_date', 'disposed_by', 'disposed_as', 'disposal_comments')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'item_code', 'batch_id', 'supplier_code', 'recipient_code', 
            'storage_zone', 'storage_location', 'qa_review_id'
        )

# Customize admin site
admin.site.site_header = "Pluviago ERP System"
admin.site.site_title = "Pluviago ERP Admin"
admin.site.index_title = "Welcome to Pluviago ERP Administration"
