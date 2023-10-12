from pydirectus import DirectusClient


def test_get_items(directus: DirectusClient) -> bool:
    result = directus.get_items("articles", limit=2)

    print(result)

    if "message" in result[0]:
        return False

    return True


def test_get_item_by_ID(directus: DirectusClient):
    result = directus.get_item_by_ID("shots", "0002b205-68b4-4737-b0e5-5a7da4ddc2d1")

    if "message" in result:
        return False

    return True


def test_delete_item(directus: DirectusClient):
    result = directus.delete_item("testcoll", "ebfdc5df-9df0-4103-af89-81c409aaaa65")

    return result


def test_filter_items(directus: DirectusClient):
    result = directus.get_items(
        collection="testcoll", filter={"test1": {"_contains": "123"}}
    )

    return result


def main() -> None:
    directus = DirectusClient(
        hostname="localhost:8055",
        static_token="56RVyDp9Lnd6k88JWwu-WXpZg-aasX7s",  # "Zt4FqyYM8quQYGM8RP0OaKXwzLdH2-fE",
    )

    t4 = test_get_items(directus)

    print(t4)


if __name__ == "__main__":
    main()
