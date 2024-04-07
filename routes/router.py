from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId
from model.books import Books
from model.students import Students 
from config.dbconfig import client

book = APIRouter()
student = APIRouter()
db = client["librarysystem"]
books_collection = db["books"]
students_collection = db["students"]

@book.post("/books", status_code=201)
async def create_book(book : Books):
    result = books_collection.insert_one(book.dict())
    
    if result.inserted_id:
        book_data = book.dict()
        bookId = str(result.inserted_id)
        book_data["id"] = bookId
        return book_data
    else:
        raise HTTPException(status_code=500, detail="Failed to insert book")
    
@book.get("/books", status_code=200)
async def list_books(available: bool = Query(None), year: int = Query(None)):
    query = {}
    if available:
        query["available"] = available
    if year:
        query["year"] = {"$gte": year}

    books = list(books_collection.find(query))
    docs = []
    for item in books :
        docs.append({
            "id" : str(item["_id"]),
            "title" : item["title"],
            "author" : item["author"],
            "year" : item["year"],
            "available" : item["available"]
        })
    return docs

@book.get("/books/{id}", status_code=200)
async def get_book(id : str):
    book = books_collection.find_one({"_id" : ObjectId(id)})
    
    if book:
        book["_id"] = str(book["_id"])
        return book
    else:
        raise HTTPException(status_code=404, detail="book did not found")
    
@book.patch("/books/{id}", status_code=204)
async def update_book(id : str, book : Books):
    updated_book = {}
    
    if book.title is not None :
        updated_book["title"] = book.title
    if book.author is not None :
        updated_book["author"] = book.author
    if book.year is not None :
        updated_book["year"] = book.year
    if book.available is not None :
        updated_book["available"] = book.available

    if updated_book :
        result = books_collection.update_one({"_id" : ObjectId(id)}, {"$set" : updated_book})
            
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="book not found")
    
@book.delete("/books/{id}", status_code=200)
async def delete_book(id : str):
    result = books_collection.delete_one({"_id" : ObjectId(id)})
    
    if result.deleted_count == 0 :
        raise HTTPException(status_code=404, detail="book not found")
    else:
        return {"book successfully deleted"}

@student.post("/students", status_code=201)
async def create_student(student: Students):
    result = students_collection.insert_one(student.dict())

    if result.inserted_id:
        student_with_id = student.dict()
        student_id = str(result.inserted_id)
        student_with_id["id"] = student_id
        return student_with_id
    else:
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
        
    if query:
        result = students_collection.update_one({"_id" : ObjectId(id)}, {"$set" : student})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="student not found")
        
    
@student.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    result = students_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="student not found")
    else :
        return {"student information deleted"}
    

        