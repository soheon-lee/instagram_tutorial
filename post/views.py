import json

from .models        import Comment

from django.views   import View
from django.http    import HttpResponse, JsonResponse

# COMMENT
class CommentView(View):
    def post(self, request):
        input_comment   = json.loads(request.body)
        Comment(
            name    = input_comment['name'],
            content = input_comment['content']
        ).save()

        return HttpResponse(status=200)

    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'comments':list(comment_data)}, status=200)
