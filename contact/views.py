import resend
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Contact

@api_view(['POST'])
def contact_api(request):
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')

    if not all([name, email, message]):
        return Response({"error": "All fields are required"}, status=400)

    # Save to database
    try:
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
    except Exception as e:
        print(f"Database save failed: {e}")
        return Response({"error": "Failed to save message"}, status=500)

    resend.api_key = settings.RESEND_API_KEY

    # Email to ADMIN
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": settings.ADMIN_EMAIL,
            "subject": f"New Contact Form Submission from {name}",
            "html": f"""
                <h2>New Contact Form Submission</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong></p>
                <p>{message}</p>
            """
        })
    except Exception as e:
        print(f"Admin email failed: {e}")
        return Response({"error": str(e)}, status=500)

    # Email to USER
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": "We received your message - GenLab",
            "html": f"""
                <h2>Hi {name}, thanks for reaching out!</h2>
                <p>We've received your message and will get back to you shortly.</p>
                <hr/>
                <p><strong>Your message:</strong></p>
                <p>{message}</p>
                <br/>
                <p>Best regards,</p>
                <p><strong>GenLab Team</strong></p>
            """
        })
    except Exception as e:
        print(f"User email failed: {e}")

    return Response({"message": "Message sent successfully!"}, status=200)