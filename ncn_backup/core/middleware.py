from django.shortcuts import render


class Friendly404Middleware:
    """
    Django skips handler404 when DEBUG=True and shows the technical 404 page.
    Replace any 404 HTML response with our branded template (dev and production).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code != 404:
            return response

        accept = request.headers.get("Accept", "")
        if "application/json" in accept and "text/html" not in accept:
            return response

        return render(request, "404.html", status=404)
