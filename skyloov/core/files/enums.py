import enum


class UploadSizeType(enum.Enum):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    ENTERPRISE = 'ENTERPRISE'

    @property
    def get_size(self):
        if self.name == self.SMALL.name:
            return 100 * 1024 * 1024
        elif self.name == self.MEDIUM.name:
            return 250 * 1024 * 1024
        elif self.name == self.HIGH.name:
            return 500 * 1024 * 1024
        elif self.name == self.ENTERPRISE.name:
            return 3072 * 1024 * 1024
