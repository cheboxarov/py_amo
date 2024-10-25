import requests
from .account_manage import AccountManager
import httpx
from py_amo.repositories import PipelinesRepository, LeadsRepository, ContactsRepository, UsersRepository, SourcesRepository, PipelineStatusesRepository
from py_amo.async_repositories import PipelinesAsyncRepository, LeadsAsyncRepository, ContactsAsyncRepository, UsersAsyncRepository, SourcesAsyncRepository, PipelineStatusesAsyncRepository


class BaseAmoSession(AccountManager):

    def __init__(self, token: str, subdomain: str):
        self.token = token
        self.subdomain = subdomain

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }
    
    def get_url(self):
        return f"https://{self.subdomain}.amocrm.ru"
    
    def get_subdomain(self):
        return self.subdomain
    


class AmoSession(BaseAmoSession):

    def get_requests_session(self):
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })
        return session
    
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
    
    def pipeline_statuses(self, pipeline_id: int):
        return PipelineStatusesRepository(pipeline_id, self)

class AsyncAmoSession(BaseAmoSession):

    """
    Будьте аккуратны с асинхронным клиентом! Не забывайте про ограничения кол-ва запросов в секунду со стороны амо!
    """

    def __init__(self, token, subdomain):
        super().__init__(token, subdomain)
        self.async_session = httpx.AsyncClient(headers=self.get_headers())

    def get_async_session(self):
        return self.async_session
    
    @property
    def leads(self):
        return LeadsAsyncRepository(self)
    
    @property
    def contacts(self):
        return ContactsAsyncRepository(self)
    
    @property
    def pipelines(self):
        return PipelinesAsyncRepository(self)
    
    @property
    def users(self):
        return UsersAsyncRepository(self)
    
    @property
    def sources(self):
        return SourcesAsyncRepository(self)
    
    def pipeline_statuses(self, pipeline_id: int):
        return PipelineStatusesAsyncRepository(pipeline_id, self)