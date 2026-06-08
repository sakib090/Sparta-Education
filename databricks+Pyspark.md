# Databricks and PySpark Research

---

## What can be considered "Big Data"?

Big Data refers to datasets so large, fast, or complex that traditional tools like Excel or standard SQL databases simply can't handle them. Think billions of rows, real-time streams, or data coming from thousands of sources at once.

The three V's define it:
- **Volume** - we're talking terabytes or petabytes, not megabytes
- **Velocity** - data arriving in real-time (social media feeds, IoT sensors, financial transactions)
- **Variety** - structured tables, unstructured text, images, logs, JSON - all mixed together

A good example? Every time you use Google, Netflix, or your bank - that's Big Data in action.

---

## What is OLTP?

**Online Transaction Processing** - the backbone of day-to-day business operations. OLTP systems are designed to handle lots of small, fast transactions in real-time.

Think of it as the system running behind the scenes when you:
- Buy something online
- Withdraw cash from an ATM
- Book a flight

OLTP databases are optimised for **writes** - inserting, updating, and deleting records quickly and safely.

### What is ACID?

ACID is a set of properties that guarantee database transactions are processed reliably:

- **Atomicity** - a transaction either fully completes or doesn't happen at all. No half-measures. If your bank transfer fails halfway through, the money goes back.
- **Consistency** - the database always moves from one valid state to another. No corrupted data.
- **Isolation** - transactions don't interfere with each other, even when running simultaneously.
- **Durability** - once a transaction is committed, it stays committed - even if the system crashes.

ACID is why you can trust your bank not to lose your money mid-transfer.

---

## What is OLAP?

**Online Analytical Processing** - the opposite end of the spectrum to OLTP. OLAP is designed for complex queries across huge amounts of historical data.

Instead of "insert this one record", OLAP asks questions like:
- "What were total sales across all regions last quarter?"
- "Which product categories are trending this year?"

OLAP is optimised for **reads** - scanning millions of rows to produce insights. Tools like Snowflake, BigQuery, and Redshift are OLAP systems. This is the world of data analysts and data engineers.

---

## What are Data Lakes? How do they work?

A **Data Lake** is a centralised storage repository that holds raw data in its native format - structured, semi-structured, and unstructured - until it's needed.

Think of it like a giant lake where everything gets thrown in:
- CSVs, JSON files, images, logs, videos
- No transformation required upfront
- Store now, figure out the structure later

**How it works:**
1. Data lands in the lake from various sources (APIs, databases, IoT devices)
2. It sits in raw form in cloud storage (like AWS S3)
3. Data scientists and engineers query it when needed
4. They apply structure at the point of reading - known as **schema-on-read**

Great for flexibility, but can turn into a "data swamp" if not managed properly.

---

## What are Data Warehouses? How do they work?

A **Data Warehouse** is a structured, organised repository designed specifically for analytics and reporting. Unlike a data lake, everything in a warehouse is cleaned, transformed, and ready to query.

Think of it like a well-organised library - everything has its place.

**How it works:**
1. Data is extracted from source systems
2. Cleaned and transformed (ETL process - sound familiar?)
3. Loaded into a structured schema
4. Analysts query it using SQL

Examples: Amazon Redshift, Google BigQuery, Snowflake.

The trade-off? Less flexible than a data lake, but much faster and easier to query.

---

## What are Data Lakehouses? How do they work?

A **Data Lakehouse** is the best of both worlds - it combines the flexibility and low cost of a data lake with the structure and performance of a data warehouse.

Introduced by Databricks, it solves the main problems with both approaches:
- Data lakes are cheap but messy
- Data warehouses are clean but expensive and rigid

**How it works:**
- Raw data is stored in open formats (like Parquet) in cloud storage
- A metadata layer adds structure on top
- Supports both SQL queries AND machine learning workloads
- ACID transactions are supported (thanks to Delta Lake)

Databricks and Delta Lake are the main technologies powering the Lakehouse architecture.

---

## What are Delta Lakes?

**Delta Lake** is an open-source storage layer that brings reliability to data lakes. It sits on top of your existing cloud storage (like S3) and adds:

- **ACID transactions** - safe, reliable data writes
- **Schema enforcement** - stops bad data getting in
- **Time travel** - query data as it looked at any point in the past
- **Scalable metadata** - handles billions of files efficiently

In plain terms: Delta Lake turns your messy data lake into something you can actually trust. It's the foundation of the Lakehouse architecture and is built into Databricks by default.

---

## What is Apache Spark?

**Apache Spark** is an open-source distributed computing engine designed for processing large amounts of data - fast.

It was created at UC Berkeley in 2009 to solve a simple problem: Hadoop (the previous big data tool) was too slow because it kept reading and writing to disk. Spark keeps data **in memory** instead, making it up to 100x faster.

Spark can handle:
- Batch processing (large historical datasets)
- Real-time streaming data
- Machine learning (MLlib)
- Graph processing
- SQL queries (Spark SQL)

It runs across a cluster of machines, splitting work across many nodes simultaneously - that's the "distributed" part.

---

## What problem did Spark solve?

Before Spark, the go-to tool for Big Data was **Hadoop MapReduce**. It worked, but it was painfully slow - every step of a job required reading from and writing to disk, which created huge bottlenecks.

Spark solved this by:
- **Keeping data in memory** (RAM) between processing steps - no constant disk I/O
- **Lazy evaluation** - Spark builds up a plan of what to do, then executes it all at once in the most efficient order
- **Fault tolerance** - if a node fails, Spark can recompute lost data from its lineage
- **Unified engine** - one tool for batch, streaming, SQL, and ML instead of separate tools for each

The result? Jobs that took hours in Hadoop could run in minutes with Spark.

---

## What is PySpark?

**PySpark** is the Python API for Apache Spark. Since Spark is written in Scala, PySpark lets Python developers use all of Spark's power without having to learn Scala.

For data engineers and data scientists already comfortable with Python and Pandas, PySpark feels familiar - but operates at a completely different scale. Instead of processing data on your laptop, PySpark distributes it across a cluster of machines.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WeatherAnalysis").getOrCreate()

df = spark.read.json("s3://my-bucket/weather_data.json")
df.show()
```

That's the same concept as Pandas - but this could be running across 100 machines processing terabytes of data.

---

## What is Databricks?

**Databricks** is a cloud-based platform built on top of Apache Spark. It was founded by the original creators of Spark and Delta Lake to make distributed data processing accessible and collaborative.

Think of it as a managed, cloud-hosted environment where you can:
- Write PySpark code in notebooks (similar to Jupyter)
- Run jobs across auto-scaling clusters
- Build and deploy ML models
- Use Delta Lake out of the box
- Collaborate with your team in real-time

Instead of setting up and managing your own Spark cluster (which is complex and time-consuming), Databricks handles all the infrastructure for you.

It sits on top of AWS, Azure, or GCP and integrates natively with cloud storage like S3.

--- 