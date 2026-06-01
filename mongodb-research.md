# Introduction to MongoDB

Welcome to this guide on MongoDB! Whether you have never heard of it before or just want a solid refresher, this document will walk you through everything you need to know - from what MongoDB actually is, to creating databases, adding documents, and keeping your data clean with validation.

---

## 1. What is MongoDB?

MongoDB is a **NoSQL document database**. Unlike traditional SQL databases that store data in rigid rows and columns (think Excel spreadsheets), MongoDB stores data as flexible **JSON-like documents**.

Each document can have its own structure, meaning you are not locked into a fixed template for every entry. This makes MongoDB incredibly flexible and developer-friendly.

```json
{
  "name": "Sakib",
  "age": 23,
  "city": "London"
}
```

---

## 2. Advantages and Disadvantages of MongoDB

### ✅ Advantages

- **Flexible schema** - documents do not all need to have the same fields
- **Scales easily** - built to handle large amounts of data across multiple servers
- **Fast development** - data is stored as JSON, which most web apps already use
- **Great for unstructured data** - perfect when your data does not fit neatly into tables

### ❌ Disadvantages

- **No joins** - unlike SQL, MongoDB does not support traditional table joins
- **Higher memory usage** - storing data as documents can use more storage than SQL
- **Not ideal for complex transactions** - SQL databases are still better for things like banking systems that need strict data integrity

---

## 3. Common Use Cases for MongoDB

MongoDB is used across a huge range of industries. Here are some of the most common:

- 🛒 **E-commerce** - storing product catalogues where each product has different attributes
- 💬 **Social media** - user profiles, posts, comments, and likes
- 📰 **Content management** - blogs, news platforms, and media sites
- 📡 **IoT (Internet of Things)** - storing real-time data from sensors and devices
- 🎮 **Gaming** - player profiles, scores, and game state

---

## 4. Connecting to MongoDB Locally Using Compass

MongoDB Compass is the official GUI for MongoDB - it lets you visually browse and manage your databases without writing any code.

**Steps to connect:**

1. Open **MongoDB Compass**
2. In the URI field, enter:
mongodb://localhost:27017
3. Click **Save & Connect**

Once connected, you will see your local databases listed in the left sidebar - `admin`, `config`, and `local` are the defaults that come with every MongoDB installation.

---

## 5. Creating a New Database

You can create a new database directly in Mongosh (the MongoDB shell inside Compass).

```js
use sparta
```

This switches to a database called `sparta`. If it does not exist yet, MongoDB will create it automatically once you add data to it.

---

## 6. Creating a New Collection

A **collection** is like a table in SQL - it groups related documents together.

```js
db.createCollection("institute")
```

You should see:
```js
{ ok: 1 }
```

---

## 7. Adding Documents

### Adding a Single Document

```js
db.institute.insertOne({
  name: "Sakib",
  course: "Data Science",
  age: 23
})
```

### Adding Multiple Documents

```js
db.institute.insertMany([
  { name: "Alice", course: "Software Engineering", age: 22 },
  { name: "Bob", course: "Cybersecurity", age: 25 },
  { name: "Charlie", course: "Data Science", age: 24 }
])
```

---

## 8. Validation

Validation allows you to enforce rules on the documents being inserted into a collection - so bad data gets rejected before it ever enters your database.

### Creating a Collection with Validation

```js
db.createCollection("students", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "age", "course"],
      properties: {
        name: {
          bsonType: "string",
          description: "Must be a string and is required"
        },
        age: {
          bsonType: "int",
          minimum: 16,
          description: "Must be an integer of at least 16"
        },
        course: {
          bsonType: "string",
          description: "Must be a string and is required"
        }
      }
    }
  }
})
```

### Invalid Entry (will be rejected ❌)

```js
db.students.insertOne({
  name: "Invalid Student",
  age: "twenty",
  course: "Data Science"
})
```

### Valid Entry (will be accepted ✅)

```js
db.students.insertOne({
  name: "Sakib",
  age: 23,
  course: "Data Science"
})
```

---

## 9. Searching for Documents

```js
// Find all documents
db.students.find()

// Find a specific document
db.students.find({ name: "Sakib" })

// Find with a condition
db.students.find({ age: { $gte: 20 } })
```

---

## 10. Films Collection - Practice

```js
db.createCollection("films", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "genre", "year", "rating"],
      properties: {
        title: { bsonType: "string" },
        genre: { bsonType: "string" },
        year: { bsonType: "int", minimum: 1888 },
        rating: { bsonType: "number", minimum: 0, maximum: 10 }
      }
    }
  }
})
```

### Insert 5 Films

```js
db.films.insertMany([
  { title: "Inception", genre: "Sci-Fi", year: 2010, rating: 8.8 },
  { title: "The Dark Knight", genre: "Action", year: 2008, rating: 9.0 },
  { title: "Interstellar", genre: "Sci-Fi", year: 2014, rating: 8.6 },
  { title: "Parasite", genre: "Thriller", year: 2019, rating: 8.5 },
  { title: "The Godfather", genre: "Crime", year: 1972, rating: 9.2 }
])
```

### Updating a Document

```js
db.films.updateOne(
  { title: "Inception" },
  { $set: { rating: 9.0 } }
)
```

### Updating Multiple Documents

```js
db.films.updateMany(
  { genre: "Sci-Fi" },
  { $set: { available: true } }
)
```

### Deleting a Document

```js
db.films.deleteOne({ title: "Parasite" })
```

---

## 11. Embedding vs Referencing

### Embedding

Embedding means storing related data **inside** the same document.

```json
{
  "name": "Sakib",
  "address": {
    "street": "123 High Road",
    "city": "London",
    "postcode": "IG1 1AA"
  }
}
```

**When to use it:**
- The related data is always accessed together
- The nested data does not change frequently
- You want fast reads

### Referencing

Referencing means storing related data in a **separate document** and linking them by ID.

```json
{
  "_id": "ORD-001",
  "customerId": "CUST-100",
  "product": "Blender"
}
```

**When to use it:**
- The related data is large or changes frequently
- The same data is referenced by many documents
- You want to avoid data duplication

---