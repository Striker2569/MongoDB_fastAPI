
# Metadata API

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Technologies](#technologies)
5. [Database Configuration](#database-configuration)
6. [Sample Queries and Outputs](#sample-queries-and-outputs)
---

### Introduction

The Metadata API is designed to efficiently query and manage metadata related to various economic and financial metrics. The API is built using FastAPI and utilizes MongoDB Atlas as the backend database.

---

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/MetadataAPI.git
   ```
2. Navigate into the project directory
   ```
   cd MetadataAPI
   ```
3. Install the required packages
   ```
   pip install -r requirements.txt
   ```

---

### Usage

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to see the automatically generated API documentation.

---

### Technologies

- FastAPI
- MongoDB Atlas
- Python 3.x

---

### Database Configuration

#### Using MongoDB Atlas

We use MongoDB Atlas as our cloud-based NoSQL database service. The API connects to MongoDB Atlas to store and manage metadata records.

Here's how the connection is initialized:

```python
from motor.motor_asyncio import AsyncIOMotorClient

async def startup_db_client():
    global client, db, collection
    client = AsyncIOMotorClient("mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority")
    db = client["metadata"]
    collection = db["metadata_collections"]
```

Replace `username` and `password` with your MongoDB Atlas credentials.

---

### Sample Queries and Outputs

#### Query for WPI
##### Input Query
```json
{
  "query": "WPI"
}
```

##### Output Response
```json
{
    "Title": "WPI - Auto rickshaw/Tempo/Matador/Three wheelers (2011-12 series)",
    "Category": "Inflation",
    "SubCategory": "WPI",
    "relevance": 1
}
```

#### Query for CPI
##### Input Query
```json
{
  "query": "CPI"
}
```

##### Output Response
```json
{
    "Title": "Consensus CPI Inflation for the Current Year",
    "Category": "Inflation",
    "SubCategory": "CPI",
    "relevance": 6
}
```
