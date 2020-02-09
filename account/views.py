import json

from .models        import Account

from django.views   import View
from django.http    import HttpResponse, JsonResponse

# SIGN-UP
class AccountView(View): # inherit
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
        account_data = Account.objects.values()
        return JsonResponse({'accounts':list(account_data)}, status=200)

# SIGN-IN
class SigninView(View):
    def post(self, request):
        user_info = json.loads(request.body)

        try:
            if Account.objects.filter(email=user_info['email']).exists():
                selected_user = Account.objects.get(email=user_info['email'])
                if selected_user.password == user_info['password']:
                    return HttpResponse(status=200)
                
                return HttpResponse(status=401)
            
            return HttpResponse(status=400)

        except KeyError as e:
            return HttpResponse(f'INVALID_KEYSSSSSSSS',status=400)
