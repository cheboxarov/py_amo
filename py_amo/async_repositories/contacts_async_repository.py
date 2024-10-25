from py_amo.schemas import ContactSchema
from py_amo.async_repositories import BaseAsyncRepository
from httpx import AsyncClient


class ContactsAsyncRepository(BaseAsyncRepository[ContactSchema]):

    REPOSITORY_PATH = "/api/v4/contacts"
    ENTITY_TYPE = "contacts"
    SCHEMA_CLASS = ContactSchema
    SCHEMA_INPUT_CLASS = ContactSchema

    async def count(self):
        params = {
            'only_count': 'Y',
            'skip_filter': 'Y',
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9',
            'dnt': '1',
            'priority': 'u=1, i',
            'referer': f'https://{self.subdomain}.amocrm.ru/contacts/list/contacts/?skip_filter=Y',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        front_session: AsyncClient = self.session
        headers["Authorization"] = front_session.headers.get("Authorization")
        front_session.headers.update(headers=headers)
        response = await front_session.post(f"https://{self.subdomain}.amocrm.ru/ajax/contacts/list/contacts/", params=params)
        response.raise_for_status()
        return response.json().get("count")