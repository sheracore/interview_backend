from skyloov.utilities.db.models import UserDataModel

from .datamodels import DataModelDetailSerializer, DataModelSummarySerializer


# UserDataModel
class UserDataModelSummarySerializer(DataModelSummarySerializer):
    class Meta:
        abstract = True
        model = UserDataModel
        fields = DataModelSummarySerializer.Meta.fields + []

        read_only_fields = DataModelSummarySerializer.Meta.read_only_fields + []


class UserDataModelDetailSerializer(DataModelDetailSerializer, UserDataModelSummarySerializer):
    class Meta:
        abstract = True
        model = UserDataModel
        fields = DataModelDetailSerializer.Meta.fields + UserDataModelSummarySerializer.Meta.fields + []

        read_only_fields = (
            DataModelDetailSerializer.Meta.read_only_fields + UserDataModelSummarySerializer.Meta.read_only_fields + []
        )
