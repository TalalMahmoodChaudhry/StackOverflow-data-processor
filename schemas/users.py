import xml.etree.ElementTree as ET
from datetime import datetime

from pydantic import BaseModel, Field, condecimal

from file_operations import get_safe_datetime_item_from_tree


class Users(BaseModel):
    id: int = Field(...)
    account_id: int = Field(None)
    display_name: str = Field(None)
    reputation: int = Field(None)
    creation_date: datetime = Field(None)
    last_access_date: datetime = Field(None)
    website_url: str = Field(None)
    location: str = Field(None)
    about_me: str = Field(None)
    views: int = Field(None)
    up_votes: int = Field(None)
    down_votes: int = Field(None)
    total_posts: int = Field(None)
    avg_monthly_comments: condecimal() = Field(None)

    class Config:
        orm_mode = True


def get_user_from_xml_tree(xml_tree: ET) -> Users:
    try:
        creation_date = datetime.strptime(xml_tree.get("CreationDate"), "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        raise Exception("Creation Date is invalid")

    last_access_date = get_safe_datetime_item_from_tree(xml_tree, "LastEditDate")

    record_insert_date_time = datetime.utcnow()

    user_data = {
        "id": xml_tree.get("Id"),
        "reputation": xml_tree.get("Reputation"),
        "creation_date": creation_date,
        "display_name": xml_tree.get("DisplayName"),
        "last_access_date": last_access_date,
        "website_url": xml_tree.get("WebsiteUrl"),
        "location": xml_tree.get("Location"),
        "about_me": xml_tree.get("AboutMe"),
        "views": xml_tree.get("Views"),
        "up_votes": xml_tree.get("UpVotes"),
        "down_votes": xml_tree.get("DownVotes"),
        "account_id": xml_tree.get("AccountId"),
        "record_insert_date_time": record_insert_date_time
    }
    return Users(**user_data)
