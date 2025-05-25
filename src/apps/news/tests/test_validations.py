"""
Testes para validações e casos extremos
"""

import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from apps.news.models import New
from apps.account.models import User, SubscriptionPlan


@pytest.mark.django_db
class TestValidations:
    """Testes para validações e casos extremos"""

    def test_news_title_max_length(self, user_writer, sample_image):
        """Testa limite máximo do título"""
        long_title = "x" * 300  # Maior que 255 caracteres

        with pytest.raises(ValidationError):
            news = New(
                title=long_title,
                subtitle="Subtítulo",
                content="Conteúdo",
                picture=sample_image,
                author=user_writer,
            )
            news.full_clean()

    def test_news_subtitle_max_length(self, user_writer, sample_image):
        """Testa limite máximo do subtítulo"""
        long_subtitle = "x" * 600  # Maior que 500 caracteres

        with pytest.raises(ValidationError):
            news = New(
                title="Título",
                subtitle=long_subtitle,
                content="Conteúdo",
                picture=sample_image,
                author=user_writer,
            )
            news.full_clean()

    def test_news_without_author(self, sample_image):
        """Testa criação de notícia sem autor - deve falhar"""
        with pytest.raises(IntegrityError):
            New.objects.create(
                title="Notícia Sem Autor",
                subtitle="Subtítulo",
                content="Conteúdo",
                picture=sample_image,
                # author não fornecido
            )

    def test_news_invalid_status(self, user_writer, sample_image):
        """Testa status inválido"""
        with pytest.raises(ValidationError):
            news = New(
                title="Título",
                subtitle="Subtítulo",
                content="Conteúdo",
                picture=sample_image,
                author=user_writer,
                status="invalid_status",
            )
            news.full_clean()

    def test_news_invalid_vertical(self, user_writer, sample_image):
        """Testa vertical inválida"""
        with pytest.raises(ValidationError):
            news = New(
                title="Título",
                subtitle="Subtítulo",
                content="Conteúdo",
                picture=sample_image,
                author=user_writer,
                verticals=["invalid_vertical"],
            )
            news.full_clean()

    def test_subscription_plan_negative_price(self):
        """Testa preço negativo em plano de assinatura"""
        with pytest.raises(ValidationError):
            plan = SubscriptionPlan(name="Plano Inválido", price=-99.99)
            plan.full_clean()

    def test_subscription_plan_empty_name(self):
        """Testa plano sem nome"""
        with pytest.raises(ValidationError):
            plan = SubscriptionPlan(name="", price=99.99)  # Nome vazio
            plan.full_clean()

    def test_user_invalid_type(self):
        """Testa tipo de usuário inválido"""
        with pytest.raises(ValidationError):
            user = User(
                username="test_user", email="test@example.com", user_type="invalid_type"
            )
            user.full_clean()

    def test_news_empty_content(self, user_writer, sample_image):
        """Testa notícia com conteúdo vazio"""
        # Dependendo das regras de negócio, pode ser válido ou não
        news = New.objects.create(
            title="Título",
            subtitle="Subtítulo",
            content="",  # Conteúdo vazio
            picture=sample_image,
            author=user_writer,
        )
        assert news.content == ""

    def test_news_very_long_content(self, user_writer, sample_image):
        """Testa notícia com conteúdo muito longo"""
        very_long_content = "x" * 100000  # 100k caracteres

        news = New.objects.create(
            title="Título",
            subtitle="Subtítulo",
            content=very_long_content,
            picture=sample_image,
            author=user_writer,
        )
        assert len(news.content) == 100000

    def test_news_special_characters(self, user_writer, sample_image):
        """Testa notícia com caracteres especiais"""
        special_title = "Título com émojis 🚀 e acentos ção"
        special_content = "Conteúdo com símbolos: @#$%^&*()_+ e unicode: 中文"

        news = New.objects.create(
            title=special_title,
            subtitle="Subtítulo especial",
            content=special_content,
            picture=sample_image,
            author=user_writer,
        )

        assert news.title == special_title
        assert news.content == special_content

    def test_subscription_plan_duplicate_name(self):
        """Testa criação de planos com nomes duplicados"""
        SubscriptionPlan.objects.create(name="Plano Único", price=99.99)

        # Criar outro com mesmo nome - deve ser permitido
        # (não há constraint de unicidade no modelo)
        plan2 = SubscriptionPlan.objects.create(name="Plano Único", price=149.99)
        assert plan2.name == "Plano Único"

    def test_news_all_verticals(self, user_writer, sample_image):
        """Testa notícia com todas as verticais possíveis"""
        all_verticals = [
            SubscriptionPlan.POWER,
            SubscriptionPlan.TAX,
            SubscriptionPlan.HEALTH,
            SubscriptionPlan.ENERGY,
            SubscriptionPlan.LABOR,
        ]

        news = New.objects.create(
            title="Notícia Completa",
            subtitle="Com todas as verticais",
            content="Conteúdo completo",
            picture=sample_image,
            author=user_writer,
            verticals=all_verticals,
        )

        assert len(news.verticals) == 5
        for vertical in all_verticals:
            assert vertical in news.verticals

    def test_news_duplicate_verticals(self, user_writer, sample_image):
        """Testa notícia com verticais duplicadas"""
        duplicate_verticals = [
            SubscriptionPlan.POWER,
            SubscriptionPlan.POWER,  # Duplicada
            SubscriptionPlan.TAX,
        ]

        news = New.objects.create(
            title="Notícia com Duplicatas",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
            verticals=duplicate_verticals,
        )

        # PostgreSQL ArrayField pode manter duplicatas
        assert len(news.verticals) == 3

    def test_user_without_username(self):
        """Testa usuário sem username"""
        with pytest.raises(ValidationError):
            user = User(username="", email="test@example.com")  # Username vazio
            user.full_clean()

    def test_user_invalid_email_format(self):
        """Testa usuário com email inválido"""
        with pytest.raises(ValidationError):
            user = User(
                username="test_user", email="email_invalido"  # Formato inválido
            )
            user.full_clean()

    def test_news_published_without_published_at(self, user_writer, sample_image):
        """Testa notícia publicada sem data de publicação"""
        news = New.objects.create(
            title="Notícia Publicada",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
            status=New.PUBLISHED,
            # published_at não definido
        )

        # Pode ser válido dependendo da lógica de negócio
        assert news.status == New.PUBLISHED
        assert news.published_at is None
