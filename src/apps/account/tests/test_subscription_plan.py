"""
Testes para o modelo SubscriptionPlan
"""

from decimal import Decimal

import pytest

from apps.account.models import SubscriptionPlan


@pytest.mark.django_db
class TestSubscriptionPlan:
    """Testes para o modelo SubscriptionPlan"""

    def test_create_subscription_plan(self):
        """Testa a criação de um plano de assinatura"""
        plan = SubscriptionPlan.objects.create(
            name="Plano Teste",
            price=Decimal("99.99"),
            is_exclusive=True,
            verticals=[SubscriptionPlan.POWER, SubscriptionPlan.TAX],
        )

        assert plan.name == "Plano Teste"
        assert plan.price == Decimal("99.99")
        assert plan.is_exclusive is True
        assert SubscriptionPlan.POWER in plan.verticals
        assert SubscriptionPlan.TAX in plan.verticals
        assert plan.id is not None

    def test_subscription_plan_str_representation(self):
        """Testa a representação string do plano de assinatura"""
        plan = SubscriptionPlan.objects.create(
            name="Plano Premium", price=Decimal("199.99")
        )

        assert str(plan) == "Plano Premium"

    def test_subscription_plan_ordering(self):
        """Testa a ordenação dos planos de assinatura"""
        plan_b = SubscriptionPlan.objects.create(
            name="Plano B", price=Decimal("150.00")
        )
        plan_a = SubscriptionPlan.objects.create(
            name="Plano A", price=Decimal("100.00")
        )

        plans = list(SubscriptionPlan.objects.all())
        assert plans[0] == plan_a  # Deve vir primeiro pela ordenação por nome
        assert plans[1] == plan_b

    def test_subscription_plan_default_values(self):
        """Testa os valores padrão do plano de assinatura"""
        plan = SubscriptionPlan.objects.create(
            name="Plano Básico", price=Decimal("50.00")
        )

        assert plan.is_exclusive is False
        assert plan.verticals == []
        assert plan.created_at is not None
        assert plan.updated_at is not None

    def test_subscription_plan_vertical_choices(self):
        """Testa as opções de verticais disponíveis"""
        expected_choices = [
            SubscriptionPlan.POWER,
            SubscriptionPlan.TAX,
            SubscriptionPlan.HEALTH,
            SubscriptionPlan.ENERGY,
            SubscriptionPlan.LABOR,
        ]

        plan = SubscriptionPlan.objects.create(
            name="Plano Completo", price=Decimal("299.99"), verticals=expected_choices
        )

        for choice in expected_choices:
            assert choice in plan.verticals

    def test_subscription_plan_meta_attributes(self):
        """Testa os atributos meta do modelo"""
        meta = SubscriptionPlan._meta
        assert str(meta.verbose_name) == "Plano de Assinatura"
        assert str(meta.verbose_name_plural) == "Planos de Assinatura"
        assert meta.ordering == ["name"]
