from py_amo.schemas import PipelineSchema
from .base_async_repository import BaseAsyncRepository
from httpx import AsyncClient
from py_amo.utils import repository_safe_request
import asyncio


class PipelinesAsyncRepository(BaseAsyncRepository[PipelineSchema]):

    REPOSITORY_PATH = "/api/v4/leads/pipelines"
    ENTITY_TYPE = "pipelines"
    SCHEMA_CLASS = PipelineSchema
    SCHEMA_INPUT_CLASS = PipelineSchema

    async def get_all_leads_count(self):
        pipelines = await self.get_all()
        semaphore = asyncio.Semaphore(5)
        result = await asyncio.gather(
            *(
                repository_safe_request(self.get_leads_count, semaphore, i, pipeline.id)
                for i, pipeline in enumerate(pipelines)
            )
        )
        return sum(result)

    async def get_leads_count(self, pipeline_id: int):
        print(pipeline_id)
        pipeline = await self.get_by_id(pipeline_id)
        data = {
            "leads_by_status": "Y",
            "skip_filter": "Y",
            f"filter[pipe][{pipeline_id}][]": [
                str(status.id) for status in pipeline.statuses
            ],
        }
        headers = {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": f"https://{self.subdomain}.amocrm.ru",
            "priority": "u=1, i",
            "referer": f"https://{self.subdomain}.amocrm.ru/leads/pipeline/{pipeline_id}/?skip_filter=Y",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        front_session: AsyncClient = self.session
        headers["Authorization"] = front_session.headers.get("Authorization")
        front_session.headers.update(headers=headers)
        response = await front_session.post(
            f"https://{self.subdomain}.amocrm.ru/ajax/leads/sum/{pipeline_id}/",
            data=data,
        )
        response.raise_for_status()
        return response.json().get("all_count")
