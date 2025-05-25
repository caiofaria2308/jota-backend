"""
Testes para os serializers de notícias
"""

import pytest
from rest_framework.test import APIRequestFactory

from apps.news.models import New
from apps.account.models import SubscriptionPlan
from apps.news.api.serializes import NewSerializer


@pytest.mark.django_db
class TestNewSerializer:
    """Testes para o NewSerializer"""

    def test_serialize_news(self, published_news):
        """Testa a serialização de uma notícia"""
        serializer = NewSerializer(published_news)
        data = serializer.data

        assert data["title"] == published_news.title
        assert data["subtitle"] == published_news.subtitle
        assert data["content"] == published_news.content
        assert data["status"] == published_news.status
        assert data["is_exclusive"] == published_news.is_exclusive
        assert data["author"] == str(published_news.author.id)

    def test_deserialize_valid_data_writer(self, user_writer, sample_image):
        """Testa a deserialização com dados válidos para writer"""
        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user_writer

        data = {
            "title": "Nova Notícia",
            "subtitle": "Subtítulo da notícia",
            "content": "Conteúdo da notícia",
            "picture": sample_image,
            "status": New.DRAFT,
            "is_exclusive": False,
            "verticals": [SubscriptionPlan.POWER],
        }

        serializer = NewSerializer(data=data, context={"request": request})

        assert serializer.is_valid()
        news = serializer.save()
        assert news.title == "Nova Notícia"
        assert news.author == user_writer

    def test_deserialize_invalid_user_type(self, user_reader, sample_image):
        """Testa a deserialização com usuário reader - deve falhar"""
        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user_reader

        data = {
            "title": "Tentativa de Criação",
            "subtitle": "Subtítulo",
            "content": "Conteúdo",
            "picture": sample_image,
            "status": New.DRAFT,
        }

        serializer = NewSerializer(data=data, context={"request": request})

        assert not serializer.is_valid()
        assert "Você não tem permissão para criar/editar notícias" in str(
            serializer.errors
        )

    def test_update_own_news(self, user_writer, draft_news):
        """Testa atualização da própria notícia"""
        factory = APIRequestFactory()
        request = factory.patch("/")
        request.user = user_writer

        data = {"title": "Título Atualizado", "status": New.PUBLISHED}

        serializer = NewSerializer(
            instance=draft_news, data=data, partial=True, context={"request": request}
        )

        assert serializer.is_valid()
        updated_news = serializer.save()
        assert updated_news.title == "Título Atualizado"
        assert updated_news.status == New.PUBLISHED

    def test_update_other_user_news(self, user_writer, published_news):
        """Testa tentativa de atualizar notícia de outro usuário"""
        # Criar outro writer
        other_writer = user_writer.__class__.objects.create_user(
            username="other_writer",
            email="other@test.com",
            password="test123",
            user_type=user_writer.__class__.WRITER,
        )

        factory = APIRequestFactory()
        request = factory.patch("/")
        request.user = other_writer

        data = {"title": "Tentativa de Hack"}

        serializer = NewSerializer(
            instance=published_news,
            data=data,
            partial=True,
            context={"request": request},
        )

        assert not serializer.is_valid()
        assert "Você não tem permissão para editar essa notícia" in str(
            serializer.errors
        )

    def test_create_sets_author_automatically(self, user_writer, sample_image):
        """Testa que o autor é setado automaticamente na criação"""
        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user_writer

        data = {
            "title": "Notícia Automática",
            "subtitle": "Subtítulo",
            "content": "Conteúdo",
            "picture": sample_image,
            "status": New.DRAFT,
            # Note: não passamos author nos dados
        }

        serializer = NewSerializer(data=data, context={"request": request})

        assert serializer.is_valid()
        news = serializer.save()
        assert news.author == user_writer

    def test_serialize_multiple_news(self, published_news, draft_news):
        """Testa serialização de múltiplas notícias"""
        news_list = [published_news, draft_news]
        serializer = NewSerializer(news_list, many=True)
        data = serializer.data

        assert len(data) == 2
        assert data[0]["title"] == published_news.title
        assert data[1]["title"] == draft_news.title

    def test_required_fields_validation(self, user_writer):
        """Testa validação de campos obrigatórios"""
        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user_writer

        # Dados incompletos
        data = {
            "title": "Título Apenas"
            # Faltam campos obrigatórios
        }

        serializer = NewSerializer(data=data, context={"request": request})

        assert not serializer.is_valid()
        # Verifica se há erros nos campos obrigatórios
        assert "subtitle" in serializer.errors or len(serializer.errors) > 0

    def test_verticals_field(self, user_writer, sample_image):
        """Testa o campo verticals"""
        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user_writer

        verticals = [
            SubscriptionPlan.POWER,
            SubscriptionPlan.TAX,
            SubscriptionPlan.HEALTH,
        ]

        data = {
            "title": "Notícia com Verticais",
            "subtitle": "Subtítulo",
            "content": "Conteúdo",
            "picture": sample_image,
            "status": New.DRAFT,
            "verticals": verticals,
        }

        serializer = NewSerializer(data=data, context={"request": request})

        assert serializer.is_valid()
        news = serializer.save()
        assert len(news.verticals) == 3
        for vertical in verticals:
            assert vertical in news.verticals
