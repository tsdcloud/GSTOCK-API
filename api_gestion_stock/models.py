import uuid as uuid
from django.db import models

from datetime import datetime, timedelta


class BaseUUIDModel(models.Model):
    """
    Base UUID model that represents a unique identifier for a given model.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @classmethod
    def readByToken(cls, token: str, is_change=False):
        """ take an object by token"""
        if is_change is False:
            return cls.objects.get(id=token)
        return cls.objects.select_for_update().get(id=token)

    @classmethod
    def mois_courant(cls):
        date_aujourd_hui = datetime.now()
        debut_mois = date_aujourd_hui.replace(day=1)
        fin_mois = datetime(
            date_aujourd_hui.year, date_aujourd_hui.month + 1, 1
        ) if date_aujourd_hui.month < 12 else datetime(
            date_aujourd_hui.year + 1, 1, 1)
        return (debut_mois, fin_mois)

    @classmethod
    def periode_derniers_x_jours(cls, x=30):
        date_fin = datetime.now()
        date_debut = date_fin - timedelta(days=x)
        return (date_debut, date_fin)

    @classmethod
    def periode_prochains_x_jours(cls, x=30):
        date_debut = datetime.now()
        date_fin = date_debut + timedelta(days=x)
        return (date_debut, date_fin)

    # def delete(self, user: str):
    #     """ delete """
    #     self.is_active = False
    #     self.save(user=user, action="CHANGE")
    #     return self

