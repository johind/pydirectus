# Directus API Wrapper

## Installation

```bash

pip install git+http://192.168.204.170:8010/kigvi/pydirectus.git

```

## Setup

### Login with static token

```python
from pydirectus import DirectusClient

directus = DirectusClient(
    hostname="http://0.0.0.0:8055", 
    api_key="your-static-api-token", 
)
```

### Login with user credentials

```python
from pydirectus import DirectusClient

directus = DirectusClient(
    hostname="http://0.0.0.0:8055", 
    username="your@email.com",
    password="password"
)
```

Note:

1. Login with LDAP is not supported yet!
2. If you are using both auth types, a static token will have priority!

## Usage Examples

```python
# return all items in shots with nested fields, limited to 10
response = directus.read_items(
    collection="articles", 
    fields=["*.*"], 
    limit=10
)
```

```python
# return item with specified id, only start_frame
response = directus.read_item(
    collection="articles", 
    item_id="0002b205-68b4-4737-b0e5-5a7da4ddc2d1", 
    fields=["title"]
)
```

```python
# create a new item in the "articles" collection
# directus will return a clone of the created object
data = {
    "title": "This is an example article",
    "author": "example"
}

response = directus.create_item(
    collection="articles", 
    data=data
)
```
