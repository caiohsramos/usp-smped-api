import api.settings

from eve import Eve
from eve.auth import requires_auth
from flask import request, abort, jsonify

from api.validation import MyValidator
from api.auth import MyAuth
from api.auth.services import TokenService
from api.resources.accounts import secure_accounts
from api.resources.accounts import secure_account_update
from api.email_service import Email
from api.auth.services import crossdomain

app = Eve(
    __name__,
    auth=MyAuth,
    validator=MyValidator,
    settings=api.settings.config
)

@app.route('/email', methods = ['POST', 'OPTIONS'])
@requires_auth('forms')
@crossdomain(origin='*')
def send_email():
    data = request.get_json()
    e = Email()
    try:
        e.send_email(data['emails'], data['subject'], data['message'])
        return jsonify({'status': 'emails sent'})
    except:
        abort(401, description="The payload was invalid")


app.register_blueprint(TokenService, url_prefix='/auth')
app.on_insert_accounts += secure_accounts
app.on_update_accounts += secure_account_update

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3001)
