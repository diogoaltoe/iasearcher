from typing import Any, Dict, List
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class Summary(BaseModel):
    summary: str = Field(description="summary")
    flag: str = Field(description="flag url")
    facts: List[str] = Field(description="interesting facts about it")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "flag": self.flag, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
