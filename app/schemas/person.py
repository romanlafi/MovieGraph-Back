from pydantic import BaseModel

class PersonBase(BaseModel):
    name: str

class PersonResponse(PersonBase):
    person_id: str

def person_node_to_response(node) -> PersonResponse:
    return PersonResponse(
        person_id=node.get("person_id"),
        name=node.get("name"),
    )