from typing import Annotated

from pydantic import BaseModel, StringConstraints


class BankRoutingNumbersSchema(BaseModel):
    routing_number: Annotated[str, StringConstraints(min_length=9, max_length=9)]
    bank_name: str
