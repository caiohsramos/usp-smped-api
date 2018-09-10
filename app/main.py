import api.settings

from eve import Eve

from api.validation import MyValidator
from api.auth import MyAuth
from api.auth.services import TokenService
from api.resources.accounts import secure_accounts

app = Eve(
    __name__,
    auth=MyAuth,
    validator=MyValidator,
    settings=api.settings.config
)

app.register_blueprint(TokenService, url_prefix='/auth')
app.on_insert_accounts += secure_accounts
if __name__ == '__main__':
    app.run(host='0.0.0.0')
