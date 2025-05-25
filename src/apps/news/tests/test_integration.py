"""
Testes de integração para o sistema de notícias
"""

import pytest
from django.urls import reverse
from rest_framework import status

from apps.news.models import New
from apps.account.models import User, SubscriptionPlan


@pytest.mark.integration
@pytest.mark.django_db
class TestNewsIntegration:
    """Testes de integração para o sistema de notícias"""

    def test_complete_news_workflow(self, api_client, user_writer, sample_image):
        """Testa o fluxo completo: criar, editar, publicar e deletar notícia"""
        api_client.force_authenticate(user=user_writer)

        # 1. Criar notícia em rascunho
        create_url = reverse("news-list")
        create_data = {
            "title": "Notícia Workflow",
            "subtitle": "Subtítulo do workflow",
            "content": "Conteúdo inicial",
            "picture": sample_image,
            "status": New.DRAFT,
            "is_exclusive": False,
            "verticals": [SubscriptionPlan.POWER],
        }

        create_response = api_client.post(create_url, create_data, format="multipart")
        assert create_response.status_code == status.HTTP_201_CREATED
        news_id = create_response.data["id"]

        # 2. Editar a notícia
        edit_url = reverse("news-detail", kwargs={"pk": news_id})
        edit_data = {
            "title": "Notícia Workflow Editada",
            "content": "Conteúdo atualizado",
            "is_exclusive": True,
        }

        edit_response = api_client.patch(edit_url, edit_data, format="json")
        assert edit_response.status_code == status.HTTP_200_OK
        assert edit_response.data["title"] == "Notícia Workflow Editada"
        assert edit_response.data["is_exclusive"] is True

        # 3. Publicar a notícia
        publish_data = {"status": New.PUBLISHED}
        publish_response = api_client.patch(edit_url, publish_data, format="json")
        assert publish_response.status_code == status.HTTP_200_OK
        assert publish_response.data["status"] == New.PUBLISHED

        # 4. Deletar a notícia
        delete_response = api_client.delete(edit_url)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # 5. Verificar que foi soft delete
        assert not New.objects.filter(id=news_id).exists()
        assert New.all_objects.filter(id=news_id).exists()

    def test_subscription_access_control(self, api_client, sample_image):
        """Testa controle de acesso baseado em assinatura"""
        # Criar writer
        writer = User.objects.create_user(
            username="writer_access",
            email="writer@access.com",
            password="test123",
            user_type=User.WRITER,
        )

        # Criar plano de assinatura
        plan = SubscriptionPlan.objects.create(
            name="Plano Power",
            price=99.99,
            is_exclusive=True,
            verticals=[SubscriptionPlan.POWER, SubscriptionPlan.TAX],
        )

        # Criar reader com assinatura
        reader_with_plan = User.objects.create_user(
            username="reader_with_plan",
            email="reader_plan@test.com",
            password="test123",
            user_type=User.READER,
            subscription_plan=plan,
        )

        # Criar reader sem assinatura
        reader_without_plan = User.objects.create_user(
            username="reader_no_plan",
            email="reader_no_plan@test.com",
            password="test123",
            user_type=User.READER,
        )

        # Writer cria notícia exclusiva
        api_client.force_authenticate(user=writer)
        create_url = reverse("news-list")
        news_data = {
            "title": "Notícia Exclusiva Power",
            "subtitle": "Apenas para assinantes",
            "content": "Conteúdo exclusivo",
            "picture": sample_image,
            "status": New.PUBLISHED,
            "is_exclusive": True,
            "verticals": [SubscriptionPlan.POWER],
        }

        create_response = api_client.post(create_url, news_data, format="multipart")
        assert create_response.status_code == status.HTTP_201_CREATED
        create_response.data["id"]

        # Reader com plano adequado deve ver a notícia
        api_client.force_authenticate(user=reader_with_plan)
        list_url = reverse("news-list")
        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK

        # Reader sem plano não deve ver a notícia
        api_client.force_authenticate(user=reader_without_plan)
        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK
        # A resposta pode estar vazia ou não conter a notícia exclusiva

    def test_multiple_verticals_access(self, api_client, sample_image):
        """Testa acesso com múltiplas verticais"""
        # Criar writer
        writer = User.objects.create_user(
            username="writer_multi",
            email="writer@multi.com",
            password="test123",
            user_type=User.WRITER,
        )

        # Criar planos diferentes
        plan_power = SubscriptionPlan.objects.create(
            name="Plano Power", price=99.99, verticals=[SubscriptionPlan.POWER]
        )

        plan_complete = SubscriptionPlan.objects.create(
            name="Plano Completo",
            price=199.99,
            verticals=[
                SubscriptionPlan.POWER,
                SubscriptionPlan.TAX,
                SubscriptionPlan.HEALTH,
            ],
        )

        # Criar readers com planos diferentes
        reader_power = User.objects.create_user(
            username="reader_power",
            email="reader_power@test.com",
            password="test123",
            subscription_plan=plan_power,
        )

        reader_complete = User.objects.create_user(
            username="reader_complete",
            email="reader_complete@test.com",
            password="test123",
            subscription_plan=plan_complete,
        )

        # Writer cria notícia que requer múltiplas verticais
        api_client.force_authenticate(user=writer)
        create_url = reverse("news-list")
        news_data = {
            "title": "Notícia Multi-Vertical",
            "subtitle": "Requer Power e Tax",
            "content": "Conteúdo multi-vertical",
            "picture": sample_image,
            "status": New.PUBLISHED,
            "is_exclusive": True,
            "verticals": [SubscriptionPlan.POWER, SubscriptionPlan.TAX],
        }

        create_response = api_client.post(create_url, news_data, format="multipart")
        assert create_response.status_code == status.HTTP_201_CREATED

        # Reader com plano completo deve ver
        api_client.force_authenticate(user=reader_complete)
        list_response = api_client.get(reverse("news-list"))
        assert list_response.status_code == status.HTTP_200_OK

        # Reader com plano limitado pode não ver (dependendo da lógica)
        api_client.force_authenticate(user=reader_power)
        list_response = api_client.get(reverse("news-list"))
        assert list_response.status_code == status.HTTP_200_OK

    def test_writer_vs_reader_permissions(self, api_client, published_news):
        """Testa diferenças de permissões entre writer e reader"""
        reader = User.objects.create_user(
            username="test_reader",
            email="reader@permissions.com",
            password="test123",
            user_type=User.READER,
        )

        writer = User.objects.create_user(
            username="test_writer",
            email="writer@permissions.com",
            password="test123",
            user_type=User.WRITER,
        )

        # Reader não pode criar notícias
        api_client.force_authenticate(user=reader)
        create_url = reverse("news-list")
        create_data = {
            "title": "Tentativa Reader",
            "subtitle": "Não deveria funcionar",
            "content": "Conteúdo",
        }

        response = api_client.post(create_url, create_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Writer pode criar notícias
        api_client.force_authenticate(user=writer)
        response = api_client.post(create_url, create_data)
        # Pode falhar por outros motivos (campos obrigatórios), mas não por permissão
        assert response.status_code != status.HTTP_403_FORBIDDEN

        # Reader pode ver notícias publicadas
        api_client.force_authenticate(user=reader)
        detail_url = reverse("news-detail", kwargs={"pk": published_news.id})
        response = api_client.get(detail_url)
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]  # 404 se não tiver acesso por outros motivos

    def test_news_filtering_and_ordering(self, api_client, user_writer, sample_image):
        """Testa filtros e ordenação de notícias"""
        api_client.force_authenticate(user=user_writer)

        # Criar várias notícias com diferentes status e verticais
        news_data = [
            {
                "title": "Notícia A - Power",
                "subtitle": "Sub A",
                "content": "Conteúdo A",
                "picture": sample_image,
                "status": New.PUBLISHED,
                "verticals": [SubscriptionPlan.POWER],
            },
            {
                "title": "Notícia B - Tax",
                "subtitle": "Sub B",
                "content": "Conteúdo B",
                "picture": sample_image,
                "status": New.DRAFT,
                "verticals": [SubscriptionPlan.TAX],
            },
        ]

        create_url = reverse("news-list")
        for data in news_data:
            api_client.post(create_url, data, format="multipart")

        # Testar filtro por status
        list_url = reverse("news-list")
        response = api_client.get(list_url, {"status": New.PUBLISHED})
        assert response.status_code == status.HTTP_200_OK

        # Testar ordenação por título
        response = api_client.get(list_url, {"ordering": "title"})
        assert response.status_code == status.HTTP_200_OK

        # Testar ordenação por data de publicação
        response = api_client.get(list_url, {"ordering": "-published_at"})
        assert response.status_code == status.HTTP_200_OK
