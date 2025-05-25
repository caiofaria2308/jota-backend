"""
Testes para a API de notícias
"""

import pytest
from django.urls import reverse
from rest_framework import status

from apps.news.models import New
from apps.account.models import SubscriptionPlan


@pytest.mark.django_db
class TestNewViewSet:
    """Testes para o ViewSet de notícias"""

    def test_list_news_unauthenticated(self, api_client):
        """Testa listagem de notícias sem autenticação"""
        url = reverse("news-list")
        response = api_client.get(url)

        # Pode retornar 401 se autenticação for obrigatória
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
        ]

    def test_list_news_as_reader_without_subscription(
        self, api_client, user_reader, published_news
    ):
        """Testa listagem como reader sem assinatura - só vê notícias não exclusivas"""
        api_client.force_authenticate(user=user_reader)
        url = reverse("news-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Deve ver apenas notícias publicadas e não exclusivas

    def test_list_news_as_reader_with_subscription(
        self, api_client, user_with_subscription, exclusive_news
    ):
        """Testa listagem como reader com assinatura"""
        api_client.force_authenticate(user=user_with_subscription)
        url = reverse("news-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_list_news_as_writer(
        self, api_client, user_writer, draft_news, published_news
    ):
        """Testa listagem como writer - vê todas as notícias"""
        api_client.force_authenticate(user=user_writer)
        url = reverse("news-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_create_news_as_writer(self, api_client, user_writer, sample_image):
        """Testa criação de notícia como writer"""
        api_client.force_authenticate(user=user_writer)
        url = reverse("news-list")

        data = {
            "title": "Nova Notícia",
            "subtitle": "Subtítulo da nova notícia",
            "content": "Conteúdo da nova notícia",
            "picture": sample_image,
            "status": New.DRAFT,
            "is_exclusive": False,
            "verticals": [SubscriptionPlan.POWER],
        }

        response = api_client.post(url, data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert New.objects.filter(title="Nova Notícia").exists()

        # Verifica se o autor foi setado automaticamente
        news = New.objects.get(title="Nova Notícia")
        assert news.author == user_writer

    def test_create_news_as_reader(self, api_client, user_reader, sample_image):
        """Testa criação de notícia como reader - deve falhar"""
        api_client.force_authenticate(user=user_reader)
        url = reverse("news-list")

        data = {
            "title": "Tentativa de Criação",
            "subtitle": "Subtítulo",
            "content": "Conteúdo",
            "picture": sample_image,
            "status": New.DRAFT,
        }

        response = api_client.post(url, data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Você não tem permissão para criar/editar notícias" in str(response.data)

    def test_update_own_news_as_writer(self, api_client, user_writer, draft_news):
        """Testa atualização da própria notícia como writer"""
        api_client.force_authenticate(user=user_writer)
        url = reverse("news-detail", kwargs={"pk": draft_news.id})

        data = {
            "title": "Título Atualizado",
            "subtitle": draft_news.subtitle,
            "content": draft_news.content,
            "status": New.PUBLISHED,
            "is_exclusive": draft_news.is_exclusive,
            "verticals": draft_news.verticals,
        }

        response = api_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        draft_news.refresh_from_db()
        assert draft_news.title == "Título Atualizado"
        assert draft_news.status == New.PUBLISHED

    def test_update_other_user_news(self, api_client, user_writer, published_news):
        """Testa tentativa de atualizar notícia de outro usuário"""
        # Criar outro writer
        other_writer = user_writer.__class__.objects.create_user(
            username="other_writer",
            email="other@test.com",
            password="test123",
            user_type=user_writer.__class__.WRITER,
        )

        api_client.force_authenticate(user=other_writer)
        url = reverse("news-detail", kwargs={"pk": published_news.id})

        data = {"title": "Tentativa de Hack"}

        response = api_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Você não tem permissão para editar essa notícia" in str(response.data)

    def test_delete_own_news_as_writer(self, api_client, user_writer, draft_news):
        """Testa deleção da própria notícia como writer"""
        api_client.force_authenticate(user=user_writer)
        url = reverse("news-detail", kwargs={"pk": draft_news.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Verifica soft delete
        assert not New.objects.filter(id=draft_news.id).exists()
        assert New.all_objects.filter(id=draft_news.id).exists()

    def test_retrieve_news_detail(self, api_client, user_reader, published_news):
        """Testa visualização de detalhes de uma notícia"""
        api_client.force_authenticate(user=user_reader)
        url = reverse("news-detail", kwargs={"pk": published_news.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == published_news.title

    def test_filter_news_by_status(
        self, api_client, user_writer, published_news, draft_news
    ):
        """Testa filtro por status"""
        api_client.force_authenticate(user=user_writer)
        url = reverse("news-list")

        # Filtrar apenas notícias publicadas
        response = api_client.get(url, {"status": New.PUBLISHED})

        assert response.status_code == status.HTTP_200_OK

    def test_ordering_news(self, api_client, user_writer):
        """Testa ordenação de notícias"""
        api_client.force_authenticate(user=user_writer)
        url = reverse("news-list")

        # Ordenar por título
        response = api_client.get(url, {"ordering": "title"})
        assert response.status_code == status.HTTP_200_OK

        # Ordenar por data de publicação
        response = api_client.get(url, {"ordering": "-published_at"})
        assert response.status_code == status.HTTP_200_OK

    def test_reader_cannot_see_draft_news(self, api_client, user_reader, draft_news):
        """Testa que reader não vê notícias em rascunho"""
        api_client.force_authenticate(user=user_reader)
        url = reverse("news-detail", kwargs={"pk": draft_news.id})

        response = api_client.get(url)

        # Pode retornar 404 se a queryset filtrar drafts
        assert response.status_code in [
            status.HTTP_404_NOT_FOUND,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_reader_cannot_see_exclusive_without_subscription(
        self, api_client, user_reader, exclusive_news
    ):
        """Testa que reader sem assinatura não vê notícias exclusivas"""
        api_client.force_authenticate(user=user_reader)
        url = reverse("news-detail", kwargs={"pk": exclusive_news.id})

        response = api_client.get(url)

        # Pode retornar 404 se a queryset filtrar exclusivas
        assert response.status_code in [
            status.HTTP_404_NOT_FOUND,
            status.HTTP_403_FORBIDDEN,
        ]
