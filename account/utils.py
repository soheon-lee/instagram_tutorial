import jwt 
import json
import requests

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from instagram.settings import SECRET_KEY
from account.models     import Account

def login_required(func):

   def wrapper(self, request, *args, **kwargs):
       access_token = request.headers.get('Authorization', None)
       if access_token:
           try:
               decode = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
               user_id = decode.get('email', None)
               user = Account.objects.get(email=user_id)
               request.user = user

           except jwt.DecodeError:
               return JsonResponse({"message" : "🤮 잘못된 토큰 입니다."}, status = 403)
           except Account.DoesNotExist:
               return JsonResponse({"message" : "😜 존재하지 않는 아이디 입니다."}, status=401)
         
           return func(self, request, *args, **kwargs)

       return JsonResponse({"message" : "😫 로그인이 필요한 서비스 입니다."}, status=401)

   return wrapper
