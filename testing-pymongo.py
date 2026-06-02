import requests
import pymongo
from pymongo import MongoClient

# Database connection 

def get_db():
    """Connect to the local MongoDB instance and return the starwars database."""
    client = MongoClient("mongodb://localhost:27017/")
    return client["starwars"]


# Fetch data from SWAPI

def fetch_all_pages(url):
    """
    swapi.info returns all results in a single list (no pagination),
    so we just fetch once and return directly.
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # swapi.info returns a plain list, not a paginated dict
    if isinstance(data, list):
        return data

    # Fallback for paginated APIs (e.g. swapi.dev)
    results = []
    while url:
        results.extend(data["results"])
        url = data.get("next")
        if url:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
    return results


def fetch_characters():
    """Pull all people/characters from the SWAPI API."""
    print("Fetching characters from SWAPI...")
    characters = fetch_all_pages("https://swapi.info/api/people/")
    print(f"  Found {len(characters)} characters.")
    return characters


def fetch_starships():
    """Pull all starships from the SWAPI API."""
    print("Fetching starships from SWAPI...")
    starships = fetch_all_pages("https://swapi.info/api/starships/")
    print(f"  Found {len(starships)} starships.")
    return starships


# Insert characters

def insert_characters(db, characters):
    """
    Insert all characters into the 'characters' collection.
    Drops the existing collection first to avoid duplicates on re-runs.
    Returns a URL -> ObjectID map so other collections can reference them.
    """
    collection = db["characters"]
    collection.drop()
    print("  Cleared existing characters collection.")

    result = collection.insert_many(characters)
    print(f"  Inserted {len(result.inserted_ids)} characters into MongoDB.")

    url_to_id = {}
    for character in collection.find({}, {"_id": 1, "url": 1}):
        if "url" in character:
            url_to_id[character["url"]] = character["_id"]

    print(f"  Built reference map for {len(url_to_id)} characters.")
    return url_to_id


# Resolve pilot URLs to MongoDB ObjectIDs

def resolve_pilots(pilot_urls, url_to_id_map):
    """
    Given a list of pilot URLs from a starship document, return a list of
    the corresponding MongoDB ObjectIDs. Any URLs not found in the map are skipped.
    """
    resolved = []
    for url in pilot_urls:
        object_id = url_to_id_map.get(url)
        if object_id:
            resolved.append(object_id)
        else:
            print(f"  Warning: no matching character found for pilot URL: {url}")
    return resolved


# Transform and insert starships

def transform_starship(starship, url_to_id_map):
    """
    Takes a raw starship dict from SWAPI and returns a version ready for MongoDB:
    - 'pilots' is replaced with a list of ObjectIDs instead of URLs
    """
    transformed = starship.copy()
    transformed["pilots"] = resolve_pilots(starship.get("pilots", []), url_to_id_map)
    return transformed


def insert_starships(db, starships, url_to_id_map):
    """
    Transform each starship and insert them all into the 'starships' collection.
    Uses insert_many for efficiency rather than inserting one at a time.
    """
    collection = db["starships"]
    collection.drop()
    print("  Cleared existing starships collection.")

    transformed = [transform_starship(s, url_to_id_map) for s in starships]
    result = collection.insert_many(transformed)
    print(f"  Inserted {len(result.inserted_ids)} starships into MongoDB.")
    return result


#  Main 

def main():
    db = get_db()

    # Step 1: fetch and insert characters first - starships reference them
    characters = fetch_characters()
    print("Inserting characters into MongoDB...")
    url_to_id_map = insert_characters(db, characters)

    # Step 2: fetch all starships from the API
    starships = fetch_starships()

    # Step 3: replace pilot URLs with ObjectIDs and insert into MongoDB
    print("Inserting starships into MongoDB...")
    insert_starships(db, starships, url_to_id_map)

    print("\nAll done! Characters and starships are in MongoDB with proper references.")


if __name__ == "__main__":
    main()


# BONUS: Basic tests

def test_characters_inserted():
    """Check that the characters collection isn't empty after running main."""
    db = get_db()
    count = db["characters"].count_documents({})
    assert count > 0, "No characters found - did main() run successfully?"
    print(f"Test passed: {count} characters in the collection.")


def test_starships_inserted():
    """Check that the starships collection isn't empty after running main."""
    db = get_db()
    count = db["starships"].count_documents({})
    assert count > 0, "No starships found - did main() run successfully?"
    print(f"Test passed: {count} starships in the collection.")


def test_pilots_are_object_ids():
    """
    Check that at least one starship has pilots stored as ObjectIDs
    rather than plain strings (URLs).
    """
    from bson import ObjectId
    db = get_db()

    starship = db["starships"].find_one({"pilots": {"$not": {"$size": 0}}})
    if starship is None:
        print("Test skipped: no starships with pilots found.")
        return

    for pilot_ref in starship["pilots"]:
        assert isinstance(pilot_ref, ObjectId), (
            f"Expected ObjectId but got {type(pilot_ref)} - pilot URLs may not have been resolved."
        )

    print(f"Test passed: pilots in '{starship.get('name')}' are stored as ObjectIDs.")


def test_pilot_references_resolve():
    """
    Pick a starship with pilots and verify each ObjectID actually points
    to a real document in the characters collection.
    """
    db = get_db()

    starship = db["starships"].find_one({"pilots": {"$not": {"$size": 0}}})
    if starship is None:
        print("Test skipped: no starships with pilots found.")
        return

    for pilot_id in starship["pilots"]:
        character = db["characters"].find_one({"_id": pilot_id})
        assert character is not None, (
            f"ObjectID {pilot_id} in starship '{starship.get('name')}' "
            f"does not match any character document."
        )

    print(f"Test passed: all pilot references in '{starship.get('name')}' resolve correctly.")