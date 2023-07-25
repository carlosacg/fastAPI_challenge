from fastapi import APIRouter, Depends
from models import People
from dependencies import get_token_header
from database import conn
from typing import List

router = APIRouter(
    prefix="/people",
    tags=["people"],
    dependencies=[Depends(get_token_header)],
)


@router.get("/")
async def get_people():
    """
    Get all people from the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    people = cursor.fetchall()
    cursor.close()

    return people


@router.get("/{id}")
async def get_people_by_id(id: int):
    """
    Get a person by their ID from the database.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM people WHERE id='{id}'")
    people = cursor.fetchone()
    cursor.close()

    return people


@router.post("/", response_model=People)
async def create_people(people: People):
    """
    Create a new person and add them to the database.
    """
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO people (name, age) VALUES (%s, %s)", (people.name, people.age)
    )
    conn.commit()
    cursor.close()

    return people


@router.put("/{id}", response_model=People)
async def update_people(id: int, people: People):
    """
    Update a person's data in the database by their ID.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE people SET name=%s, age=%s WHERE id=%s", (people.name, people.age, id)
    )
    conn.commit()
    cursor.close()

    return people


@router.delete("/{id}", status_code=204)
async def delete_people(id: int):
    """
    Delete a person from the database by their ID.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM people WHERE id=%s", (id,))
    conn.commit()
    cursor.close()

    return {"message": "Person deleted successfully"}
