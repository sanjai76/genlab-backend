from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Contact
from django.core.mail import send_mail


@api_view(['POST'])
def contact_api(request):

    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")

    # ⭐ Save to database
    Contact.objects.create(
        name=name,
        email=email,
        message=message
    )

    # ⭐ Email to USER (confirmation)
    send_mail(
        subject="GenLab Contact Confirmation",
        message="Hi {},\n\nThank you for contacting GenLab. Our team will reach you soon.".format(name),
        from_email="yourgmail@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )

    # ⭐ Email to ADMIN (lead notification)
    admin_message = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Message: {message}
"""

    send_mail(
        subject="🚨 New GenLab Contact Lead",
        message=admin_message,
        from_email="yourgmail@gmail.com",
        recipient_list=["sanjaimsd141@gmail.com"],
        fail_silently=False,
    )

    return Response({"status": "saved"})