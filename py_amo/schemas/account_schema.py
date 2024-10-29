from pydantic import BaseModel, Field
from typing import Optional


class AccountShema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    subdomain: Optional[str] = None
    current_user_id: Optional[int] = None
    country: Optional[str] = None
    customers_mode: Optional[str] = None
    is_unsorted_on: Optional[bool] = None
    is_loss_reason_enabled: Optional[bool] = None
    is_helpbot_enabled: Optional[bool] = None
    is_technical_account: Optional[bool] = None
    contact_name_display_order: Optional[int] = None
    amojo_id: Optional[str] = None
