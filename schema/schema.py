# from model.students import Address

def bookEntity(item) -> dict :
    return {
        "id" : str(item["_id"]),
        "title" : item["title"],
        "author" : item["author"],
        "year" : item["year"]
    }

def bookConverter(items) -> list:
    return [bookEntity(item) for item in items]

def Address(item) -> dict :
    return {
        "city" : item["city"],
        "country" : item["country"]
    }
   
def studentsEntity(item) -> dict :
    return {
        "id" : str(item["_id"]),
        "name" : item["name"],
        "age" : item["age"],
        "address" : Address(item["address"])
    }
  
def studentsConverter(items) -> list:
    return [studentsEntity(item) for item in items]  