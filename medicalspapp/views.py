from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings


def index(request):
    return render(request, 'index.html')


@require_POST
def contact_enquiry(request):
    name        = request.POST.get('name', '').strip()
    email       = request.POST.get('email', '').strip()
    phone       = request.POST.get('phone', '').strip()
    role        = request.POST.get('role', '').strip()       # Buyer / Supplier
    subject_in  = request.POST.get('subject', '').strip()
    message_in  = request.POST.get('message', '').strip()

    if not all([name, email, role, message_in]):
        return JsonResponse({'status': 'error', 'msg': 'Please fill all required fields.'}, status=400)

    subject = f"[MSP Enquiry – {role}] {subject_in or 'New Enquiry'} from {name}"
    body = (
        f"Name    : {name}\n"
        f"Email   : {email}\n"
        f"Phone   : {phone or '—'}\n"
        f"Role    : {role}\n\n"
        f"Message :\n{message_in}"
    )

    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_HOST_USER])
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)

