import requests
import re

class WebService:
    def __init__(self, base_url: str):
        self.session = requests.session()
        self.base_url = base_url
    

    def _get_token(self, url: str):
        response = self.session.get(self.base_url + url)
        html = response.text
        token = re.search('<input type="hidden" name="csrfmiddlewaretoken" value="(.+?)">', html)
        if token:
            return token.group(1)
        else:    
            assert False, f'failed to get token {token}' 


    def login(self, login: str, password: str):
        token = self._get_token('/login/')
        data = {
            'username': login, 
            'password': password, 
            'csrfmiddlewaretoken': token,
        }
        self.session.post(self.base_url +'/login/', data=data)
        csrftoken = self.session.cookies.get('csrftoken')
        self.session.headers.update({'X-CSRFToken': csrftoken})

    def create_test(self, test_name:str, test_description: str):
        token = self._get_token('/test/new')
        data = {
            'name': test_name, 
            'description': test_description, 
            'csrfmiddlewaretoken': token,
        }
        response = self.session.post(self.base_url + '/test/new', data=data) 
    
    def report_test_execute(self, test_id: int, status: str):
        self.session.post(self.base_url + f'/tests/{test_id}/status', json={'status': status})


    def close(self):
        self.session.close()