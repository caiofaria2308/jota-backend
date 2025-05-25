"""
Fixtures compartilhadas para testes do projeto Jota
"""

import io

import pytest
from PIL import Image
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.news.models import New
from apps.account.models import SubscriptionPlan

User = get_user_model()


@pytest.fixture
def api_client():
    """Cliente API para testes"""
    return APIClient()


@pytest.fixture
def user_reader():
    """Usuário do tipo Reader"""
    return User.objects.create_user(
        username="reader_test",
        email="reader@test.com",
        password="testpass123",
        user_type=User.READER,
    )


@pytest.fixture
def user_writer():
    """Usuário do tipo Writer"""
    return User.objects.create_user(
        username="writer_test",
        email="writer@test.com",
        password="testpass123",
        user_type=User.WRITER,
    )


@pytest.fixture
def subscription_plan():
    """Plano de assinatura básico"""
    return SubscriptionPlan.objects.create(
        name="Plano Básico",
        price=99.99,
        is_exclusive=True,
        verticals=[SubscriptionPlan.POWER, SubscriptionPlan.TAX],
    )


@pytest.fixture
def subscription_plan_premium():
    """Plano de assinatura premium"""
    return SubscriptionPlan.objects.create(
        name="Plano Premium",
        price=199.99,
        is_exclusive=True,
        verticals=[
            SubscriptionPlan.POWER,
            SubscriptionPlan.TAX,
            SubscriptionPlan.HEALTH,
            SubscriptionPlan.ENERGY,
            SubscriptionPlan.LABOR,
        ],
    )


@pytest.fixture
def user_with_subscription(user_reader, subscription_plan):
    """Usuário reader com plano de assinatura"""
    user_reader.subscription_plan = subscription_plan
    user_reader.save()
    return user_reader


@pytest.fixture
def sample_image():
    """Imagem de exemplo para upload"""
    # Criar uma imagem simples
    image = Image.new("RGB", (100, 100), color="red")
    image_io = io.BytesIO()
    image.save(image_io, format="JPEG")
    image_io.seek(0)

    return SimpleUploadedFile(
        "test_image.jpg", image_io.getvalue(), content_type="image/jpeg"
    )


@pytest.fixture
def published_news(user_writer, sample_image):
    """Notícia publicada"""
    return New.objects.create(
        title="Notícia Publicada",
        subtitle="Subtítulo da notícia publicada",
        content="Conteúdo da notícia publicada para teste",
        picture=sample_image,
        author=user_writer,
        status=New.PUBLISHED,
        is_exclusive=False,
        verticals=[SubscriptionPlan.POWER],
    )


@pytest.fixture
def exclusive_news(user_writer, sample_image):
    """Notícia exclusiva"""
    return New.objects.create(
        title="Notícia Exclusiva",
        subtitle="Subtítulo da notícia exclusiva",
        content="Conteúdo da notícia exclusiva para teste",
        picture=sample_image,
        author=user_writer,
        status=New.PUBLISHED,
        is_exclusive=True,
        verticals=[SubscriptionPlan.POWER, SubscriptionPlan.TAX],
    )


@pytest.fixture
def draft_news(user_writer, sample_image):
    """Notícia em rascunho"""
    return New.objects.create(
        title="Notícia Rascunho",
        subtitle="Subtítulo da notícia em rascunho",
        content="Conteúdo da notícia em rascunho para teste",
        picture=sample_image,
        author=user_writer,
        status=New.DRAFT,
        is_exclusive=False,
        verticals=[SubscriptionPlan.HEALTH],
    )
