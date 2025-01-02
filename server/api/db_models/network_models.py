# external imports
import re
import datetime
from enum import Enum
from pydantic import Field
from typing import Optional, List, Dict

# internal imports
from api.utils.object_id import PydanticObjectId
from server.api.db_models.base_models import Serialization, Collection

# enumerate classes
class Severity(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    critical = 'critical'

# model classes
class Threat(Serialization):
    """Represents a detected threat."""
    id: Optional[PydanticObjectId] = Field(default = None, alias = '_id')
    network_id: Optional[PydanticObjectId] = Field(default = None)
    type: str
    severity: Severity
    description: Optional[str] = Field(default = '')
    resolved: bool = Field(default = False)
    detected_at: datetime.datetime = Field(default_factory = lambda: datetime.datetime.now(tz = datetime.timezone.utc))
    resolved_at: Optional[datetime.datetime] = Field(default = None)

    def resolve(self):
        """Marks a threat resolved."""
        self.resolved = True
        self.resolved_at = datetime.datetime.now(tz = datetime.timezone.utc)

class ConnectionDetails(Serialization):
    """Represents connection details/credentials for a network."""
    id: Optional[PydanticObjectId] = Field(default = None, alias = '_id')
    ip_address: str
    token: Optional[str]
    credentials: Optional[dict]

class LogEntry(Serialization, Collection):
    """Represents a network log received and processed by the system."""
    id: Optional[PydanticObjectId] = Field(default = None, alias = '_id')
    level: str
    message: str
    timestamp: datetime.datetime

class Network(Serialization, Collection):
    """Represents a network registered by the user."""
    id: Optional[PydanticObjectId] = Field(default = None, alias = '_id')
    name: str = Field(default = '')
    user_id: Optional[PydanticObjectId] = Field(default = None)
    description: Optional[str] = Field(default = '')
    connected: bool = Field(default = False)
    logs: Optional[List[PydanticObjectId]] = Field(default_factory = list)
    connection_details: Optional[PydanticObjectId] = Field(default = None)
    threats: Optional[List[PydanticObjectId]] = Field(default_factory = list)
    created_at: datetime.datetime = Field(default_factory = lambda: datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory = lambda: datetime.datetime.now(tz=datetime.timezone.utc))