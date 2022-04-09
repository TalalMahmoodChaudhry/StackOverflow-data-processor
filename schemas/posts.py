import enum
import xml.etree.ElementTree as ET
from datetime import datetime

from pydantic import BaseModel, Field

from constants import DATETIME_FORMAT
from file_operations import get_safe_datetime_item_from_tree


class PostType(str, enum.Enum):
    Question = 1
    Answer = 2


class RawPosts(BaseModel):
    id: int = Field(...)
    post_type_id: PostType = Field(None)
    parent_id: int = Field(None)
    acceptance_answer_id: int = Field(None)
    creation_date: datetime = Field(None)
    score: int = Field(None)
    view_count: int = Field(None)
    body: str = Field(None)
    # Foreign key could be set here to the id of RawUserTable however it is very probable
    # that stream data coming in is unordered in production. For this task I could control
    # this, but I have made the assumption it may be unordered.
    owner_user_id: int = Field(None)
    last_editor_display_name: str = Field(None)
    last_edit_date: datetime = Field(None)
    last_activity_date: datetime = Field(None)
    community_owned_date: datetime = Field(None)
    closed_date: str = Field(None)
    title: str = Field(None)
    tags: str = Field(None)
    answer_count: int = Field(None)
    comment_count: int = Field(None)
    favorite_count: int = Field(None)
    record_insert_date_time: datetime = Field(None)

    class Config:
        orm_mode = True


def get_post_from_xml_tree(xml_tree: ET) -> RawPosts:
    try:
        creation_date = datetime.strptime(xml_tree.get("CreationDate"), DATETIME_FORMAT)
    except ValueError:
        raise Exception("Creation Date is invalid")

    last_edit_date = get_safe_datetime_item_from_tree(xml_tree, "LastEditDate")
    last_activity_date = get_safe_datetime_item_from_tree(xml_tree, "LastActivityDate")
    community_owned_date = get_safe_datetime_item_from_tree(xml_tree, "CommunityOwnedDate")

    record_insert_date_time = datetime.utcnow()

    data = {
        "id": xml_tree.get("Id"),
        "post_type_id": xml_tree.get("PostTypeId"),
        "parent_id": xml_tree.get("ParentId"),
        "acceptance_answer_id": xml_tree.get("AcceptedAnswerId"),
        "creation_date": creation_date,
        "score": xml_tree.get("Score"),
        "view_count": xml_tree.get("ViewCount"),
        "body": xml_tree.get("Body"),
        "owner_user_id": xml_tree.get("OwnerUserId"),
        "last_editor_display_name": xml_tree.get("LastEditorDisplayName"),
        "last_edit_date": last_edit_date,
        "last_activity_date": last_activity_date,
        "community_owned_date": community_owned_date,
        "closed_date": xml_tree.get("ClosedDate"),
        "title": xml_tree.get("Title"),
        "tags": xml_tree.get("Tags"),
        "answer_count": xml_tree.get("AnswerCount"),
        "comment_count": xml_tree.get("CommentCount"),
        "favorite_count": xml_tree.get("FavoriteCount"),
        "record_insert_date_time": record_insert_date_time
    }
    return RawPosts(**data)
