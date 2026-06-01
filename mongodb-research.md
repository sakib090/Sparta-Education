# MongoDB Research

## What is MongoDB?

- A NoSQL document database
- Stores data as JSON-like documents

## Types of NoSQL Databases

- **Document databases** = store data as documents, similar to JSON files. Each document can have its own structure. MongoDB is an example of this.
- **Key-Value databases** = the simplest type. Data is stored as a key (like a label) and a value (the actual data). Think of it like a dictionary. Redis is an example.
- **Column-family databases** = store data in columns rather than rows, which makes reading large amounts of data very fast. Apache Cassandra is an example.
- **Graph databases** = store data as nodes and relationships, great for things like social networks where connections between data matter. Neo4j is an example.

## What type of database is MongoDB an example of?

- MongoDB is a document database. 
- Instead of storing data in rows and columns like a traditional spreadsheet (which is what SQL databases do), 
MongoDB stores each piece of data as a document basically a JSON-like object. 
- So instead of a rigid table, you get a flexible blob of data that can look different for each entry.

## Why is MongoDB so popular?

- **Flexible structure** = you don't need to plan out every field in advance like you do with SQL. You can change the shape of your data as your app grows.
- **Easy to scale** = MongoDB is built to handle huge amounts of data across multiple servers, which is great for big applications.
- **Developer friendly** = the data looks like JSON, which is already what most web apps use, so there's less translation needed between your code and your database.
- **Fast to get started** = you can have a database up and running in minutes without writing complex setup code.