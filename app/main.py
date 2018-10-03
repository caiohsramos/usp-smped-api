import app.api.settings

from eve import Eve

from app.api.validation import MyValidator
from app.api.auth import MyAuth
from app.api.auth.services import TokenService
from app.api.resources.accounts import secure_accounts

server = Eve(
    __name__,
    auth=MyAuth,
    validator=MyValidator,
    settings=app.api.settings.config
)

server.register_blueprint(TokenService, url_prefix='/auth')
server.on_insert_accounts += secure_accounts

if __name__ == '__main__':
    server.run(host='0.0.0.0',port=3001)
