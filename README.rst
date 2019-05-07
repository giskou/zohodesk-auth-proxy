ZOHO Desk authentication proxy
==============================

This microservice is managing the refreshing of the oauth2 token used to
authenticate with the Zoho Desk api.

Any request to this service will be forwarded to zoho with the right token
attached in the 'Authorization' header.


Configuration
-------------

You will need to create an app/client in the zoho development webpage [1]_

The redirect url is not really important because no user or browser is going to
be involved in the auth process. It just has to be defined to a value that has
to be the same in the configuration of this microservice.
Select *WEB Based* as a client type.

Keep *Client ID*, *Client Secret* and *Redirect URI* to configure this
microservice.
You also need the *Organization ID*, which you can get from the Desk main
webpage -> Setup (the cog on the top right) -> General Settings
(under Customization) -> Developer Space -> API (the bottom of the page)
The *Token Scope* is a comma separated list of scopes [2]_

You will also need a *Code* which will only be used to get the refresh token.
To get that code go to the zoho development webpage [1]_ and, on the client
you are going to use, click the three vertical dots of the far right and
select self client.
Enter the scope (comma separated for more than one) [2]_ and set the expiry.

You now have <expiry> minutes to use that token and get the refresh token.

To get a refresh token by running the following::

 curl --request POST \
       --url https://accounts.zoho.eu/oauth/v2/token \
       --header 'content-type: application/x-www-form-urlencoded' \
       --data grant_type=authorization_code \
       --data client_id=<client_id> \
       --data client_secret=<client_secret> \
       --data redirect_uri=<redirect_uri> \
       --data scope=<scope> \
       --data code=<code>

The result should be look like this::

   {
     "access_token": "1000.67013ab3960787bcf3affae67e649fc0.83a789c859e040bf11e7d05f9c8b5ef6",
     "refresh_token": "1000.aed4288cd9cfb2d63d093faef1b98890.2f4aa58ddadbec9fbbfd683805da839b",
     "expires_in_sec": 3600,
     "token_type": "Bearer",
     "expires_in": 3600000
   }

:NOTE:
    The refresh token does not expire. If you want to revoke it, remove the
    client app and create a new one.

The following environment variables need to be defined:

- CLIENT_ID
- CLIENT_SECRET
- REDIRECT_URI
- ORG_ID
- REFRESH_TOKEN

Extra optional environment variables:

- API_ROOT (default: https://desk.zoho.eu)
- ACCESS_TOKEN_URL (default: https://accounts.zoho.eu/oauth/v2/token)
- TOKEN_SCOPE (default: Desk.tickets.READ)

:WARNING:
    Be extra carefull with the top level part of the domains.
    If you have an account in .eu then all the urls
    (developer console, api, webpage, access token) **must end with .eu**


Sample docker-compose file for running::

  version: "3.7"

  services:
    zohodesk-auth-proxy:
      image: zohodesk-auth-proxy:latest
      ports:
        - 8000:8000
      environment:
        - CLIENT_ID=<client_id>
        - CLIENT_SECRET=<client_secret>
        - REDIRECT_URI=<redirect_uri>
        - REFRESH_TOKEN=<refresh_token>
        - ORG_ID=<org_id>


.. [1] https://accounts.zoho.eu/developerconsole
.. [2] https://desk.zoho.com/DeskAPIDocument#Authentication#Authtokens#Oauth_Scopes
