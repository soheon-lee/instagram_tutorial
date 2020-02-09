import json

from .models    import Account

from django.views   import View
from django.http    import HttpResponse, JsonResponse

#SIGN-UP
class AccountView(View):
    def post(self, request):
        user_info = json.loads(request.body)

        if Account.objects.filter(email=user_info['email']).exists():
            return HttpResponse(status=409)

        Account(
                name = user_info['name'],
                email = user_info['email'],
                password = user_info['password']
        ).save()
        
        return HttpResponse(status=200)

    def get(self, request):
        return JsonResponse({'Customers':list(Account.objects.values())}, status=200)

#SIGN-IN
class SigninView(View):
    def post(self, request):
        unknown_user = json.loads(request.body)

        try:
            if Account.objects.filter(email=unknown_user['email']).exists():
                user = Account.objects.get(email=unknown_user['email'])
    
                if user.password == unknown_user['password']:
                    return HttpResponse(status=200)

                return HttpResponse(status=401)
    
            return HttpResponse(status=400)

        except KeyError:
            return HttpResponse(f'INVALID_KEYS', status=400)
