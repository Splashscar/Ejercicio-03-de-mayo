API_TOKEN = "securewallet2026"


def validate_token(headers):
    token = headers.get("X-API-TOKEN")

    return token == API_TOKEN