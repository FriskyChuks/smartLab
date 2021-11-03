from django.apps import AppConfig


class RadiologyConfig(AppConfig):
    name = 'radiology'

    def ready(self):
        import radiology.signals