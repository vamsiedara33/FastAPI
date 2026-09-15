# Books API

A simple RESTful API for managing a book collections.

## Endpoints

Base path: `/api/books`

| Method | Endpoint          | Description                          |
|--------|-------------------|---------------------------------------|
| GET    | `/api/books`      | Get all books (supports filters)      |
| GET    | `/api/books/:id`  | Get a single book by id               |
| POST   | `/api/books`      | Create a new book                     |
| PUT    | `/api/books/:id`  | Update a book (full or partial)       |
| DELETE | `/api/books/:id`  | Delete a book                         |

### Query filters (GET /api/books)
- `?author=tolkien` — filter by author (partial, case-insensitive)
- `?genre=fantasy` — filter by genre (partial, case-insensitive)

### Book object shape

```json
{
  "id": 1,
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "year": 1937,
  "genre": "Fantasy"
}
```

`title` and `author` are required on create. `year` and `genre` are optional.

## Example requests (curl)

**Get all books**
```bash
curl http://localhost:3000/api/books
```

**Get one book**
```bash
curl http://localhost:3000/api/books/1
```

**Create a book**
```bash
curl -X POST http://localhost:3000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953, "genre": "Dystopian"}'
```

**Update a book**
```bash
curl -X PUT http://localhost:3000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"year": 1938}'
```

**Delete a book**
```bash
curl -X DELETE http://localhost:3000/api/books/1
```

