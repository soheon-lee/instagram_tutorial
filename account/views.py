import json

from .models import Account
from django.views import View
from django.http import HttpResponse, JsonResponse

# SIGN-UP
class AccountView(View): # inherit
    def post(self, request):
        data = json.loads(request.body)
        Account(
                name = data['name'],
                email = data['email'],
                password = data['password']
        ).save()

        return HttpResponse(status=200)

    def get(self, request):
        account_data = Account.objects.values()
        return JsonResponse({'accounts':list(account_data)}, status=200)

# LOGIN
class Login(View):
    def post(self, request):
        login_info      = json.loads(request.body)
        login_email     = login_info['email']
        login_password  = login_info['password']

        try:
            user_enrolled_account = Account.objects.get(email=login_email)
            if login_password == user_enrolled_account.password:
                return JsonResponse({'message':"OK"}, status=200)
            else:
                return JsonResponse({'message':"Login Failed"}, status=401)
        except:
            return JsonResponse({'message':"Login Failed"}, status=401)
