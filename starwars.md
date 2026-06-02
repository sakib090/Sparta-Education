# PyMongo Referencing Challenge - Write-Up

## The Approach

### 1. Fetching the Data

SWAPI returns all results in a single flat list rather than paginating them, so the fetch function checks whether the response is a list and returns it directly. A paginated fallback was kept in for compatibility with other SWAPI mirrors (e.g. `swapi.dev`) that do paginate.

```python
def fetch_all_pages(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list):
        return data

    results = []
    while url:
        results.extend(data["results"])
        url = data.get("next")
        if url:
            data = requests.get(url).json()
    return results
```

### 2. Populating Characters First

The initial version of the script tried to resolve pilot URLs against an empty (or non-existent) `characters` collection, which produced warnings for every single pilot. The fix was straightforward: insert characters into MongoDB *before* processing starships, and build the URL-to-ObjectID lookup map immediately from the inserted documents.

```python
def insert_characters(db, characters):
    collection = db["characters"]
    collection.drop()
    collection.insert_many(characters)

    url_to_id = {}
    for character in collection.find({}, {"_id": 1, "url": 1}):
        if "url" in character:
            url_to_id[character["url"]] = character["_id"]

    return url_to_id
```

### 3. Replacing Pilot URLs with ObjectIDs (Help understood with Claude)

Each starship from the API has a `pilots` field containing a list of URLs like `https://swapi.info/api/people/1`. These are resolved against the lookup map before inserting into MongoDB, swapping each URL for the corresponding `_id`.

```python
def resolve_pilots(pilot_urls, url_to_id_map):
    return [url_to_id_map[url] for url in pilot_urls if url in url_to_id_map]
```

### 4. Inserting Starships

Once transformed, all 36 starships are inserted in a single `insert_many` call for efficiency.

---

## Problems Encountered

### `TypeError: list indices must be integers or slices, not str`

The first error hit was on `data["results"]` inside the fetch loop. SWAPI returns a plain list at `https://swapi.info/api/starships/` rather than a paginated object with a `results` key. The fix was to check `isinstance(data, list)` and return early if so.

### Pilot warnings on every starship

The second issue was that all pilot URLs were unresolvable, because the `characters` collection didn't exist yet when the script ran. Fixing the order of operations - characters in first, starships second - resolved this completely. The final run inserted 82 characters and 36 starships with no warnings.

---

## Final Output

```
Fetching characters from SWAPI...
  Found 82 characters.
Inserting characters into MongoDB...
  Cleared existing characters collection.
  Inserted 82 characters into MongoDB.
  Built reference map for 82 characters.
Fetching starships from SWAPI...
  Found 36 starships.
Inserting starships into MongoDB...
  Cleared existing starships collection.
  Inserted 36 starships into MongoDB.

All done! Characters and starships are in MongoDB with proper references.
```

---

## Bonuses Completed

- **Functions throughout** - every logical step is its own named function with a docstring
- **Basic testing** - four test functions included at the bottom of the script:
  - `test_characters_inserted` - checks the characters collection is populated
  - `test_starships_inserted` - checks the starships collection is populated
  - `test_pilots_are_object_ids` - verifies pilots are stored as ObjectIDs, not strings
  - `test_pilot_references_resolve` - checks each pilot ObjectID points to a real character document
