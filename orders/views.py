from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct

import razorpay
from GreatKart import settings

import razorpay
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.http import JsonResponse
from .models import Order, Payment  # adjust based on your structure

# Razorpay client initialization
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payments(request):
     return render(request, 'orders/payments.html')

def place_order(request,total=0, quantity=0,):
        current_user = request.user

        # If the cart count is less than or equal to 0, then redirect back to shop
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count <= 0:
            return redirect('store')

        grand_total = 0
        tax = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                # Store all the billing information inside Order table
                data = Order()
                data.user = current_user
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                data.address_line_1 = form.cleaned_data['address_line_1']
                data.address_line_2 = form.cleaned_data['address_line_2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.order_note = form.cleaned_data['order_note']
                data.order_total = grand_total
                data.tax = tax
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()

                # Generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()
               # return redirect('checkout')

                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
                context = {
                    'order': order,
                    'cart_items': cart_items,
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total,
                }
                return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')

# def create_order(request):
#     if request.method == 'POST':
#         try:
#             amount = round(float(request.POST['amount']), 2)  # Convert to paise
#             print("Amount received:", amount)

#             if not amount or amount <= 0:
#                 return JsonResponse({"error": "Invalid amount provided."})

#             order_data = {
#                 "amount": amount,
#                 "currency": "INR",
#                 "payment_capture": True
#             }

#             # Try creating Razorpay order (with retry logic)
#             for _ in range(3):
#                 try:
#                     order_response = client.order.create(order_data)
#                     print("Order response:", order_response)
#                     break
#                 except Exception as e:
#                      print("Order creation error:", str(e))
#             else:
#                 return JsonResponse({"error": "Failed to create order after retries."})

#             # Create Order object
#             order = Order.objects.create(
#                 user=request.user,
#                 order_total=amount / 100,  # Stored in INR
#                 razorpay_order_id=order_response['id'],
#                 is_ordered=False,  # Optional but explicit
#                 status='Pending'
#             )

#             # Create Payment object
#             payment = Payment.objects.create(
#                 user=request.user,
#                 order=order,
#                 amount=amount / 100,
#                 payment_method='Razorpay',
#                 status='Pending',
#                 transaction_id=order_response['id']
#             )

#             # Link payment to order (optional but explicit)
#             order.payment = payment
#             order.save()

#             # Send order data to frontend
#             return JsonResponse({
#                 "order_id": order_response['id'],
#                 "key": settings.RAZORPAY_KEY_ID,
#                 "amount": amount
#             })

#         except Exception as e:
#             print("Exception in create_order:", str(e))
#             return JsonResponse({"error": str(e)})

#     return JsonResponse({"error": "Invalid request"})

# from decimal import Decimal
# import razorpay.errors

# def create_order(request):
#     if request.method == 'POST':
#         try:
#             amount_rupees = Decimal(request.POST['amount'])
#             amount_paise = int(amount_rupees * 100)
#             print("Amount (paise):", amount_paise)

#             if amount_paise <= 0:
#                 return JsonResponse({"error": "Invalid amount."})

#             order_data = {
#                 "amount": amount_paise,
#                 "currency": "INR",
#                 "payment_capture": 1
#             }

#             # Razorpay Order Creation
#             for _ in range(3):
#                 try:
#                     order_response = client.order.create(order_data)
#                     print("Order Created:", order_response)
#                     break
#                 except razorpay.errors.BadRequestError as e:
#                     print("BadRequestError:", e.status_code, e.args)
#                     return JsonResponse({"error": "Razorpay BadRequestError", "detail": str(e.args)})
#                 except razorpay.errors.HttpError as e:
#                     print("HttpError:", e.status_code, e.args)
#                     return JsonResponse({"error": "Razorpay HttpError", "detail": str(e.args)})
#             else:
#                 return JsonResponse({"error": "Failed to create order after retries."})

#             # return order data to frontend
#             return JsonResponse({
#                 "order_id": order_response['id'],
#                 "key": settings.RAZORPAY_KEY_ID,
#                 "amount": amount_paise
#             })

#         except Exception as e:
#             print("General Exception:", str(e))
#             return JsonResponse({"error": str(e)})

from decimal import Decimal
from orders.models import Payment  # if not already imported

def create_order(request):
    if request.method == 'POST':
        try:
            amount_rupees = Decimal(request.POST['amount'])
            amount_paise = int(amount_rupees * 100)
            print("Amount (paise):", amount_paise)

            if amount_paise <= 0:
                return JsonResponse({"error": "Invalid amount."})

            order_data = {
                "amount": amount_paise,
                "currency": "INR",
                "payment_capture": 1
            }

            # Razorpay Order Creation
            for _ in range(3):
                try:
                    order_response = client.order.create(order_data)
                    print("Order Created:", order_response)
                    break
                except razorpay.errors.BadRequestError as e:
                    return JsonResponse({"error": "Razorpay BadRequestError", "detail": str(e.args)})
                except razorpay.errors.HttpError as e:
                    return JsonResponse({"error": "Razorpay HttpError", "detail": str(e.args)})
            else:
                return JsonResponse({"error": "Failed to create order after retries."})

            # ✅ Save the Payment record here
            Payment.objects.create(
                user=request.user,
                amount=amount_rupees,
                payment_method='Razorpay',
                status='Pending',
                is_paid=False,
                transaction_id=order_response['id']  # <-- critical!
            )

            return JsonResponse({
                "order_id": order_response['id'],
                "key": settings.RAZORPAY_KEY_ID,
                "amount": amount_paise
            })

        except Exception as e:
            print("General Exception:", str(e))
            return JsonResponse({"error": str(e)})



def verify_payment(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("Received Data:", data)

            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            if not (razorpay_order_id and razorpay_payment_id and razorpay_signature):
                return JsonResponse({"error": "Missing required payment details."})

            # Prepare params for signature verification
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            # Verify payment signature
            try:
                client.utility.verify_payment_signature(params_dict)
                print("Payment verification successful.")

                # Update Payment
                payment = Payment.objects.get(transaction_id=razorpay_order_id)
                payment.status = 'Success'
                payment.is_paid = True
                payment.save()

                # Update related Order
                # order = payment.order
                # order.is_ordered = True
                # order.status = 'Accepted'
                # order.save()

                return JsonResponse({"success": True, "message": "Payment verified successfully!"})

            except razorpay.errors.SignatureVerificationError:
                print("Signature verification failed.")
                return JsonResponse({"error": "Invalid payment signature."})

        except Exception as e:
            print("Exception in verify_payment:", str(e))
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})

def payment_success(request):
    return render(request, 'orders/success.html')