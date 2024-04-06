from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId
from model.books import Books
from model.students import Students 
from model.students import Address
from config.dbconfig import client
from schema.schema import studentsEntity, studentsConverter, bookConverter, bookEntity

book = APIRouter()
student = APIRouter()
db = client["librarysystem"]
books_collection = db["books"]
students_collection = db["students"]

@student.post("/students", status_code=201)
async def create_student(student: Students):
    result = students_collection.insert_one(student.dict())

    # Ensure insertion was successful
    if result.inserted_id:
        # Return the ID of the inserted document
        return studentsEntity(result)
    else:
        # Handle insertion failure
        raise HTTPException(status_code=500, detail="Failed to insert student")

@student.get("/students", status_code=200)
async def list_students(country: str = Query(None), age: int = Query(None)):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    students = list(students_collection.find(query))
    docs = []
    for item in students :
        docs.append({
            "id" : str(item["_id"]),
            "name" : item["name"],
            "age" : item["age"],
            "address" : item["address"]
        })
    return docs

@student.get("/students/{id}", status_code=200)
async def get_student(id: str):
    student = students_collection.find_one({"_id" : ObjectId(id)})
    if student:
        student["_id"] = str(student["_id"])
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    

@student.patch("/students/{id}", status_code=204)
async def update_student(id : str, student : Students):
    update_data = {}
    if student.name is not None:
        update_data["name"] = student.name
    if student.age is not None:
        update_data["age"] = student.age
    if student.address is not None:
        update_data["address"] = student.address.dict()

    result = students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    
@student.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    result = students_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="student not found")
    else :
        return {"student information deleted"}