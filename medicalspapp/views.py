from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings


def index(request):
    return render(request, 'index.html')


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "\n"
        "Sitemap: https://www.medicalsupplyportal.com/sitemap.xml\n"
    )
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.medicalsupplyportal.com/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://www.medicalsupplyportal.com/supplier/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.medicalsupplyportal.com/products/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>"""
    return HttpResponse(content, content_type='application/xml')


@require_POST
def contact_enquiry(request):
    name        = request.POST.get('name', '').strip()
    email       = request.POST.get('email', '').strip()
    phone       = request.POST.get('phone', '').strip()
    subject_in  = request.POST.get('subject', '').strip()
    message_in  = request.POST.get('message', '').strip()

    if not all([name, email, message_in]):
        return JsonResponse({'status': 'error', 'msg': 'Please fill all required fields.'}, status=400)

    subject = f"[MSP Enquiry] {subject_in or 'New Enquiry'} from {name}"
    body = (
        f"Name    : {name}\n"
        f"Email   : {email}\n"
        f"Phone   : {phone or '—'}\n\n"
        f"Message :\n{message_in}"
    )

    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_HOST_USER])
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)

