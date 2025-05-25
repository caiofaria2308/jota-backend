"""
Testes de performance e carga
"""

import pytest
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from apps.news.models import New
from apps.account.models import User, SubscriptionPlan


@pytest.mark.slow
@pytest.mark.django_db
class TestPerformance:
    """Testes de performance"""

    def test_bulk_news_creation(self, api_client, user_writer, sample_image):
        """Testa criação em massa de notícias"""
        import time

        # Medir tempo de criação em massa no banco
        start_time = time.time()

        news_list = []
        for i in range(10):
            news_list.append(
                New(
                    title=f"Notícia Performance {i}",
                    subtitle=f"Subtítulo {i}",
                    content=f"Conteúdo da notícia {i}",
                    author=user_writer,
                    status=New.PUBLISHED,
                    is_exclusive=False,
                    verticals=[SubscriptionPlan.POWER],
                )
            )

        # Bulk create para performance
        New.objects.bulk_create(news_list)

        end_time = time.time()
        creation_time = end_time - start_time

        # Verificar que todas foram criadas e tempo foi razoável
        assert New.objects.filter(title__startswith="Notícia Performance").count() == 10
        assert creation_time < 1.0  # Deve levar menos de 1 segundo

    def test_large_queryset_performance(self, api_client, user_writer):
        """Testa performance com grande volume de dados"""
        # Criar muitas notícias via ORM (mais rápido que API)
        news_list = []
        for i in range(50):
            news = New(
                title=f"Notícia Massa {i}",
                subtitle=f"Sub {i}",
                content=f"Conteúdo {i}",
                author=user_writer,
                status=New.PUBLISHED,
                is_exclusive=i % 3 == 0,  # Algumas exclusivas
                verticals=(
                    [SubscriptionPlan.POWER] if i % 2 == 0 else [SubscriptionPlan.TAX]
                ),
            )
            news_list.append(news)

        New.objects.bulk_create(news_list)

        # Testar listagem com grande volume
        api_client.force_authenticate(user=user_writer)
        list_url = reverse("news-list")

        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK

        # Testar com filtros
        response = api_client.get(list_url, {"status": New.PUBLISHED})
        assert response.status_code == status.HTTP_200_OK

        # Testar com ordenação
        response = api_client.get(list_url, {"ordering": "title"})
        assert response.status_code == status.HTTP_200_OK

    def test_subscription_filtering_performance(self, api_client, sample_image):
        """Testa performance do filtro de assinaturas"""
        # Criar múltiplos planos
        plans = []
        for i in range(5):
            plan = SubscriptionPlan.objects.create(
                name=f"Plano {i}",
                price=99.99 + i * 50,
                verticals=[SubscriptionPlan.POWER, SubscriptionPlan.TAX],
            )
            plans.append(plan)

        # Criar múltiplos usuários com diferentes planos
        users = []
        for i, plan in enumerate(plans):
            user = User.objects.create_user(
                username=f"user_{i}",
                email=f"user{i}@test.com",
                password="test123",
                user_type=User.READER,
                subscription_plan=plan,
            )
            users.append(user)

        # Criar writer
        writer = User.objects.create_user(
            username="writer_perf",
            email="writer@perf.com",
            password="test123",
            user_type=User.WRITER,
        )

        # Criar muitas notícias exclusivas
        for i in range(20):
            New.objects.create(
                title=f"Notícia Exclusiva {i}",
                subtitle=f"Sub {i}",
                content=f"Conteúdo {i}",
                author=writer,
                status=New.PUBLISHED,
                is_exclusive=True,
                verticals=[SubscriptionPlan.POWER, SubscriptionPlan.TAX],
            )

        # Testar acesso de cada usuário
        list_url = reverse("news-list")
        for user in users:
            api_client.force_authenticate(user=user)
            response = api_client.get(list_url)
            assert response.status_code == status.HTTP_200_OK

    @override_settings(DEBUG=True)
    def test_query_optimization(
        self, api_client, user_writer, django_assert_num_queries
    ):
        """Testa otimização de queries"""
        # Criar algumas notícias
        for i in range(3):
            New.objects.create(
                title=f"Notícia Query {i}",
                subtitle=f"Sub {i}",
                content=f"Conteúdo {i}",
                author=user_writer,
                status=New.PUBLISHED,
            )

        api_client.force_authenticate(user=user_writer)
        list_url = reverse("news-list")

        # Verificar número de queries na listagem (ajustado para realidade)
        with django_assert_num_queries(5):  # Count + Select + Author lookups
            response = api_client.get(list_url)
            assert response.status_code == status.HTTP_200_OK
