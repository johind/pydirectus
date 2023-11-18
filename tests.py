from pydirectus import DirectusClient

if __name__ == "__main__":
    directus = DirectusClient(
        "http://10.27.16.131:8055", static_token="sBuZtCySno9HgBLzI9p7I7iaXZvlueE-"
    )

    scenes = directus.read_items(
        "scenes",
        {
            "fields": ["id", "index", "footage_in", "footage_out"],
            "limit": 10,
        },
    )

    print(scenes)
