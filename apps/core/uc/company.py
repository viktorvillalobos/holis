from apps.core.models import Company


class CreateCompany(object):
    def __init__(self, name: str, code: str, email: str) -> 'CreateCompany':
        self.name = name
        self.code = code
        self.email = email

    def execute(self) -> Company:
        return Company.objects.create(
            name=self.name, code=self.code, email=self.email
        )
