from django.db import models
from account.models import Account

class Comment(models.Model):
    account     = models.ForeignKey(Account, on_delete = models.CASCADE)
    content     = models.CharField(max_length = 500)
    created_at  = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.account.name

