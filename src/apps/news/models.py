import uuid

from django.db import models
from safedelete import models as models_safedelete
from django_q.tasks import schedule
from author.decorators import with_author
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from apps.account.models import SubscriptionPlan

User = get_user_model()


@with_author
class New(models_safedelete.SafeDeleteModel):
    """
    Model representing a news article.
    """

    PUBLISHED = "published"
    DRAFT = "draft"
    STATUS_CHOICES = (
        (PUBLISHED, _("Publicado")),
        (DRAFT, _("Rascunho")),
    )

    _safedelete_policy = models_safedelete.SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500)
    picture = models.ImageField(upload_to="news_pictures")
    content = models.TextField()
    is_exclusive = models.BooleanField(
        default=False, verbose_name=_("Acesso exclusivo ?")
    )
    published_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        User,
        verbose_name=_("Autor da noticia"),
        on_delete=models.PROTECT,
        related_name="news",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    verticals = ArrayField(
        models.CharField(max_length=50, choices=SubscriptionPlan.VERTICAL_CHOICES),
        blank=True,
        default=list,
    )

    class Meta:
        verbose_name = _("Notícia")
        verbose_name_plural = _("Notícias")
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        if self.status == self.DRAFT and self.published_at:
            # Schedule the task to send email alerts
            schedule(
                "apps.news.tasks.publish_news",
                news_id=str(self.id),
                schedule_type="O",
                next_run=self.published_at,
            )
        return obj
