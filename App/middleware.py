from django.http import HttpResponseForbidden
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_superuser:
                # نمایش پیام خطا
                return HttpResponseForbidden("<h1>Access Denied</h1>")
        response = self.get_response(request)
        return response
