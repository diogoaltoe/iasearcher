from typing import Any, Dict
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class Wikipedia(BaseModel):
    url: str = Field(description="wikipedia url")

    def to_dict(self) -> Dict[str, Any]:
        return {"url": self.url}


wikipedia_parser = PydanticOutputParser(pydantic_object=Wikipedia)
