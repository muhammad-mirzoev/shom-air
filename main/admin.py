from django.contrib import admin
from .models import Category, Product, Size, ProductSize

# ===== Category =====
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# ===== ProductSize Inline =====
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # сколько пустых полей показывать по умолчанию

# ===== Product =====
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline]  # Включаем размеры прямо на странице продукта

# ===== Size =====
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ===== ProductSize =====
@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'stock')
    list_filter = ('product', 'size')
