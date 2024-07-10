import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


from courses.models import *

def test_new_user():
    user = coursedetails(course_name='patkennedy79@gmail.com')
    assert user.course_name == 'patkennedy79@gmail.com'
    # assert user.course_id == 'patkennedy79@gmail.com'
    # assert user.hashed_password != 'FlaskIsAwesome'
    # assert user.role == 'user'


