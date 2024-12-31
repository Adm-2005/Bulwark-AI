import re
import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from fastapi.encoders import jsonable_encoder
from api.utils.objectId import PydanticObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class Severity(str, Enum):
    Low = "low"
    Medium = "medium"
    High = "high"
    Critical = "critical"

class Threat(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    network_id: Optional[PydanticObjectId] = Field(None)
    type: str
    severity: Severity
    description: Optional[str] = Field(default="")
    resolved: bool = Field(default=False)
    detected_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))
    resolved_at: Optional[datetime.datetime] = Field(None)

    def resolve(self):
        self.resolved = True
        self.resolved_at = datetime.datetime.now(tz=datetime.timezone.utc)

    def to_json(self):
        return jsonable_encoder(self, custom_encoder={PydanticObjectId: str})
    
    def to_bson(self):
        data = self.model_dump(by_alias=True)
        if data.get('_id') is None:
            data.pop('_id', None)
        return data

class ConnectionDetails(BaseModel):
    ip_address: str
    token: Optional[str]
    credentials: Optional[dict]

class LogEntry(BaseModel):
    timestamp: datetime.datetime
    level: str
    message: str

class Network(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    slug: str
    user_id: Optional[PydanticObjectId] = Field(None)
    name: str = Field(default="")
    description: Optional[str] = Field(default="")
    connection_details: ConnectionDetails
    connected: bool = Field(default=False)
    logs: Optional[List[LogEntry]] = Field(default_factory=list)
    threats: Optional[List[PydanticObjectId]] = Field(default_factory=list)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))

    def generate_slug(self, collection):
        cleaned_name = re.sub(r'[^a-zA-Z0-9\s-]', '', self.name)
        base_slug = cleaned_name.lower().replace(" ", "-").strip("-")

        unique_slug = base_slug
        counter = 1 
    
        while collection.find_one({ "slug": unique_slug }):
            unique_slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = unique_slug

    def update_timestamp(self):
        self.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)

    def to_json(self):
        return jsonable_encoder(self, custom_encoder={PydanticObjectId: str})
    
    def to_bson(self):
        data = self.model_dump(by_alias=True)
        if data.get('_id') is None:
            data.pop('_id', None)
        return data

class User(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    full_name: str 
    username: str
    email: EmailStr
    hashed_password: Optional[str] = Field(None)
    networks: Optional[List[PydanticObjectId]] = Field(default_factory=list) 

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        if not self.hashed_password:
            raise ValueError("Password is not set.")
        return check_password_hash(self.hashed_password, password)
    
    def to_json(self, exclude_password=True):
        user_data = jsonable_encoder(
            self,
            custom_encoder={PydanticObjectId: str}, 
        )
        if exclude_password:
            user_data.pop('hashed_password', None)
        return user_data

    def to_bson(self):
        data = self.model_dump(by_alias=True)
        if data.get('_id') is None:
            data.pop('_id', None)
        return data