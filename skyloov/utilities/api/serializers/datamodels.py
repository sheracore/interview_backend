from rest_framework import serializers

from skyloov.utilities.db.models import DataModel


# DataModel
class DataModelSummarySerializer(serializers.ModelSerializer):
    i_content_type_id = serializers.SerializerMethodField()

    class Meta:
        abstract = True
        model = DataModel
        fields = [
            'pk',
            'created_at',
            'update_at',
            'is_active',
        ]

        read_only_fields = [
            'pk',
            'created_at',
            'update_at',
            'is_active',
        ]


class DataModelDetailSerializer(DataModelSummarySerializer):
    class Meta:
        abstract = True
        model = DataModel
        fields = DataModelSummarySerializer.Meta.fields + []

        read_only_fields = DataModelSummarySerializer.Meta.fields + []
