from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return self.short_code
