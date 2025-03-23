from fyers_apiv3 import fyersModel

def generate_fyers_auth_url(client_id, secret_key, redirect_uri, state):
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        state=state
    )
    return session.generate_authcode()


def exchange_code_for_fyers_token(code, client_id, secret_key, redirect_uri):
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code"
    )
    session.set_token(code)
    return session.generate_token()
