"""Zeff Cloud Dataset Type."""
__docformat__ = "reStructuredText en"

import enum


@enum.unique
class ZeffDatasetType(enum.Enum):
    """Type of dataset."""

    generic = "GENERIC"
    temporal = "TEMPORAL"
    geospatial = "GEOSPATIAL"

    @property
    def validator(self) -> str:
        """Return default validator python name for this dataset type."""
        # pylint: disable=no-member
        name = self.name.capitalize()
        return f"{__package__}.validator.Record{name}Validator"

    @property
    def root_tag(self) -> str:
        """Return common tag root for Zeff URI tags."""
        return "tag:zeff.com,2019-12"

    @property
    def datasets_list_tag(self) -> str:
        """Tag to list datasets."""
        return f"{self.root_tag}:datasets/list"

    @property
    def dataset_add_tag(self) -> str:
        """Tag to add a new dataset."""
        return f"{self.root_tag}:datasets/{self.name}/add"

    @property
    def dataset_tag(self) -> str:
        """Tag to get, update, or delete a specific dataset."""
        return f"{self.root_tag}:datasets"

    @property
    def models_list_tag(self) -> str:
        """Tag to list models in a dataset."""
        return f"{self.root_tag}:models/list"

    @property
    def model_tag(self) -> str:
        """Tag to get, update, or delete a specific model version."""
        return f"{self.root_tag}:models"

    @property
    def model_records_list_tag(self) -> str:
        """Tag to list records in a model."""
        return f"{self.root_tag}:models/records_{self.name}/list"

    @property
    def model_record_add_tag(self) -> str:
        """Tag to add a record to a model."""
        return f"{self.root_tag}:models/records_{self.name}/add"

    @property
    def model_record_tag(self) -> str:
        """Tag to get, update, or delete a specific record in a model."""
        return f"{self.root_tag}:models/records_{self.name}"

    @property
    def records_list_tag(self) -> str:
        """Tag to list records in a dataset."""
        return f"{self.root_tag}:records_{self.name}/list"

    @property
    def record_add_tag(self) -> str:
        """Tag to add a record to a dataset."""
        return f"{self.root_tag}:records_{self.name}/add"

    @property
    def record_tag(self) -> str:
        """Tag to get, update, or delete a specific record in a dataset."""
        return f"{self.root_tag}:records_{self.name}"
