from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Post(models.Model):
    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    title = models.CharField(max_length=64, verbose_name="عنوان")
    image = models.ImageField(upload_to="news-images/", verbose_name="عکس")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید ها")
    promote = models.BooleanField(default=False, verbose_name="افزودن به اسلایدر")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")
    text = RichTextField(verbose_name="متن")


class Comment(models.Model):
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    post = models.ForeignKey("Post", on_delete=models.CASCADE, verbose_name="پست", null=True)
    parent = models.ForeignKey("Comment", null=True, blank=True, related_name="replies", on_delete=models.CASCADE,
                               verbose_name="پاسخ")
    is_valid = models.BooleanField(default=False, verbose_name="معتبر")
    text = models.TextField(verbose_name="متن")
