# PyDirectus: Python API Wrapper for Directus

PyDirectus is a simple and lightweight Python REST API wrapper for [Directus](https://github.com/directus/directus). It provides methods and typed dicts to work with items and files and is easily extensible. It also handles authentication and re-authentication.

The low-level rest adapter is based on [this series of blog posts](https://www.pretzellogix.net/2021/12/08/how-to-write-a-python3-sdk-library-module-for-a-json-rest-api/) by [@PretzelLogix](https://github.com/PretzelLogix)!

> [!IMPORTANT]
> Please be aware that PyDirectus is still under active development and some parts may be subject to change in the future!

## Installation

```bash
pip install git+https://github.com/johind/pydirectus
```

## Getting Started

To get started with PyDirectus, create an instance of the `DirectusClient` class by providing your Directus instance's hostname. You can also include optional parameters for authentication, SSL verification, and logging.

```python
from pydirectus import DirectusClient

directus = DirectusClient(hostname="http://0.0.0.0:8055")
```

### Authentication

The authentication process is done automatically, and you have a couple of options to choose from:

- **Static Token:** Provide a static token for simple authentication that bypasses the logic of the authentication process.
- **Username and Password:** Use your Directus username and password for a more secure authentication.

```python
directus = DirectusClient(
    hostname="http://0.0.0.0:8055",
    static_token="your_static_token",
    # OR
    username="your_username",
    password="your_password",
)
```

> [!NOTE]
> If you use both types of authentication, a static token takes precedence.

### Making a request

Now that you have your PyDirectus client set up, making requests is easy. Let's fetch items from a collection:

```python
items = directus.read_items("articles")
```

You can perform various operations like reading, creating, updating, and deleting items and files using the provided methods in the `DirectusClient`.

> [!TIP]
> The available query parameters align with the global parameters [outlined in the Directus documentation](https://docs.directus.io/reference/query.html).

### Examples

#### Reading Items

```python
# Retrieve the latest 10 items from the articles collection
items = directus.read_items("articles", query={"limit": 10})

# Fetch items that match specific filter criteria
filtered_items = directus.read_items(
    collection="articles",
    query={"filter": {"author": {"_eq": "Beff Jezos"}}},
)
```

#### Reading an Item by ID

```python
item = directus.read_item(collection="articles", id="53356")
```

#### Creating an Item

```python
new_item_data = {"field1": "value1", "field2": "value2"}
created_item = directus.create_item("your_collection", data=new_item_data)
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

### Working with files

The method scheme introduced earlier also applies to other tables, such as the files

```python
# Retrieve the latest 5 files
files = directus.read_files(query={"limit": 5})
```

Currently, only existing files stored in the directory can be added. Uploading a file is not possible yet. This feature will be added soon!

```python
file_data: File = {
    "storage": "local",
    "filename_disk": "demo/big-buck-bunny.mp4",
    "filename_download": "big-buck-bunny.mp4",
    "title": "Big Buck Bunny Demo",
    "type": "video/mp4",
    "filesize": 24252243, # in bytes
    "width": 1920,
    "height": 1080,
    "duration": 596047, # in milliseconds
    "metadata": {"frame_rate": 25.0}, # optional example
}

created_file = directus.create_file(file_data)
```

To learn more about the client, refer to the methods provided in the [DirectusClient](https://github.com/johind/pydirectus/blob/main/pydirectus/directus.py#L33)!

Feel free to report issues on [GitHub](https://github.com/johind/pydirectus).
