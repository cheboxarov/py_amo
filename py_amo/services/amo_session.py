import requests
from .account_manage import AccountManager
from repositories import PipelinesRepository, LeadsRepository, ContactsRepository, UsersRepository, SourcesRepository


class AmoSession(AccountManager):

    def __init__(self, token: str, subdomain: str):
        self.token = token
        self.subdomain = subdomain
    
    def get_requests_session(self):
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })
        return session
    
    def get_url(self):
        return f"https://{self.subdomain}.amocrm.ru"
    
    @property
    def leads(self):
        return LeadsRepository(self)
    
    @property
    def contacts(self):
        return ContactsRepository(self)
    
    @property
    def pipelines(self):
        return PipelinesRepository(self)
    
    @property
    def users(self):
        return UsersRepository(self)
    
    @property
    def sources(self):
        return SourcesRepository(self)
