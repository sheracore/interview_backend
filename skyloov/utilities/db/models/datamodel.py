from django.db import models
from django.utils.translation import gettext_lazy as _
"""
DataModel
"""


class DataModelQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super(DataModelQuerySet, self).__init__(*args, **kwargs)

    def active(self):
        return self.filter(is_active=True)


class DataModelManager(models.Manager):
    def get_queryset(self):
        return DataModelQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class DataModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    update_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.pk)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(DataModel, self).save(*args, **kwargs)

    @property
    def record_is_adding(self):
        return self._state.adding

    @property
    def resourcetype(self):
        return self._meta.object_name


"""
User Data Model
"""


class UserDataModelQuerySet(DataModelQuerySet):
    pass


class UserDataModelManager(DataModelManager):
    def get_queryset(self):
        return UserDataModelQuerySet(self.model, using=self._db)


class UserDataModel(DataModel):
    """Abstract for user model"""

    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('User'))

    class Meta:
        abstract = True