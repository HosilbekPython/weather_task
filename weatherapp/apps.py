from django.apps import AppConfig
from django.core.checks import register, CheckMessage, ERROR
from django.db import connection
from django.db.utils import OperationalError

class WeatherappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weatherapp'

    def ready(self):
        try:
            with connection.cursor():
                pass
            from .tasks import start_scheduler
            start_scheduler()
        except OperationalError:
            def db_check(*args, **kwargs):
                return [
                    CheckMessage(
                        level=ERROR,
                        msg="Could not start scheduler: Database is not ready.",
                        hint="Ensure migrations are applied and the database is accessible.",
                        obj=self,
                    )
                ]
            register(db_check)