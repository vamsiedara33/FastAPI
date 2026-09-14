from fastapi import FastAPI, Body
# https://fastapi.tiangolo.com/tutorial/first-steps/

app = FastAPI()

BOOKS = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "category": "Fiction"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "category": "Fiction"},
    {"id": 3, "title": "1984", "author": "George Orwell", "year": 1949, "category": "Dystopian Fiction"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813, "category": "Romance"},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951, "category": "Fiction"}
]
#  ----------------------------------------------------------------------------------------------------------------------------

# Path parameters : 

# i) Static path parameters:
# Static path parameters are fixed values in the URL path. They are defined in the route path
# Ex: @app.get("/books"), @app.get("/category")

# ii) Dynamic path parameters:
# Path parameters are used to capture values from the URL path. They are defined in the route path using curly braces {}. For example, in the route /books/{book_id}, book_id is a path parameter that can be accessed in the function.
# @app.get("/books/{book_id}"), @app.get("/books/{book_id}/reviews"), etc.

# Note:
# Always define static path parameters before dynamic path parameters in the route path.
# i) order of path parameters matters. If you have multiple path parameters, they should be defined in the order they appear in the URL path. For example, if you have a route /books/{book_id}/reviews/{review_id}, the function signature should be defined as follows: async def read_book_review(book_id: int, review_id: int):
# ii) Path parameters are always strings by default. If you want to specify a different data type for a path parameter, you can use type hints in the function signature. For example, if you want to specify that book_id should be an integer, you can define the route as follows:
# @app.get("/books/{book_id}")
# iii) Path parameters are always required and cannot be optional. If a path parameter is not provided in the URL, FastAPI will return a 404 error.

# --------****************************************  Get ******************************************************----------

# static path parameters
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Books API!"}

@app.get("/books")
async def read_all_books():
    return BOOKS

# Dynamic path parameters
# @app.get("/books/{book_id}")
# async def read_book(book_id: int):   # Type hint ensures book_id is an integer, by default path parameters are strings, so we need to convert it to int
#     for book in BOOKS:
#         if book["id"] == book_id:
#             return book
#     return {"error": "Book not found"}

@app.get("/books/{category}")
async def read_books_by_category(category: str):
    books_in_category = [book for book in BOOKS if book["category"].lower() == category.lower()]
    if books_in_category:
        return books_in_category
    return {"error": "No books found in this category"}

# @app.get("/books/{book_id}/reviews")
# @app.get("/books/{book_id}/{review_id}")

#  ----------------------------------------------------------------------------------------------------------------------------


# Query parameters:
# Query Parameters are request parameters that have been attached after “?”
# Query Parameters have name=value pairs
# Ex: 127.0.0.1:8000/books/?category=math   (?category=math is the query parameter)

# Query parameters are optional parameters that can be included in the URL after the path.
#  They are defined in the function signature using the query parameter name and type hint. 
# For example, in the route "/books?author=Harper+Lee", author is a query parameter that can be accessed in the function.

@app.get("/book/") # http://127.0.0.1:8000/book/?category=fiction
async def read_books_by_category_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").lower() == category.lower():
            books_to_return.append(book)
    if books_to_return:
        return books_to_return
    return {"error": "No books found in this category"}

#  ----------------------------------------------------------------------------------------------------------------------------

# --------****************************************  Post ******************************************************----------
@app.post("/books/create_book")
async def create_book(new_book=Body()): # Request body
    BOOKS.append(new_book) 
    return {"message": "Book created successfully", "book": new_book}


# --------****************************************  put ******************************************************----------
@app.put("/books/update_book/{book_id}")
async def update_book(book_id: int, updated_book=Body()):
    for index, book in enumerate(BOOKS):
        if book["id"] == book_id:
            BOOKS[index] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}
    return {"error": "Book not found"}

# --------**************************************** delete ******************************************************----------
@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(BOOKS):
        if book["id"] == book_id:
            deleted_book = BOOKS.pop(index)
            return {"message": "Book deleted successfully", "book": deleted_book}
    return {"error": "Book not found"}

# To Run FastAPI on a Custom Port:

# > uvicorn books:app --port 3000
# or 
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, port=10000)