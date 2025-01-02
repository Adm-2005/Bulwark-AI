# external imports
import datetime
from enum import Enum
from typing import Optional, List
from pydantic import EmailStr, Field
from fastapi.encoders import jsonable_encoder
from werkzeug.security import generate_password_hash, check_password_hash

# internal imports
from api.utils.object_id import PydanticObjectId
from server.api.db_models.base_models import Serialization

# model classes
class User(Serialization):
    """Represents users of the application."""
    id: Optional[PydanticObjectId] = Field(default = None, alias = '_id')
    first_name: Optional[str] = Field(default = None)
    last_name: Optional[str] = Field(default = None) 
    username: str
    email: EmailStr
    hashed_password: Optional[str] = Field(default = None)
    networks: Optional[List[PydanticObjectId]] = Field(default_factory = list) 
    joined_at: datetime.datetime = Field(default_factory = lambda: datetime.datetime.now(tz = datetime.timezone.utc))

    def set_password(self, password: str) -> None:
        """
        Hashes given password. Should be called when creating or updating user.

        Args
            password: password to be hashed
        """
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Validates given password using hashed password.

        Args
            password: password to be validated

        Returns
            [bool]: True if password is correct
        """
        if not self.hashed_password:
            raise ValueError("Password is not set.")
        
        return check_password_hash(self.hashed_password, password)
    
    def to_json(self):
        """Overrides Serialization model's to_json method to prevent password exposure."""
        data = jsonable_encoder(self, custom_encoder = {PydanticObjectId: str})
        data.pop('hashed_password', None)
        return data