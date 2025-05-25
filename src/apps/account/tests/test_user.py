"""
Testes para o modelo User
"""

import pytest
from safedelete import models as models_safedelete
from django.contrib.auth import get_user_model

from apps.account.models import SubscriptionPlan

User = get_user_model()


@pytest.mark.django_db
class TestUser:
    """Testes para o modelo User"""

    def test_create_user_reader(self):
        """Testa a criação de um usuário do tipo Reader"""
        user = User.objects.create_user(
            username="reader_test",
            email="reader@test.com",
            password="testpass123",
            user_type=User.READER,
        )

        assert user.username == "reader_test"
        assert user.email == "reader@test.com"
        assert user.user_type == User.READER
        assert user.subscription_plan is None
        assert user.check_password("testpass123")

    def test_create_user_writer(self):
        """Testa a criação de um usuário do tipo Writer"""
        user = User.objects.create_user(
            username="writer_test",
            email="writer@test.com",
            password="testpass123",
            user_type=User.WRITER,
        )

        assert user.username == "writer_test"
        assert user.email == "writer@test.com"
        assert user.user_type == User.WRITER
        assert user.subscription_plan is None

    def test_user_default_type(self):
        """Testa que o tipo padrão do usuário é Reader"""
        user = User.objects.create_user(
            username="default_user", email="default@test.com", password="testpass123"
        )

        assert user.user_type == User.READER

    def test_user_str_representation(self):
        """Testa a representação string do usuário"""
        user = User.objects.create_user(
            username="test_user", email="test@example.com", password="testpass123"
        )

        assert str(user) == "test@example.com"

    def test_user_with_subscription_plan(self):
        """Testa usuário com plano de assinatura"""
        plan = SubscriptionPlan.objects.create(
            name="Plano Premium", price=199.99, is_exclusive=True
        )

        user = User.objects.create_user(
            username="premium_user",
            email="premium@test.com",
            password="testpass123",
            subscription_plan=plan,
        )

        assert user.subscription_plan == plan
        assert user.subscription_plan.name == "Plano Premium"

    def test_user_type_choices(self):
        """Testa as opções de tipo de usuário"""
        user_writer = User.objects.create_user(
            username="writer",
            email="writer@test.com",
            password="test123",
            user_type=User.WRITER,
        )

        user_reader = User.objects.create_user(
            username="reader",
            email="reader@test.com",
            password="test123",
            user_type=User.READER,
        )

        assert user_writer.user_type == User.WRITER
        assert user_reader.user_type == User.READER

    def test_subscription_plan_relationship(self):
        """Testa o relacionamento com plano de assinatura"""
        plan = SubscriptionPlan.objects.create(name="Plano Básico", price=99.99)

        user1 = User.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="test123",
            subscription_plan=plan,
        )

        user2 = User.objects.create_user(
            username="user2",
            email="user2@test.com",
            password="test123",
            subscription_plan=plan,
        )

        # Testa o relacionamento reverso
        assert user1 in plan.users.all()
        assert user2 in plan.users.all()
        assert plan.users.count() == 2

    def test_user_without_subscription_plan(self):
        """Testa usuário sem plano de assinatura"""
        user = User.objects.create_user(
            username="free_user", email="free@test.com", password="testpass123"
        )

        assert user.subscription_plan is None

    def test_user_subscription_plan_on_delete(self):
        """Testa comportamento quando plano é deletado"""
        plan = SubscriptionPlan.objects.create(name="Plano Temporário", price=50.00)

        user = User.objects.create_user(
            username="temp_user",
            email="temp@test.com",
            password="test123",
            subscription_plan=plan,
        )

        # Deleta o plano usando hard delete para forçar o SET_NULL
        plan.delete(force_policy=models_safedelete.HARD_DELETE)
        user.refresh_from_db()

        # Verifica que o usuário ainda existe mas sem plano (SET_NULL behavior)
        assert user.subscription_plan is None
