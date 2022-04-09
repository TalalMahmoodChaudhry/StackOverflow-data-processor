from pydantic import BaseModel, Field


class Errors(BaseModel):
    text: str = Field(None)
    error_message: str = Field(None)

    class Config:
        orm_mode = True


def get_error_from_xml_tree(line: str, error_message: str) -> Errors:
    return Errors(text=line, error_message=error_message)


def is_error(line: str) -> bool:
    if line in ["<users>", "</users>", "<posts>", "</posts>", "<comments>", "</comments>"]:
        return False
    else:
        return True
