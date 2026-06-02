import requests
import pymongo
from pymongo import MongoClient


# --- Database connection ---

def get_db():
    """Connect to the local MongoDB instance and return the starwars database."""
    client = MongoClient("mongodb://localhost:27017/")
    return client["starwars"]


# --- Fetch data from SWAPI ---

def fetch_all_pages(url):
    """
    SWAPI paginates its results. This keeps fetching until there are no more pages,
    returning all results in a single flat list.
    """
    results = []
    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results.extend(data["results"])
        url = data.get("next")  # None when we've hit the last page
    return results


def fetch_starships():
    """Pull all starships from the SWAPI API."""
    print("Fetching starships from SWAPI...")
    starships = fetch_all_pages("https://swapi.info/api/starships/")
    print(f"  Found {len(starships)} starships.")
    return starships


# --- Resolve pilot URLs to MongoDB ObjectIDs ---

def build_pilot_url_to_id_map(db):
    """
    Query the existing characters collection and build a lookup dictionary
    mapping each character's SWAPI URL to their MongoDB _id.
    This is what lets us replace the pilot URLs with proper ObjectID references.
    """
    characters = db["characters"]
    url_to_id = {}

    for character in characters.find({}, {"_id": 1, "url": 1}):
        if "url" in character:
            url_to_id[character["url"]] = character["_id"]

    print(f"  Loaded {len(url_to_id)} character references from MongoDB.")
    return url_to_id


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


# --- Transform and insert starships ---

def transform_starship(starship, url_to_id_map):
    """
    Takes a raw starship dict from SWAPI and returns a version ready for MongoDB:
    - 'pilots' is replaced with a list of ObjectIDs instead of URLs
    - '_id' is left for MongoDB to auto-generate
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

    # Clear out any existing documents so re-runs don't create duplicates
    collection.drop()
    print("  Cleared existing starships collection.")

    transformed = [transform_starship(s, url_to_id_map) for s in starships]
    result = collection.insert_many(transformed)
    print(f"  Inserted {len(result.inserted_ids)} starships into MongoDB.")
    return result


# --- Main ---

def main():
    db = get_db()

    # Step 1: pull all starships from the API
    starships = fetch_starships()

    # Step 2: build a URL -> ObjectID map from the existing characters collection
    print("Building pilot reference map...")
    url_to_id_map = build_pilot_url_to_id_map(db)

    # Step 3: replace pilot URLs with ObjectIDs and insert into MongoDB
    print("Inserting starships into MongoDB...")
    insert_starships(db, starships, url_to_id_map)

    print("\nDone! Starships collection is ready with referenced pilot ObjectIDs.")


if __name__ == "__main__":
    main()


# =============================================================================
# BONUS: Basic tests
# =============================================================================

def test_starships_inserted():
    """Check that the starships collection isn't empty after running main."""
    db = get_db()
    count = db["starships"].count_documents({})
    assert count > 0, "No starships found — did main() run successfully?"
    print(f"Test passed: {count} starships in the collection.")


def test_pilots_are_object_ids():
    """
    Check that at least one starship has pilots stored as ObjectIDs
    rather than plain strings (URLs).
    """
    from bson import ObjectId
    db = get_db()

    # Find any starship that has at least one pilot
    starship = db["starships"].find_one({"pilots": {"$not": {"$size": 0}}})
    if starship is None:
        print("Test skipped: no starships with pilots found.")
        return

    for pilot_ref in starship["pilots"]:
        assert isinstance(pilot_ref, ObjectId), (
            f"Expected ObjectId but got {type(pilot_ref)} — pilot URLs may not have been resolved."
        )

    print(f"Test passed: pilots in '{starship.get('name')}' are stored as ObjectIDs.")