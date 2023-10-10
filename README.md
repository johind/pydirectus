# Directus API Wrapper

## Installation

```bash
pip install git+http://192.168.204.170:8010/kigvi/pydirectus.git
```

## Setup

### Login with static token:
```python
from pydirectus import DirectusAPI

directus = DirectusAPI(
    hostname="192.168.204.42:8055", 
    api_key="Zt4FqyYM8quQYGM8RP0OaKXwzLdH2-fE", 
)
```
### Login with user credentials:
```python
from pydirectus import DirectusAPI

directus = DirectusAPI(
    hostname="192.168.204.42:8055", 
    username="your@email-address",
    password="password"
)
```
Note:
1. Login with LDAP is not supported yet!
2. If you are using both auth types, a static token will have priority!

## Examples

```python
# return all items in shots with nested fields, limited to 10
response = directus.get_items(
    collection="shots", 
    fields=["*.*"], 
    limit=10
)

# return item with specified id, only start_frame
response = directus.get_item_by_ID(
    collection="shots", 
    item_id="0002b205-68b4-4737-b0e5-5a7da4ddc2d1", 
    fields=["start_frame"]
)
