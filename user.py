from flask import request

class User:
    def authenticate():
        authToken = request.cookies.get('auth_token')

        if not authToken:
            return

        return True

    def login(username, password):
        if username != 'testUser' or password != 'testPassword':
            return

        return 'SampleText'