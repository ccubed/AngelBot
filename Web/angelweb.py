from flask import *
import redis
from serverglob import *
from encryption import *

application = Flask(__name__)

@application.route("/")
def root():
    return render_template("index.html")


@application.route("/oauth/<provider>/<userid>")
def generate_oauth_handshake(provider, userid):
    if provider in ['Github']:
        url = "https://github.com/login/oauth/authorize?client_id={0}&redirect_uri={1}&scope=gist,public_repo&state={2}".format(oauth['github']['cid'], "https://angelbot.vertinext.com/oauth/oauthcallback", userid)
        return redirect(url)
    else:
        return redirect(url_for('static', filename='html/oauth_security.html', values=None), code=303)

@application.route("/oauth/oauthcallback")
def oauth_callback():
    if 'state' not in request.args:
        return redirect(url_for('static', filename='html/oauth_security.html'), code=303)
    else:
        rcon = redis.StrictRedis(host="localhost", port=6379, db=1)
        status = rcon.hget(request.args.get('state'), "oauth_status")
        rcon.shutdown()
        if status != "in_progress":
            return redirect(url_for('static', filename='html/oauth_security.html'), code=303)

    if 'error' in request.args:
        return redirect(url_for('static', filename='html/oauth_access.html'), code=303)

    rcon = redis.StrictRedis(host="localhost", port=6379, db=1)
    enc = AESCipher(cryptokey)
    atoken = enc.encrypt(request.args.get('code'))
    rcon.hset(request.args.get('state'), "Github_Code", atoken)
    rcon.hset(request.args.get('state'), "oauth_status", "None")
    rcon.shutdown()
    return redirect(url_for('static', filename='html/oauth_success.html'), code=303)


application.debug = True

if __name__ == "__main__":
    application.run(threaded=True, port=8000)
