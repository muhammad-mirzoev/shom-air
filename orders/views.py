from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import View
from .forms import OrderForm
from .models import Order, OrderItem
from cart.cart import Cart
from main.models import ProductSize
from django.shortcuts import get_object_or_404
from payment.views import create_stripe_checkout_session, create_heleket_payment
import logging

logger = logging.getLogger(__name__)


@method_decorator(login_required(login_url='/users/login'), name='dispatch')
class CheckoutView(View):

    def get(self, request):
        cart = Cart(request)

        if len(cart) == 0:
            if request.headers.get('HX-Request'):
                return TemplateResponse(
                    request,
                    'orders/empty_cart.html',
                    {'message': 'Ваша корзина пуста'}
                )
            return redirect('cart:cart_detail')

        form = OrderForm(user=request.user)

        context = {
            'form': form,
            'cart': cart,
            'total_price': cart.get_total_price(),
        }

        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'orders/checkout_content.html', context)

        return render(request, 'orders/checkout.html', context)

    def post(self, request):
        cart = Cart(request)
        payment_provider = request.POST.get('payment_provider')

        if len(cart) == 0:
            return redirect('cart:cart_detail')

        if payment_provider not in ['stripe', 'heleket']:
            form = OrderForm(user=request.user)
            return render(request, 'orders/checkout.html', {
                'form': form,
                'cart': cart,
                'total_price': cart.get_total_price(),
                'error_message': 'Выберите способ оплаты',
            })

        form_data = request.POST.copy()
        if not form_data.get('email'):
            form_data['email'] = request.user.email

        form = OrderForm(form_data, user=request.user)

        if not form.is_valid():
            return render(request, 'orders/checkout.html', {
                'form': form,
                'cart': cart,
                'total_price': cart.get_total_price(),
                'error_message': 'Исправьте ошибки в форме',
            })

        # ---- СОЗДАЁМ ЗАКАЗ ----
        order = Order.objects.create(
            user=request.user,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            company=form.cleaned_data['company'],
            address1=form.cleaned_data['address1'],
            address2=form.cleaned_data['address2'],
            city=form.cleaned_data['city'],
            country=form.cleaned_data['country'],
            province=form.cleaned_data['province'],
            postal_code=form.cleaned_data['postal_code'],
            phone=form.cleaned_data['phone'],
            total_price=cart.get_total_price(),
            payment_provider=payment_provider,
        )

        # ---- СОЗДАЁМ OrderItem ----
        for item in cart:
            product_size = get_object_or_404(ProductSize, id=item['size'])

        OrderItem.objects.create(
            order=order,
            product=item['product'],
            size=product_size,
            quantity=item['quantity'],
            price=item['price'],
        )

        # ---- ОПЛАТА ----
        try:
            if payment_provider == 'stripe':
                session = create_stripe_checkout_session(order, request)
                cart.clear()
                return redirect(session.url)

            if payment_provider == 'heleket':
                payment = create_heleket_payment(order, request)
                cart.clear()
                return redirect(payment['url'])

        except Exception as e:
            order.delete()
            return render(request, 'orders/checkout.html', {
                'form': form,
                'cart': cart,
                'total_price': cart.get_total_price(),
                'error_message': str(e),
            })
