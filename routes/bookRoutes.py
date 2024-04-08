from fastapi import APIRouter, Query, HTTPException
from pydantic import ValidationError
from bson import ObjectId
from model.books import Books
from config.dbconfig import client

book = APIRouter()
db = client["librarysystem"]
books_collection = db["books"]


@book.post("/books", status_code=201)
async def create_student(book: Books):
    try:
        result = books_collection.insert_one(book.dict())
        if result.inserted_id:
            student_with_id = book.dict()
            student_id = str(result.inserted_id)
            student_with_id["id"] = student_id
            return student_with_id
        else:
            raise HTTPException(status_code=500, detail="Failed to insert student")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@book.get("/books", status_code=200)
async def list_books(available: bool = Query(None)):
    query = {}
    if available is not None:
        query["available"] = available

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
        book_data = {
            "id": str(book["_id"]),
            "title": book["title"],
            "author": book["author"],
            "year": book["year"],
            "available": book["available"]
        }
        return book_data
    else:
        raise HTTPException(status_code=404, detail="book did not found")
    
@book.patch("/books/{id}", status_code=204)
async def update_book(id : str, title : str = Query(None), author : str = Query(None), year : int = Query(None), available : bool = Query(None)):
    query = {}
    book = books_collection.find_one({"_id" : ObjectId(id)})
    
    if title : 
        query["title"] = title
        book["title"] = title
    if author : 
        query["author"] = author
        book["author"] = author
    if year : 
        query["year"] = year
        book["year"] = year
    if available is not None : 
        query["available"] = available
        book["available"] = available
        
    if query:
        result = books_collection.update_one({"_id" : ObjectId(id)}, {"$set" : book})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="No book found")
    
    
@book.delete("/books/{id}", status_code=200)
async def delete_book(id : str):
    book = books_collection.find_one({"_id": ObjectId(id)})
    
    if book:
        book_details = book["title"]
        result = books_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 1:
            return {f"{book_details} deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete student")
    else:
        raise HTTPException(status_code=404, detail="Student not found")
