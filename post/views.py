import json

from .models    import Comment

from django.views   import View
from django.http    import HttpResponse, JsonResponse

#SIGN-UP
class CommentView(View):
    def post(self, request):
        comment_info = json.loads(request.body)

        Comment(
                name = comment_info['name'],
                content = comment_info['content']
        ).save()
        
        return HttpResponse(status=200)

    def get(self, request):
        return JsonResponse({'Comments':list(Comment.objects.values())}, status=200)
