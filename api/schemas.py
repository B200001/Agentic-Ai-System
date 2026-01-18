from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class RunTaskRequest(BaseModel):
    goal: str

class RunTaskResponse(BaseModel):
    goal: str
    plan: Dict[str, Any]
    final_output: str
    logs: List[str]
    memory_used: Optional[bool] = False
