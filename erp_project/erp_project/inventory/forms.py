from django import forms
from .models import (
    ItemRecord, Supplier, Customer, Batch, InventoryTransaction, QAReview,
    CategoryChoices, ChemicalSubtypeChoices, BiologicalSubtypeChoices,
    PackagingSubtypeChoices, PlasticwaresSubtypeChoices, ElectricalSubtypeChoices,
    EquipmentSubtypeChoices, ConsumablesSubtypeChoices, StationerySubtypeChoices,
    GradeChoices, HazardClassChoices, ChemicalFamilyChoices, UOMChoices
)

class ItemRecordForm(forms.ModelForm):
    """Form for creating/editing ItemRecord with dynamic subtype choices"""
    
    class Meta:
        model = ItemRecord
        fields = [
            'item_record_id', 'item_name', 'unit_of_measure', 'category', 'subtype',
            'grade', 'hazard_class', 'chemical_family', 'contamination_risk',
            'critical_to_product'
        ]
        widgets = {
            'item_record_id': forms.TextInput(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_of_measure': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'onchange': 'updateSubtypeChoices()'}),
            'subtype': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'hazard_class': forms.Select(attrs={'class': 'form-control'}),
            'chemical_family': forms.Select(attrs={'class': 'form-control'}),
            'contamination_risk': forms.Select(attrs={'class': 'form-control'}),
            'critical_to_product': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial subtype choices based on category
        if self.instance and self.instance.category:
            self.fields['subtype'].choices = self.get_subtype_choices(self.instance.category)
        else:
            self.fields['subtype'].choices = [('', 'Select a category first')]
        
        # Show/hide chemical family based on category
        if self.instance and self.instance.category != CategoryChoices.CHEMICAL:
            self.fields['chemical_family'].widget = forms.HiddenInput()
            self.fields['hazard_class'].widget = forms.HiddenInput()
    
    def get_subtype_choices(self, category):
        """Get appropriate subtype choices based on category"""
        if category == CategoryChoices.BIOLOGICAL:
            return [('', 'Select subtype')] + list(BiologicalSubtypeChoices.choices)
        elif category == CategoryChoices.CHEMICAL:
            return [('', 'Select subtype')] + list(ChemicalSubtypeChoices.choices)
        elif category == CategoryChoices.PACKAGING:
            return [('', 'Select subtype')] + list(PackagingSubtypeChoices.choices)
        elif category == CategoryChoices.PLASTICWARES:
            return [('', 'Select subtype')] + list(PlasticwaresSubtypeChoices.choices)
        elif category == CategoryChoices.ELECTRICAL:
            return [('', 'Select subtype')] + list(ElectricalSubtypeChoices.choices)
        elif category == CategoryChoices.EQUIPMENT:
            return [('', 'Select subtype')] + list(EquipmentSubtypeChoices.choices)
        elif category == CategoryChoices.CONSUMABLES:
            return [('', 'Select subtype')] + list(ConsumablesSubtypeChoices.choices)
        elif category == CategoryChoices.STATIONERY:
            return [('', 'Select subtype')] + list(StationerySubtypeChoices.choices)
        else:
            return [('', 'Select a category first')]

class SupplierForm(forms.ModelForm):
    """Form for creating/editing Supplier"""
    
    class Meta:
        model = Supplier
        fields = [
            'supplier_id', 'supplier_name', 'business_unit', 'address',
            'country_of_origin', 'certifications', 'approved', 'approved_on',
            'last_reviewed_on', 'review_frequency', 'notes'
        ]
        widgets = {
            'supplier_id': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'country_of_origin': forms.TextInput(attrs={'class': 'form-control'}),
            'certifications': forms.TextInput(attrs={'class': 'form-control'}),
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'approved_on': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_reviewed_on': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'review_frequency': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CustomerForm(forms.ModelForm):
    """Form for creating/editing Customer"""
    
    class Meta:
        model = Customer
        fields = [
            'customer_code', 'customer_name', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country', 'contact_person',
            'phone', 'email', 'customer_type', 'gstin', 'preferred_courier',
            'qa_required_before_ship', 'approved', 'approved_on', 'remarks'
        ]
        widgets = {
            'customer_code': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'gstin': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_courier': forms.TextInput(attrs={'class': 'form-control'}),
            'qa_required_before_ship': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'approved_on': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BatchForm(forms.ModelForm):
    """Form for creating/editing Batch"""
    
    class Meta:
        model = Batch
        fields = [
            'batch_id', 'item_record_id', 'subtype', 'supplier_code',
            'supplier_product_id', 'batch_source', 'batch_type',
            'quantity_received', 'received_date', 'expiry_date',
            'qa_status', 'storage_location'
        ]
        widgets = {
            'batch_id': forms.TextInput(attrs={'class': 'form-control'}),
            'item_record_id': forms.Select(attrs={'class': 'form-control'}),
            'subtype': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_code': forms.Select(attrs={'class': 'form-control'}),
            'supplier_product_id': forms.Select(attrs={'class': 'form-control'}),
            'batch_source': forms.Select(attrs={'class': 'form-control'}),
            'batch_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity_received': forms.NumberInput(attrs={'class': 'form-control'}),
            'received_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'qa_status': forms.Select(attrs={'class': 'form-control'}),
            'storage_location': forms.Select(attrs={'class': 'form-control'}),
        }

class InventoryTransactionForm(forms.ModelForm):
    """Form for creating/editing InventoryTransaction"""
    
    class Meta:
        model = InventoryTransaction
        fields = [
            'transaction_id', 'transaction_datetime', 'transaction_user',
            'transaction_type', 'comments', 'supplier_code', 'supplier_name',
            'recipient_code', 'recipient_company', 'invoice_no', 'invoice_date',
            'product_code', 'item_code', 'product_name', 'batch_id', 'unit_id',
            'mfg_date', 'expiry_date', 'opened_date', 'quantity', 'unit',
            'coa_provided', 'sds_provided', 'label_applied', 'storage_zone',
            'storage_location', 'qa_status', 'qa_review_id', 'qa_file_link',
            'sub_ingredient_log_id', 'coa_match', 'sds_match', 'spec_match',
            'used_in', 'used_by', 'used_date', 'finished_date', 'return_status',
            'adjustment_reason', 'serial_number', 'maintenance_due_date',
            'calibration_date', 'condition', 'physical_location',
            'recipient_contact', 'dispatch_method', 'dispatch_address',
            'courier_name', 'tracking_number', 'disposed_date', 'disposed_by',
            'disposed_as', 'disposal_comments'
        ]
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'transaction_user': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'supplier_code': forms.Select(attrs={'class': 'form-control'}),
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'recipient_code': forms.Select(attrs={'class': 'form-control'}),
            'recipient_company': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control'}),
            'item_code': forms.Select(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_id': forms.Select(attrs={'class': 'form-control'}),
            'unit_id': forms.TextInput(attrs={'class': 'form-control'}),
            'mfg_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'opened_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'coa_provided': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sds_provided': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'label_applied': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'storage_zone': forms.Select(attrs={'class': 'form-control'}),
            'storage_location': forms.Select(attrs={'class': 'form-control'}),
            'qa_status': forms.Select(attrs={'class': 'form-control'}),
            'qa_review_id': forms.Select(attrs={'class': 'form-control'}),
            'qa_file_link': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_ingredient_log_id': forms.TextInput(attrs={'class': 'form-control'}),
            'coa_match': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sds_match': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'spec_match': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'used_in': forms.TextInput(attrs={'class': 'form-control'}),
            'used_by': forms.TextInput(attrs={'class': 'form-control'}),
            'used_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'finished_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_status': forms.TextInput(attrs={'class': 'form-control'}),
            'adjustment_reason': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'maintenance_due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'calibration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'physical_location': forms.TextInput(attrs={'class': 'form-control'}),
            'recipient_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'dispatch_method': forms.Select(attrs={'class': 'form-control'}),
            'dispatch_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'courier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
            'disposed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'disposed_by': forms.TextInput(attrs={'class': 'form-control'}),
            'disposed_as': forms.Select(attrs={'class': 'form-control'}),
            'disposal_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class QAReviewForm(forms.ModelForm):
    """Form for creating/editing QAReview"""
    
    class Meta:
        model = QAReview
        fields = [
            'qa_review_id', 'batch_number', 'item_code', 'supplier_code',
            'sub_ingredient_log', 'coa_match', 'sds_match', 'spec_match',
            'coa_attached', 'sds_attached', 'label_attached', 'spec_attached',
            'document_match', 'review_outcome', 'qa_reviewer', 'review_date',
            'qa_file_link', 'inventory_txn_id', 'comments'
        ]
        widgets = {
            'qa_review_id': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_number': forms.Select(attrs={'class': 'form-control'}),
            'item_code': forms.Select(attrs={'class': 'form-control'}),
            'supplier_code': forms.Select(attrs={'class': 'form-control'}),
            'sub_ingredient_log': forms.TextInput(attrs={'class': 'form-control'}),
            'coa_match': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sds_match': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'spec_match': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'coa_attached': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sds_attached': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'label_attached': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'spec_attached': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'document_match': forms.Select(attrs={'class': 'form-control'}),
            'review_outcome': forms.Select(attrs={'class': 'form-control'}),
            'qa_reviewer': forms.TextInput(attrs={'class': 'form-control'}),
            'review_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'qa_file_link': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_txn_id': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 