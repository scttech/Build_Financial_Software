from pydantic import BaseModel, Field

class AchFile(BaseModel):
    file_id: str = Field(examples=["1", "2"],
                         title="ACH File ID",
                         description="The ACH file ID used to identify the file in the system",
                         pattern=r"^[a-z0-9_]+$")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "file_id": "1"
                },
                {
                    "file_id": "2"
                }
            ]
        }
    }
