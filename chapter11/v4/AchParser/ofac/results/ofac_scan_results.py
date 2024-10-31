from decimal import Decimal

from pydantic import BaseModel, UUID4, Field


class OfacScanResults(BaseModel):
    id: int = Field(title="ID", description="The ID of the result")
    ach_files_id: UUID4 = Field(title="ACH Files ID", description="The ACH Files ID")
    ach_batch_id: UUID4 = Field(title="ACH Batch ID", description="The ACH Batch ID")
    sdn_name: str = Field(title="SDN Name", description="The SDN Name")
    individual_name: str = Field(
        title="Individual Name", description="The Individual Name"
    )
    alias: str = Field(title="Alias", description="The Alias from the SDN List")
    similarity_score: Decimal = Field(
        title="Similarity Score", description="The Similarity Score"
    )
    daitch_mokotoff_match_name: bool = Field(
        title="Daitch Mokotoff Match Name", description="Daitch Mokotoff Match Name"
    )
    daitch_mokotoff_match_alias: bool = Field(
        title="Daitch Mokotoff Match Alias", description="Daitch Mokotoff Match Alias"
    )
