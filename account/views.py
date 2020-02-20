import json
import jwt
import bcrypt

from django.views   import View
from django.http    import HttpResponse, JsonResponse

from .models        import Account
from instagram.settings      import SECRET_KEY

# SIGN-UP
class AccountView(View): # inherit
    def post(self, request):
        user_info = json.loads(request.body)

        if Account.objects.filter(email=user_info['email']).exists():
            return HttpResponse(status=409)

        Account(
                name = user_info['name'],
                email = user_info['email'],
                password = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
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

                if bcrypt.checkpw(user_info['password'].encode('utf-8'), selected_user.password.encode('utf-8')):
                    token = jwt.encode({'email': selected_user.email}, SECRET_KEY, algorithm='HS256').decode('utf-8')
                    return JsonResponse({"token":token}, status=200)
                
                return HttpResponse(status=401)
            
            return HttpResponse(status=400)

        except KeyError:
            return HttpResponse('INVALID_KEY',status=400)

# TOKEN-CHECK from JMLEE
class TokenCheckView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_token_info = jwt.decode(data['token'], 'secretkey-soheon', algorithm='HS256')

        if Account.objects.filter(email=user_token_info['email']).exists():
            return HttpResponse(status=200)
        return HttpResponse(status=403)

#================================================
#=========          DECORATOR         ===========
#================================================

class MyInfoView(View):
    def is_signed_in_user(func):
        def wrapper(*args, **kwargs):
            data = json.loads(request.body)
            user_token_info = jwt.decode(data['token'], 'secretkey-soheon', algorithm='HS256')
            if Account.objects.filter(email=user_token_info['email']).exists():
                return func
            return False
        return wrapper

    @is_signed_in_user
    def post(self, request):
        data = json.loads(request.body)
        selected_user =  Account.objects.get(email=data['email'])
        return JsonResponse({"me":selected_user}, status=200)


