from social.backends.facebook import FacebookOAuth2


class FacebookAuth(FacebookOAuth2):
    AUTHORIZATION_URL = 'https://www.facebook.com/v2.4/dialog/oauth'
    ACCESS_TOKEN_URL = 'https://graph.facebook.com/v2.4/oauth/access_token'
    REVOKE_TOKEN_URL = 'https://graph.facebook.com/v2.4/{uid}/permissions'
    USER_DATA_URL = 'https://graph.facebook.com/v2.4/me?fields=id,email,birthday,gender,name,link'
