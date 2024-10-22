from typing import Annotated

from pydantic import BaseModel, Field


class NoteBaseSchema(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    body: Annotated[str, Field(min_length=1, max_length=50000)]
    tags: list[str] | None = None


class NoteCreateSchema(NoteBaseSchema):
    pass


class NoteSchema(NoteBaseSchema):
    id: int


class NotePartialUpdateSchema(NoteBaseSchema):
    title: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    body: Annotated[str, Field(min_length=1, max_length=50000)] | None = None
    tags: list[str] | None = None
