# import base64
# import hashlib
import json
import requests
import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from cart.cart import Cart
from orders.models import Order


# stripe login
# stripe listen --forward-to localhost:8000/payment/stripe/webhook/


# HELEKET_API_KEY = settings.HELEKET_API_KEY
# HELEKET_BASE_URL = 'https://api.heleket.com/v1'
# HELEKET_SECRET_KEY = settings.HELEKET_SECRET_KEY

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


def create_stripe_checkout_session(order, request):
    cart = Cart(request)
    line_items = []

    for item in cart:
        product = item['product']
        line_items.append(
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': item['quantity'],
            }
        )

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=(
            request.build_absolute_uri('/payment/stripe/success/')
            + '?session_id={CHECKOUT_SESSION_ID}'
        ),
        cancel_url=(
            request.build_absolute_uri('/payment/stripe/cancel/')
            + f'?order_id={order.id}'
        ),
        metadata={'order_id': order.id},
    )

    order.stripe_payment_intent_id = checkout_session.payment_intent
    order.payment_provider = 'stripe'
    order.save()

    return checkout_session


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata'].get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponse(status=400)

        if order.status not in ('processing', 'completed'):
            order.status = 'processing'
            order.stripe_payment_intent_id = session.get('payment_intent')
            order.save()

    return HttpResponse(status=200)


def stripe_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('main:index')

    session = stripe.checkout.Session.retrieve(session_id)
    order_id = session.metadata.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    cart = Cart(request)
    cart.clear()

    context = {'order': order}
    if request.headers.get('HX-Request'):
        return TemplateResponse(
            request, 'payment/stripe_success_content.html', context
        )

    return render(request, 'payment/stripe_success.html', context)


def stripe_cancel(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return redirect('orders:checkout')

    order = get_object_or_404(Order, id=order_id)
    order.status = 'cancelled'
    order.save()

    context = {'order': order}
    if request.headers.get('HX-Request'):
        return TemplateResponse(
            request, 'payment/stripe_cancel_content.html', context
        )

    return render(request, 'payment/stripe_cancel.html', context)


"""
def create_heleket_payment(order, request):
    amount_str = f'{order.total_price:.2f}'
    payload = {
        'amount': amount_str,
        'currency': 'USDT',
        'order_id': str(order.id),
        'callback_url': request.build_absolute_uri(
            '/payment/heleket/webhook/'
        ),
        'description': f'Order #{order.id}',
        'convert_to': 'USDT',
    }

    payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    encoded_payload = base64.b64encode(
        payload_str.encode('utf-8')
    ).decode('utf-8')

    sign = hashlib.md5(
        (encoded_payload + HELEKET_SECRET_KEY).encode('utf-8')
    ).hexdigest()

    headers = {
        'merchant': HELEKET_API_KEY,
        'sign': sign,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        f'{HELEKET_BASE_URL}/payment',
        headers=headers,
        data=payload_str,
        timeout=10,
    )

    if response.status_code != 200:
        raise Exception(f'Heleket API error: {response.text}')

    payment = response.json()
    if payment.get('state') != 0:
        raise Exception(f'Error creating Heleket payment: {response.text}')

    order.heleket_payment_id = payment.get('result', {}).get('uuid')
    order.payment_provider = 'heleket'
    order.save()

    return payment['result']


@csrf_exempt
@require_POST
def heleket_webhook(request):
    signature = request.headers.get('sign')
    payload = request.body.decode('utf-8')

    encoded_payload = base64.b64encode(
        payload.encode('utf-8')
    ).decode('utf-8')

    expected = hashlib.md5(
        (encoded_payload + HELEKET_SECRET_KEY).encode('utf-8')
    ).hexdigest()

    if signature != expected:
        return HttpResponseBadRequest('Invalid signature')

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    result = data.get('result', {})
    payment_id = result.get('uuid')
    status = result.get('payment_status')
    order_id = result.get('order_id')

    if not order_id:
        return HttpResponseBadRequest('Missing order_id')

    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponseBadRequest('Order not found')

        if status == 'paid':
            if order.status != 'completed':
                order.status = 'completed'
                order.heleket_payment_id = payment_id
                order.save()

        elif status in {
            'fail',
            'cancel',
            'system_fail',
            'wrong_amount',
            'refund_fail',
        }:
            if order.status != 'cancelled':
                order.status = 'cancelled'
                order.save()

    return HttpResponse(status=200)


def heleket_success(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return redirect('orders:checkout')

    order = get_object_or_404(Order, id=order_id)

    if order.status == 'completed':
        cart = Cart(request)
        cart.clear()

        context = {'order': order}
        if request.headers.get('HX-Request'):
            return TemplateResponse(
                request, 'payment/heleket_success_content.html', context
            )

        return render(request, 'payment/heleket_success.html', context)

    if order.status == 'cancelled':
        return redirect('payment:heleket_cancel')

    context = {'order': order}
    if request.headers.get('HX-Request'):
        return TemplateResponse(
            request, 'payment/heleket_pending_content.html', context
        )

    return render(request, 'payment/heleket_pending.html', context)


def heleket_cancel(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return redirect('orders:checkout')

    order = get_object_or_404(Order, id=order_id)
    order.status = 'cancelled'
    order.save()

    context = {'order': order}
    if request.headers.get('HX-Request'):
        return TemplateResponse(
            request, 'payment/heleket_cancel_content.html', context
        )

    return render(request, 'payment/heleket_cancel.html', context)
"""