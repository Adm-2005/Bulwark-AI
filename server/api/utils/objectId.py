from bson import ObjectId
from pydantic import GetCoreSchemaHandler, ValidationError
from pydantic.json_schema import JsonSchemaValue
from pydantic.types import GetJsonSchemaHandler
from pydantic_core import core_schema

class PydanticObjectId(ObjectId):
    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId: {value}")
        return ObjectId(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "example": "507f1f77bcf86cd799439011"}

def pydantic_objectid_encoder(v: PydanticObjectId) -> str:
    return str(v)