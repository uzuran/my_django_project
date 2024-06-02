"""import AppConfig"""

from django.apps import AppConfig


class MyPortfolioWebAppConfig(AppConfig):
    """
    AppConfig class for the My Portfolio Web App.

    This class provides configuration settings and metadata for the My Portfolio Web App
    Django application.

    Attributes:
        default_auto_field (str): The default primary key field type for models within
            this app. Defaults to 'django.db.models.BigAutoField'.
        name (str): The name of the Django application. Should match the name of the
            application directory. Defaults to 'my_portfolio_web_app'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_portfolio_web_app'
