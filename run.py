from eve import Eve
from oauth2 import BearerAuth
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth
import os

app = Eve(auth=BearerAuth)
app.config['SENTINEL_MANAGEMENT_USERNAME'] = 'admin'
app.config['SENTINEL_MANAGEMENT_PASSWORD'] = 'admin'
app.config['SENTINEL_REDIS_URL'] = os.environ.get('REDIS_URL','redis://localhost:6379')
app.config['SENTINEL_MONGO_URI'] = os.environ.get('MONGO_URI','mongodb://localhost')

ResourceOwnerPasswordCredentials(app)

@app.route('/endpoint')
@oauth.require_oauth()
def restricted_access():
    return "You made it through and accessed the protected resource!"

if __name__=='__main__':
    app.run(host='0.0.0.0',ssl_context='adhoc')