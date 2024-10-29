from typing import Optional, List
from pydantic import BaseModel, Field


class PageSchema(BaseModel):
    name: Optional[str] = Field(
        None, description="Отображаемое пользователю название пункта"
    )
    id: Optional[str] = Field(
        None, description="Идентификатор пункта в выпадающем списке"
    )
    link: Optional[str] = Field(
        None, description="Номер телефона, указанный в кнопке WhatsApp"
    )


class ServiceParamsSchema(BaseModel):
    waba: Optional[bool] = Field(
        None, description="Является ли источник белым WhatsApp"
    )


class ServiceSchema(BaseModel):
    type: Optional[str] = Field(
        None, description="Тип сервиса, поддерживается только whatsapp"
    )
    params: Optional[ServiceParamsSchema] = Field(
        None, description="Настройки источника"
    )
    pages: Optional[List[PageSchema]] = Field(
        None, description="Список элементов для настройки CRM Plugin"
    )


class SourceSchema(BaseModel):
    id: int = Field(..., description="ID источника")
    name: str = Field(..., description="Название источника")
    pipeline_id: int = Field(..., description="ID воронки, может быть архивной")
    external_id: Optional[str] = Field(
        None, description="Внешний идентификатор источника на стороне интеграции"
    )
    default: Optional[bool] = Field(
        None, description="Является ли источником по-умолчанию"
    )
    origin_code: Optional[str] = Field(
        None, description="Код основного канала источника"
    )
    services: Optional[List[ServiceSchema]] = Field(
        None, description="Массив сервисов, связанных с источником"
    )
