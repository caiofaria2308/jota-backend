import uuid

from django.db import models
from safedelete import models as models_safedelete
from author.decorators import with_author
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


@with_author
class SubscriptionPlan(models_safedelete.SafeDeleteModel):
    """
    Model representing a subscription plan.
    """

    _safedelete_policy = models_safedelete.NO_DELETE
    POWER = "power"
    TAX = "tax"
    HEALTH = "health"
    ENERGY = "energy"
    LABOR = "labor"
    VERTICAL_CHOICES = (
        (POWER, _("Poder")),
        (TAX, _("Imposto")),
        (HEALTH, _("Saúde")),
        (ENERGY, _("Energia")),
        (LABOR, _("Trabalhista")),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_exclusive = models.BooleanField(
        default=False, verbose_name=_("Acesso exclusivo ?")
    )
    verticals = ArrayField(
        models.CharField(max_length=50, choices=VERTICAL_CHOICES),
        blank=True,
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Plano de Assinatura")
        verbose_name_plural = _("Planos de Assinatura")
        ordering = ["name"]

    def __str__(self):
        return self.name


@with_author
class User(AbstractUser):
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        related_name="users",
    )

    def __str__(self):
        return self.email
