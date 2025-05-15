class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.session.get('token')
        if token:
            request.headers = {
                'Authorization': f'Bearer {token}',
            }
        response = self.get_response(request)
        return response
