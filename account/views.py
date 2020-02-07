import json

from .models import Account, Comment
from django.views import View
from django.http import HttpResponse, JsonResponse

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
            login_account = Account.objects.get(email=login_email)
            if login_password == login_account.password:
                return JsonResponse({'message':"OK"}, status=200)
            else:
                return JsonResponse({'message':"Login Failed"}, status=401)
        except:
            return JsonResponse({'message':"Login Failed"}, status=401)

# COMMENT            
class CommentView(View):
    def post(self, request):
        input_comment   = json.loads(request.body)
        Comment(
            name        = input_comment['name'],
            email       = input_comment['email'],
            content     = input_comment['content']
        ).save()

        return HttpResponse(status=200)

    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'comments':list(comment_data)}, status=200)


# LOGIN ===== METHOD 1 ===== : previous version
class Login1(View):
    def post(self, request):
        login_info      = json.loads(request.body)
        login_email     = login_info['email']
        login_password  = login_info['password']

        print("======LOG-IN INFO======")
        print("LOGIN-EMAIL:",login_email)
        print("LOGIN-PASSWORD:",login_password)
        print("==========END==========")

        login_account = Account.objects.filter(email=login_email)
        isCustomer  = (len(login_account) != 0)
    
        if isCustomer:
            if login_password == login_account[0].password:
                print("OK")
                message = "Logged in"
                return JsonResponse({'message':message}, status=200)
            else:
                print("WRONG PASSWORD")
                message = "Login fail: WRONG PASSWORD"
                return JsonResponse({'message':message}, status=200)
        else:
            print("Please sign-up first")
            message = "Login fail: Please sign-up first"
            return JsonResponse({'message':message}, status=200)
