from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from skyloov.utilities.db.models import DataModel


# DataModel
class DataModelSummarySerializer(serializers.ModelSerializer):
    i_content_type_id = serializers.SerializerMethodField()

    class Meta:
        abstract = True
        model = DataModel
        fields = [
            'pk',
            'resourcetype',
            'i_content_type_id',
            'created_at',
            'update_at',
            'is_active',
        ]

        read_only_fields = [
            'pk',
            'resourcetype',
            'i_content_type_id',
            'created_at',
            'update_at',
            'is_active',
        ]

    def get_i_content_type_id(self, obj):
        # ContentType Manager will cache the data so don't worry about performance
        return ContentType.objects.get_for_model(obj).pk


class DataModelDetailSerializer(DataModelSummarySerializer):
    class Meta:
        abstract = True
        model = DataModel
        fields = DataModelSummarySerializer.Meta.fields + []

        read_only_fields = DataModelSummarySerializer.Meta.fields + []
