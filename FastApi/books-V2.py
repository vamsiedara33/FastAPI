from fastapi import FastAPI, Body, Path, Query, HTTPException
from typing import Optional

from pydantic import BaseModel, Field
# Pydantics: 
# Pydantics is commonly used as a resource for data validation and how to handle data coming to our FastAPI application.
# Python library that is used for data modeling, data parsing and has efficient error handling.

from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

# validating book data using pydantic model (which comes through post request body)
class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=5) 

    # model_config is used to provide additional configuration options for the Pydantic model.
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A novel set in the Roaring Twenties.",
                "rating": 5
            }
        }
    }



BOOKS = [
    Book(id=1, title="The Great Gatsby", author="F. Scott Fitzgerald", description="A novel set in the Roaring Twenties.", rating=5),
    Book(id=2, title="To Kill a Mockingbird", author="Harper Lee", description="A novel about racial injustice in the Deep South.", rating=5),
    Book(id=3, title="1984", author="George Orwell", description="A dystopian novel about a totalitarian regime.", rating=5),
    Book(id=4, title="Pride and Prejudice", author="Jane Austen", description="A classic romance novel.", rating=4),
    Book(id=5, title="The Catcher in the Rye", author="J.D. Salinger", description="A novel about teenage rebellion and alienation.", rating=4)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

# Get book by id
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(..., description="The ID of the book to retrieve", gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
    # return {"Error": "Book not found"}  

# filter by book rating
@app.get("/books/rating/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(rating: int = Query(description="The rating of the book to filter by", gt=0, lt=6)):
    books_with_rating = [book for book in BOOKS if book.rating == rating]
    if books_with_rating:
        return books_with_rating
    return {"Error": "No books found with this rating"}

# create book using post request
@app.post('/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book created successfully", "book": book_request}

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = max([b.id for b in BOOKS]) + 1
    else:
        book.id = 1
    return book

# update book using put request
@app.put("/books/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_request: BookRequest, book_id: int = Path(gt=0)):
    book_changed = False
    for book in BOOKS:
        if book.id == book_id:
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
            book_changed = True
            return {"message": "Book updated successfully", "book": book}
    # return {"Error": "Book not found"}
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")

# delete book using delete request
@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(description="The ID of the book to delete", gt=0)):
    book_found = False
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            book_found = True
            return {"message": "Book deleted successfully"}
    if not book_found:
        raise HTTPException(status_code=404, detail="Book not found")
    # return {"Error": "Book not found"}

