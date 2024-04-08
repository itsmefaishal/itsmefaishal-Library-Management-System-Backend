from fastapi import APIRouter, Query, HTTPException
from pydantic import ValidationError
from bson import ObjectId
from model.students import Students 
from config.dbconfig import client


student = APIRouter()

db = client["librarysystem"]

students_collection = db["students"]

@student.post("/students", status_code=201)
async def create_student(student: Students):
    try:
        result = students_collection.insert_one(student.dict())
        if result.inserted_id:
            student_with_id = student.dict()
            student_id = str(result.inserted_id)
            student_with_id["id"] = student_id
            return student_with_id
        else:
            raise HTTPException(status_code=500, detail="Failed to insert student")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@student.get("/students", status_code=200)
async def list_students(country: str = Query(None), age: int = Query(None)):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    
    print("Constructed Query:", query)  

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
        student_data = {
            "id": str(student["_id"]),
            "name": student["name"],
            "age": student["age"],
            "address" : {
                "city": student["address"]["city"],
                "country": student["address"]["country"]
            }
        }
        return student_data
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
        
@student.patch("/students/{id}", status_code=204)
async def update_student(id : str, name : str = Query(None), age : int = Query(None), city : str = Query(None), country : str = Query(None)):
    query = {}
    student = students_collection.find_one({"_id" : ObjectId(id)})
    
    if name : 
        query["name"] = name
        student["name"] = name
    if age :
        query["age"] = age
        student["age"] = age
    if city or country:
        new_address = {}
        
        if city :
            new_address["city"] = city
            
        if country :
            new_address["country"] = country
        
        student["address"] = new_address
        query["address"] = new_address
        
    if query:
        
        result = students_collection.update_one({"_id" : ObjectId(id)}, {"$set" : student}) 
              
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="student not found")
        
    
@student.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    student = students_collection.find_one({"_id": ObjectId(id)})
    
    if student:
        student_details = student["name"]
        result = students_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 1:
            return {f"{student_details} deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete student")
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    

        