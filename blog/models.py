from django.db import models

NULLABLE = {'null': True, 'blank': True}

class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='title')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    text = models.TextField(verbose_name='text')
    image = models.ImageField(upload_to='blogs_images/', verbose_name='preview', **NULLABLE)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='date created')
    is_published = models.BooleanField(default=True, verbose_name='was published')
    counter_view = models.IntegerField(default=0, verbose_name='counter of views')

    def __str__(self):
        return f"{self.title} was created {self.date_created}"

    class Meta:
        verbose_name='blog'
        verbose_name_plural='blogs'
        ordering = ('date_created', )
