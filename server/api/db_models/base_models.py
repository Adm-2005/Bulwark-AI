# external imports
import re
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from fastapi.encoders import jsonable_encoder

# internal imports
from api.utils.object_id import PydanticObjectId

class Serialization(BaseModel):
    """Base serialization model inherited by other models."""

    def to_json(self) -> Dict[str, Any]:
        """Returns a json-like representation of the object."""
        return jsonable_encoder(self, custom_encoder = {PydanticObjectId: str})
    
    def to_bson(self) -> Dict[str, Any]:
        """Returns a bson-like representation of the object."""
        data = self.model_dump(by_alias = True)

        if data.get('_id') is None:
            data.pop('_id', None)

        return data
    
class Collection(BaseModel):
    """Base model to be inherited by models that have many-to-one relationship with user."""
    slug: Optional[str] = Field(default = '')

    def generate_slug(self, collection):
        cleaned_name = re.sub(r'[^a-zA-Z0-9\s-]', '', self.name)
        base_slug = cleaned_name.lower().replace(' ', '-').strip('-')

        unique_slug = base_slug
        counter = 1 
    
        while collection.find_one({ 'slug': unique_slug }):
            unique_slug = f'{base_slug}-{counter}'
            counter += 1

        self.slug = unique_slug