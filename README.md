# PyDirectus: Python API Wrapper for Directus

PyDirectus is a simple and lightweight Python REST API wrapper for [Directus](https://github.com/directus/directus). It provides methods and typed dicts to work with items and files and is easily extensible. It also handles authentication and re-authentication.

The low-level rest adapter is based on [this blog post series](https://www.pretzellogix.net/2021/12/08/how-to-write-a-python3-sdk-library-module-for-a-json-rest-api/) from [@PretzelLogix](https://github.com/PretzelLogix)!

Please note, that PyDirectus is still under development and some parts might improve or change in the future!

## Installation

```bash
pip install pydirectus
```

## Getting Started

To get started with PyDirectus, create an instance of the `DirectusClient` class by providing your Directus instance's hostname. You can also include optional parameters for authentication, SSL verification, and logging.

```python
from pydirectus import DirectusClient

directus = DirectusClient(hostname="http://0.0.0.0:8055")
```

### Authentication

Authentication is handled automatically, and you have a couple of options:

- **Static Token:** Provide a static token for straightforward authentication.
- **Username and Password:** Use your Directus username and password for more secure authentication.

```python
directus = DirectusClient(
    hostname="http://0.0.0.0:8055",
    static_token="your_static_token",
    # OR
    username="your_username",
    password="your_password",
)
```

Note: If you use both types of authentication, a static token will take precedence.

### Making Requests

Now that you have your PyDirectus client set up, making requests is easy. Let's fetch items from a collection:

```python
items = directus.read_items(collection="your_collection")
```

You can perform various operations like reading, creating, updating, and deleting items and files using the provided methods in the `DirectusClient`.

### Examples

#### Reading Items

```python
# Retrieve the latest 10 items
items = directus.read_items(collection="your_collection", query={"limit": 10})

# Fetch items that match specific criteria
filtered_items = directus.read_items(
    collection="your_collection",
    query={"filter": {"field2": {"_eq": "some word"}}},
)
```

#### Creating an Item

```python
new_item_data = {"field1": "value1", "field2": "value2"}
created_item = directus.create_item(collection="your_collection", data=new_item_data)
```

#### Updating an Item

```python
updated_item_data = {"field1": "new_value1"}
updated_item = directus.update_item(
    collection="your_collection", id="item_id", data=updated_item_data
)
```

#### Deleting an Item

```python
directus.delete_item(collection="your_collection", id="item_id")
```

### File Operations

You can also perform operations on files:

```python
# Retrieve the latest 5 files
files = directus.read_files(query={"limit": 5})
```

Please note that it is currently not possible to upload a file.
You can only add an existing file that is stored in the storage directory.
This feature will be added in the near future!

Explore the provided methods in the [DirectusClient](https://github.com/johind/pydirectus/blob/main/pydirectus/directus.py#L33) to interact with your Directus instance effortlessly!

Feel free to report issues on [GitHub](https://github.com/johind/pydirectus).
