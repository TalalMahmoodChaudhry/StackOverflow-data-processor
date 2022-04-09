import xml.etree.ElementTree as ET
from datetime import datetime

from pydantic import BaseModel, Field

from constants import DATETIME_FORMAT


class RawComments(BaseModel):
    id: int = Field(...)
    post_id: int = Field(None)
    creation_date: datetime = Field(None)
    score: int = Field(None)
    text: str = Field(None)
    # Foreign key could be set here to the id of RawUserTable however it is very probable
    # that stream data coming in is unordered in production. For this task I could control
    # this, but I have made the assumption it may be unordered.
    user_id: int = Field(None)
    record_insert_date_time: datetime = Field(None)

    class Config:
        orm_mode = True


def get_comment_from_xml_tree(xml_tree: ET) -> RawComments:
    try:
        creation_date = datetime.strptime(xml_tree.get("CreationDate"), DATETIME_FORMAT)
    except ValueError:
        raise Exception("Creation Date is invalid")

    record_insert_date_time = datetime.utcnow()

    data = {
        "id": xml_tree.get("Id"),
        "post_id": xml_tree.get("PostId"),
        "creation_date": creation_date,
        "score": xml_tree.get("Score"),
        "text": xml_tree.get("Text"),
        "user_id": xml_tree.get("UserId"),
        "record_insert_date_time": record_insert_date_time
    }
    return RawComments(**data)
