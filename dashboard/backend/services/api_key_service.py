import secrets


class APIKeyService:

    def generate(self):

        return secrets.token_hex(32)

    def validate(self, key):

        # lookup database
        return True