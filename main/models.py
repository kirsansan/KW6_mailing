from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Mailing(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    text = models.TextField(verbose_name='описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания', **NULLABLE)
    # used_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания', **NULLABLE)

    def __str__(self):
        return f"{self.title}, {self.text[:100]}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('title',)
