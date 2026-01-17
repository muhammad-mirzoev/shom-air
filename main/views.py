from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductSize
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    sort = request.GET.get('sort')
    allowed_sorts = ['name', '-name', 'price', '-price']

    if sort in allowed_sorts:
        products = products.order_by(sort)

    return render(request, 'main/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request, id, slug):
    # Получаем сам продукт
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    # Получаем похожие продукты из той же категории (кроме текущего)
    related_products = Product.objects.filter(category=product.category,
                                              available=True).exclude(id=product.id)[:4]

    # Форма добавления в корзину
    cart_product_form = CartAddProductForm()

    # Получаем все доступные размеры для этого продукта
    sizes = ProductSize.objects.filter(product=product)

    return render(request, 'main/product/detail.html', {
        'product': product,
        'related_products': related_products,
        'cart_product_form': cart_product_form,
        'sizes': sizes,  # передаем размеры в шаблон
    })
