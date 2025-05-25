from logging import Logger

log = Logger(__name__)


def send_email(subject, recipient_list, body):
    """
    Mock function to send an email.
    In a real application, you would use Django's email sending capabilities.
    """
    log.info(f"Sending email with subject: {subject} to {recipient_list}")
    log.info(f"Email body: {body}")
    # Here you would integrate with an actual email service
    # e.g., send_mail(subject, body, from_email, recipient_list)


def publish_news(news_id=None):
    """
    Send an alert to all users about a new news article.
    """
    from apps.news.models import New
    from apps.account.models import User

    log.info(f"Publishing news with ID: {news_id}")
    if not news_id:
        log.warning("No news ID provided.")
        return
    news: New = New.objects.get(id=news_id)
    users = (
        User.objects.select_related(
            "subscription_plan",
        )
        .prefetch_related(
            "subscription_plan__verticals",
        )
        .filter(
            user_type=User.READER,
        )
    )
    if news.is_exclusive:
        # Check if the user has the right subscription plan
        users = users.filter(
            subscription_plan__verticals__overlap=news.verticals,  # TODO VERIFY OVERLAP
            subscription_plan__is_exclusive=True,
        )
    news.status = New.PUBLISHED
    news.save()
    # Notify all users about the new article
    for user in users:
        send_email(
            subject="Notificação de nova notícia",
            recipient_list=[user.email],
            body=f"Confira a nova notícia: {news.title}",
        )
    log.info(f"Alert sent to all users about news article: {news.title}")
