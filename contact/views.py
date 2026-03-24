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

    # ⭐ Email to USER (safe sending)
    try:
        send_mail(
            subject="GenLab Contact Confirmation",
            message=f"Hi {name},\n\nThank you for contacting GenLab. Our team will reach you soon.",
            from_email="sanjaimsd141@gmail.com",
            recipient_list=[email],
            fail_silently=True,
        )
    except Exception as e:
        print("User mail error:", e)

    # ⭐ Email to ADMIN (safe sending)
    admin_message = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Message: {message}
"""

    try:
        send_mail(
            subject="🚨 New GenLab Contact Lead",
            message=admin_message,
            from_email="sanjaimsd141@gmail.com",
            recipient_list=["sanjaimsd141@gmail.com"],
            fail_silently=True,
        )
    except Exception as e:
        print("Admin mail error:", e)

    return Response({"status": "saved"})