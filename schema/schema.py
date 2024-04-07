
def bookEntity(item) -> dict :
    return {
        "id" : str(item["_id"]),
        "title" : item["title"],
        "author" : item["author"],
        "year" : item["year"],
        "available" : item["available"]
    }


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
   