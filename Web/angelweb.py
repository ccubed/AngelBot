from flask import *
import redis
from serverglob import *
from encryption import *
import requests

application = Flask(__name__)

@application.route("/")
def root():
    return render_template("index.html")


@application.route("/oauth/<provider>/<userid>")
def generate_oauth_handshake(provider, userid):
    if provider in ['Github']:
        url = "https://github.com/login/oauth/authorize?client_id={0}&redirect_uri={1}&scope=gist,public_repo&state={2}".format(oauth['github']['cid'], "https://angelbot.vertinext.com/oauth/oauthcallback/github", userid)
        return redirect(url)
    else:
        return redirect(url_for('static', filename='html/oauth_security.html', values=None), code=303)


@application.route("/oauth/oauthcallback/<provider>")
def oauth_callback(provider):
    enc = AESCipher(cryptokey)
    rcon = redis.StrictRedis(db=1)
    if 'state' not in request.args:
        return redirect(url_for('static', filename='html/oauth_security.html'), code=303)

    if 'error' in request.args:
        return redirect(url_for('static', filename='html/oauth_access.html'), code=303)

    if 'code' in request.args:
        atoken = request.args.get('code')
        if provider == "github":
            params = {'client_id': oauth['github']['cid'], 'client_secret': oauth['github']['csecret'], 'code': atoken, 'redirect_uri': 'https://angelbot.vertinext.com/oauth/oauthcallback/github', 'state': request.args.get('state')}
            headers = {'Accept':'application/json'}
            ga = requests.post("https://github.com/login/oauth/access_token", params=params, headers=headers)
            gaj = ga.json()
            if 'access_token' in gaj:
                access = enc.encrypt(gaj['access_token'])
                scope = gaj['scope']
                rcon.hset(request.args.get('state'), 'Github_Token', access)
                rcon.hset(request.args.get('state'), 'Github_Scope', scope)
                return redirect(url_for('static', filename='html/oauth_success.html'), code=303)
            else:
                return redirect(url_for('static', filename='html/oauth_failed.html'), code=303)

application.debug = True

if __name__ == "__main__":
    application.run(threaded=True, port=8000)
