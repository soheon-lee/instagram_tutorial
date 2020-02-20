import json

from .models        import Comment
from account.utils          import login_required

from django.views   import View
from django.http    import HttpResponse, JsonResponse

# COMMENT
class CommentView(View):

    @login_required
    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'comments':list(comment_data)}, status=200)
    
    @login_required
    def post(self, request):
        input_comment   = json.loads(request.body)
        Comment(
            name    = input_comment['name'],
            content = input_comment['content']
        ).save()

        return HttpResponse(status=200)
