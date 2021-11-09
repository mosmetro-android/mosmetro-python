from requests import Session
from user_agent import generate_user_agent


session = Session()
# session.verify = False  # only for testing
session.headers['user-agent'] = generate_user_agent()
