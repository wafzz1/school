from school import school
import os
import pytest
import json


# def test_home_page():
#     # os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
#     flask_app = school()
#     flask_app.register_blueprint(hospital)
#     flask_app.config['TESTING'] = True
#     yield flask_app


#     # Create a test client using the Flask application configured for testing
#     with flask_app.test_client() as test_client:
#         response = test_client.get('/course/test')
#         assert response.status_code == 200
#         assert b"Welcome to the" in response.data
#         # assert b"Flask User Management Example!" in response.data
#         # assert b"Need an account?" in response.data
#         # assert b"Existing user?" in response.data


@pytest.fixture
def app():
    app = school()
    app.register_blueprint(hospital)
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()