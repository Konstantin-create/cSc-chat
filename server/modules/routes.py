from app import app


# User routes
@app.route('/api/user-signup')
def _api_signup():
    return {'data': 'test'}
