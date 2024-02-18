from django.db import models


class CreationService():
    def __init__(self, model: models.Model) -> None:
        self.model = model

    def get_or_create(self, data: dict):
        object = self.model.objects.filter(**data).first()
        if object is None:
            object = self.model.objects.create(**data)
        return object


class CreationServiceFactroy:
    @staticmethod
    def get(model: models.Model):
        classes = {}
        if model in classes:
            return classes[model]()

        return CreationService(model)
