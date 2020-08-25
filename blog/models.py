from django.db import models
from django.urls import reverse_lazy


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=False)
    udpated = models.DateTimeField(auto_now=True, editable=False, blank=False, null=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    body = models.TextField(blank=True, null=False)

    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])