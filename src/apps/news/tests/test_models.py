"""
Testes para o modelo New
"""

import pytest

from apps.news.models import New
from apps.account.models import SubscriptionPlan


@pytest.mark.django_db
class TestNew:
    """Testes para o modelo New"""

    def test_create_news_draft(self, user_writer, sample_image):
        """Testa a criação de uma notícia em rascunho"""
        news = New.objects.create(
            title="Notícia de Teste",
            subtitle="Subtítulo da notícia",
            content="Conteúdo da notícia de teste",
            picture=sample_image,
            author=user_writer,
            status=New.DRAFT,
            is_exclusive=False,
            verticals=[SubscriptionPlan.POWER],
        )

        assert news.title == "Notícia de Teste"
        assert news.subtitle == "Subtítulo da notícia"
        assert news.content == "Conteúdo da notícia de teste"
        assert news.author == user_writer
        assert news.status == New.DRAFT
        assert news.is_exclusive is False
        assert SubscriptionPlan.POWER in news.verticals
        assert news.id is not None

    def test_create_news_published(self, user_writer, sample_image):
        """Testa a criação de uma notícia publicada"""
        news = New.objects.create(
            title="Notícia Publicada",
            subtitle="Subtítulo da notícia publicada",
            content="Conteúdo da notícia publicada",
            picture=sample_image,
            author=user_writer,
            status=New.PUBLISHED,
            is_exclusive=True,
            verticals=[SubscriptionPlan.POWER, SubscriptionPlan.TAX],
        )

        assert news.status == New.PUBLISHED
        assert news.is_exclusive is True
        assert len(news.verticals) == 2

    def test_news_str_representation(self, user_writer, sample_image):
        """Testa a representação string da notícia"""
        news = New.objects.create(
            title="Título da Notícia",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
        )

        assert str(news) == "Título da Notícia"

    def test_news_default_status(self, user_writer, sample_image):
        """Testa que o status padrão é DRAFT"""
        news = New.objects.create(
            title="Notícia Padrão",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
        )

        assert news.status == New.DRAFT

    def test_news_default_is_exclusive(self, user_writer, sample_image):
        """Testa que o padrão é not exclusive"""
        news = New.objects.create(
            title="Notícia Pública",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
        )

        assert news.is_exclusive is False

    def test_news_default_verticals(self, user_writer, sample_image):
        """Testa que verticals padrão é lista vazia"""
        news = New.objects.create(
            title="Notícia Sem Vertical",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
        )

        assert news.verticals == []

    def test_news_with_multiple_verticals(self, user_writer, sample_image):
        """Testa notícia com múltiplas verticais"""
        all_verticals = [
            SubscriptionPlan.POWER,
            SubscriptionPlan.TAX,
            SubscriptionPlan.HEALTH,
            SubscriptionPlan.ENERGY,
            SubscriptionPlan.LABOR,
        ]

        news = New.objects.create(
            title="Notícia Completa",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
            verticals=all_verticals,
        )

        assert len(news.verticals) == 5
        for vertical in all_verticals:
            assert vertical in news.verticals

    def test_news_ordering(self, user_writer, sample_image):
        """Testa a ordenação das notícias por published_at"""
        from datetime import timedelta

        from django.utils import timezone

        now = timezone.now()

        news1 = New.objects.create(
            title="Notícia Antiga",
            subtitle="Sub1",
            content="Conteúdo1",
            picture=sample_image,
            author=user_writer,
            status=New.PUBLISHED,
            published_at=now - timedelta(hours=2),
        )

        news2 = New.objects.create(
            title="Notícia Recente",
            subtitle="Sub2",
            content="Conteúdo2",
            picture=sample_image,
            author=user_writer,
            status=New.PUBLISHED,
            published_at=now - timedelta(hours=1),
        )

        news_list = list(New.objects.all())
        # Ordenação decrescente por published_at
        assert news_list[0] == news2  # Mais recente primeiro
        assert news_list[1] == news1

    def test_news_meta_attributes(self):
        """Testa os atributos meta do modelo"""
        meta = New._meta
        assert str(meta.verbose_name) == "Notícia"
        assert str(meta.verbose_name_plural) == "Notícias"
        assert meta.ordering == ["-published_at"]

    def test_news_author_relationship(self, user_writer, user_reader, sample_image):
        """Testa o relacionamento com o autor"""
        news = New.objects.create(
            title="Notícia do Writer",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
        )

        assert news.author == user_writer
        assert news in user_writer.news.all()
        assert news not in user_reader.news.all()

    def test_news_safedelete_policy(self, user_writer, sample_image):
        """Testa a política de soft delete"""
        news = New.objects.create(
            title="Notícia para Deletar",
            subtitle="Subtítulo",
            content="Conteúdo",
            picture=sample_image,
            author=user_writer,
        )

        news_id = news.id
        news.delete()

        # Verifica que foi soft delete
        assert New.objects.filter(id=news_id).count() == 0
        assert New.all_objects.filter(id=news_id).count() == 1
