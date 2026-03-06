from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class RobotOptions(BaseModel):
    paths: Optional[List[str]] = Field(default=None, description="Paths where are located tests")
    test: Optional[str] = Field(default=None, description="Test Name To Run")
    task: Optional[str] = Field(default=None, description="Task Name To Run")
    suite: Optional[str] = Field(default=None, description="Suite Name To Run")
    loglevel: LogLevel = Field(default=LogLevel.INFO, description="Log level")
    sync: bool = Field(default=False, description="Synchronous execution")
    dry_run: bool = Field(default=False, description="Dry run execution")
    rpa: bool = Field(default=False, description="RPA execution mode")
    include_tags: Optional[List[str]] = Field(default=None, description="Tags to include")
    exclude_tags: Optional[List[str]] = Field(default=None, description="Tags to exclude")
    variables: Optional[Dict[str, str]] = Field(default=None, description="Variables")
