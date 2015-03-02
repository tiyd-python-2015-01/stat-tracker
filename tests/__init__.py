def login(user, client):
    return client.post('/login', data=dict(
        email=user.email,
        password=user.password
    ), follow_redirects=True)