import enum


class Email(enum.Enum):
    SUBJECT = 'SUBJECT'
    BODY = 'MESSAGE'

    @property
    def get_value(self) -> str:
        if self.name == self.SUBJECT.name:
            return "SHERACORE from skyloov"
        if self.name == self.BODY.name:
            return "This is from SKYLOOV, wellcome to SKYLOOV, you can choose and get your apartment 100 online"
