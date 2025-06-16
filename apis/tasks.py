from celery import shared_task
from decouple import config
@shared_task()
def send_email_task(user_email, order_id):
    from django.core.mail import send_mail
    subject = 'Order Confirmation'
    message = f'Your order with ID {order_id} has been confirmed.'
    from_email = config('EMAIL_HOST_USER')
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
