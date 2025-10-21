from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    MedicineCategory, Medicine, Customer, Prescription, PrescriptionItem,
    Bill, BillItem, Payment, StockMovement, Supplier, PurchaseOrder, PurchaseOrderItem
)


@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'generic_name', 'manufacturer', 'category', 'unit', 'strength',
        'stock_quantity', 'selling_price', 'is_low_stock', 'is_active'
    ]
    list_filter = ['category', 'unit', 'requires_prescription', 'is_controlled_substance', 'is_active']
    search_fields = ['name', 'generic_name', 'manufacturer', 'medicine_code', 'barcode']
    list_editable = ['stock_quantity', 'selling_price', 'is_active']
    readonly_fields = ['medicine_code', 'barcode', 'profit_margin']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'generic_name', 'manufacturer', 'category', 'unit', 'strength', 'description')
        }),
        ('Inventory Management', {
            'fields': ('stock_quantity', 'minimum_stock', 'maximum_stock', 'expiry_date')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price', 'margin_percentage', 'profit_margin')
        }),
        ('Prescription & Control', {
            'fields': ('requires_prescription', 'is_controlled_substance')
        }),
        ('Identification', {
            'fields': ('medicine_code', 'barcode')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def is_low_stock(self, obj):
        if obj.is_low_stock:
            return format_html('<span style="color: red;">⚠️ Low Stock</span>')
        return format_html('<span style="color: green;">✓ Good</span>')
    is_low_stock.short_description = 'Stock Status'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'full_name', 'phone', 'email', 'city', 'is_active', 'created_at']
    list_filter = ['is_active', 'gender', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'email', 'customer_id']
    list_editable = ['is_active']
    readonly_fields = ['customer_id', 'age']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('customer_id', 'first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender', 'age')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'city', 'state', 'pincode')
        }),
        ('Medical Information', {
            'fields': ('allergies', 'medical_conditions')
        }),
        ('Insurance Information', {
            'fields': ('insurance_provider', 'insurance_number', 'insurance_validity')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1
    fields = ['medicine', 'dosage', 'frequency', 'duration', 'quantity', 'unit_price', 'total_price']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_id', 'customer', 'doctor_name', 'prescription_date', 'status', 'total_amount']
    list_filter = ['status', 'prescription_date', 'created_at']
    search_fields = ['prescription_id', 'customer__first_name', 'customer__last_name', 'doctor_name']
    list_editable = ['status']
    readonly_fields = ['prescription_id', 'total_amount']
    inlines = [PrescriptionItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('prescription_id', 'customer', 'prescription_date')
        }),
        ('Doctor Information', {
            'fields': ('doctor_name', 'doctor_license', 'clinic_name')
        }),
        ('Prescription Details', {
            'fields': ('diagnosis', 'symptoms', 'instructions', 'notes')
        }),
        ('Status', {
            'fields': ('status', 'dispensed_at')
        }),
    )


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1
    fields = ['medicine', 'quantity', 'unit_price', 'total_price', 'batch_number', 'expiry_date']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = [
        'bill_id', 'customer', 'bill_date', 'total_amount', 'payment_status',
        'paid_amount', 'balance_amount', 'created_by'
    ]
    list_filter = ['payment_status', 'payment_method', 'bill_date', 'created_at']
    search_fields = ['bill_id', 'customer__first_name', 'customer__last_name', 'customer__phone']
    list_editable = ['payment_status']
    readonly_fields = ['bill_id', 'subtotal', 'total_amount', 'balance_amount']
    inlines = [BillItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('bill_id', 'customer', 'prescription', 'bill_date', 'created_by')
        }),
        ('Bill Details', {
            'fields': ('subtotal', 'discount_amount', 'discount_percentage', 'tax_amount', 'tax_percentage', 'total_amount')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'paid_amount', 'balance_amount', 'paid_at')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'bill', 'customer', 'amount', 'payment_method', 'payment_status', 'payment_date']
    list_filter = ['payment_method', 'payment_status', 'payment_date', 'created_at']
    search_fields = ['payment_id', 'bill__bill_id', 'customer__first_name', 'customer__last_name', 'transaction_id']
    list_editable = ['payment_status']
    readonly_fields = ['payment_id']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('payment_id', 'bill', 'customer', 'amount', 'payment_date')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'payment_status', 'transaction_id')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by')
        }),
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'movement_type', 'quantity', 'previous_stock', 'new_stock', 'movement_date', 'created_by']
    list_filter = ['movement_type', 'movement_date', 'created_at']
    search_fields = ['medicine__name', 'reference_number', 'notes']
    readonly_fields = ['previous_stock', 'new_stock']
    
    fieldsets = (
        ('Movement Information', {
            'fields': ('medicine', 'movement_type', 'quantity', 'previous_stock', 'new_stock')
        }),
        ('Reference Information', {
            'fields': ('reference_number', 'notes', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('movement_date',)
        }),
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'city', 'credit_limit', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'phone', 'email', 'gst_number']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'contact_person', 'phone', 'email')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Business Information', {
            'fields': ('gst_number', 'license_number', 'credit_limit')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    fields = ['medicine', 'quantity', 'unit_price', 'total_price', 'batch_number', 'expiry_date']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'order_date', 'status', 'total_amount', 'created_by']
    list_filter = ['status', 'order_date', 'created_at']
    search_fields = ['po_number', 'supplier__name', 'notes']
    list_editable = ['status']
    readonly_fields = ['po_number', 'subtotal', 'total_amount']
    inlines = [PurchaseOrderItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('po_number', 'supplier', 'order_date', 'expected_delivery', 'created_by')
        }),
        ('Order Details', {
            'fields': ('status', 'subtotal', 'tax_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


# Custom admin site configuration
admin.site.site_header = "Mediwell Care Pharmacy Management"
admin.site.site_title = "Pharmacy Admin"
admin.site.index_title = "Pharmacy Management System"