from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. User Management and RBAC
# ==========================================



# ==========================================
# 2. Suppliers and Categories
# ==========================================
class Supplier(models.Model):
    """
    Supplier model: External entities that supply goods and products.
    """
    name = models.CharField(max_length=255, verbose_name="Supplier Name")
    contact_person = models.CharField(max_length=255, blank=True, null=True, verbose_name="Contact Person")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=50, verbose_name="Phone")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Product categories to organize inventory and avoid data duplication (3NF).
    """
    name = models.CharField(max_length=150, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.name


# ==========================================
# 3. Product and Inventory Management
# ==========================================
class Product(models.Model):
    """
    Core product table: Tracks current stock quantity and low stock threshold for AI Agent triggers.
    """
    name = models.CharField(max_length=255, verbose_name="Product Name")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Category")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Primary Supplier")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Selling Price")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cost Price")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stock Quantity")
    low_stock_threshold = models.PositiveIntegerField(default=5, verbose_name="Low Stock Threshold")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Stock: {self.stock_quantity})"


# ==========================================
# 4. Customer Sales / Orders
# ==========================================
class Sale(models.Model):
    """
    Customer sales invoice header.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales', verbose_name="Customer")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sale Date")

    def __str__(self):
        return f"Sale Invoice #{self.id}"


class SaleItem(models.Model):
    """
    Line items within a sales invoice.
    """
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name="Sale Invoice")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sale_items', verbose_name="Product")
    quantity = models.PositiveIntegerField(verbose_name="Sold Quantity")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price at Sale")

    def get_cost(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"


# ==========================================
# 5. Smart Purchase Orders (AI Agent Core)
# ==========================================
class PurchaseOrder(models.Model):
    """
    Purchase orders sent to suppliers (automatically drafted by the AI Agent when stock is low).
    """
    STATUS_CHOICES = [
        ('draft', 'Draft (by AI)'),
        ('ordered', 'Ordered'),
        ('received', 'Received & Added to Stock'),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders', verbose_name="Supplier")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Order Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    notes = models.TextField(blank=True, null=True, verbose_name="Guidance Notes")

    def __str__(self):
        return f"Purchase Order #{self.id} - {self.supplier.name} ({self.get_status_display()})"


class PurchaseOrderItem(models.Model):
    """
    Products requested in the purchase order from the supplier.
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items', verbose_name="Purchase Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_items', verbose_name="Product")
    quantity = models.PositiveIntegerField(verbose_name="Requested Quantity")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Supplier Unit Price")

    def get_cost(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"Request {self.quantity} of {self.product.name}"