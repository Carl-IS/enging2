import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    requests = None


BASE_DIR = Path(__file__).resolve().parent
CACHE_PATH = BASE_DIR / "data" / "pokemon_cache.csv"
POKEAPI_TIMEOUT_SECONDS = 6
POKEAPI_MAX_WORKERS = 16

CSV_FIELDS = [
    "id",
    "pokemon",
    "native_region",
    "type_1",
    "type_2",
    "hp",
    "attack",
    "defense",
    "special_attack",
    "special_defense",
    "speed",
    "sprite_url",
    "is_legendary",
    "is_mythical",
    "is_paradox",
]

REGION_DEX_RANGES = {
    "Kanto": range(1, 152),
    "Johto": range(152, 252),
    "Hoenn": range(252, 387),
    "Sinnoh": range(387, 494),
    "Unova": range(494, 650),
    "Kalos": range(650, 722),
    "Alola": range(722, 810),
    "Galar": range(810, 906),
    "Paldea": range(906, 1026),
}

ALLOWED_REGION_IDS = [*range(252, 387), *range(387, 494), *range(810, 906)]
POKEMON_ID_OVERRIDES = {
    "pikachu": 25,
    "raichu": 26,
    "electabuzz": 125,
    "magneton": 82,
    "voltorb": 100,
    "electrode": 101,
}
PARADOX_NAMES = {
    "Great Tusk", "Scream Tail", "Brute Bonnet", "Flutter Mane", "Slither Wing",
    "Sandy Shocks", "Roaring Moon", "Walking Wake", "Gouging Fire", "Raging Bolt",
    "Iron Treads", "Iron Bundle", "Iron Hands", "Iron Jugulis", "Iron Moth",
    "Iron Thorns", "Iron Valiant", "Iron Leaves", "Iron Boulder", "Iron Crown",
}


def _sprite_url(pokemon_id: int | None) -> str | None:
    if not pokemon_id:
        return None
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"


FALLBACK_POKEMON = [
    {"id": 260, "pokemon": "Swampert", "native_region": "Hoenn", "type_1": "Water", "type_2": "Ground", "hp": 100, "attack": 110, "defense": 90, "special_attack": 85, "special_defense": 90, "speed": 60, "sprite_url": _sprite_url(260), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 330, "pokemon": "Flygon", "native_region": "Hoenn", "type_1": "Ground", "type_2": "Dragon", "hp": 80, "attack": 100, "defense": 80, "special_attack": 80, "special_defense": 80, "speed": 100, "sprite_url": _sprite_url(330), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 286, "pokemon": "Breloom", "native_region": "Hoenn", "type_1": "Grass", "type_2": "Fighting", "hp": 60, "attack": 130, "defense": 80, "special_attack": 60, "special_defense": 60, "speed": 70, "sprite_url": _sprite_url(286), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 306, "pokemon": "Aggron", "native_region": "Hoenn", "type_1": "Steel", "type_2": "Rock", "hp": 70, "attack": 110, "defense": 180, "special_attack": 60, "special_defense": 60, "speed": 50, "sprite_url": _sprite_url(306), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 282, "pokemon": "Gardevoir", "native_region": "Hoenn", "type_1": "Psychic", "type_2": "Fairy", "hp": 68, "attack": 65, "defense": 65, "special_attack": 125, "special_defense": 115, "speed": 80, "sprite_url": _sprite_url(282), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 323, "pokemon": "Camerupt", "native_region": "Hoenn", "type_1": "Fire", "type_2": "Ground", "hp": 70, "attack": 100, "defense": 70, "special_attack": 105, "special_defense": 75, "speed": 40, "sprite_url": _sprite_url(323), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 405, "pokemon": "Luxray", "native_region": "Sinnoh", "type_1": "Electric", "type_2": "", "hp": 80, "attack": 120, "defense": 79, "special_attack": 95, "special_defense": 79, "speed": 70, "sprite_url": _sprite_url(405), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 445, "pokemon": "Garchomp", "native_region": "Sinnoh", "type_1": "Dragon", "type_2": "Ground", "hp": 108, "attack": 130, "defense": 95, "special_attack": 80, "special_defense": 85, "speed": 102, "sprite_url": _sprite_url(445), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 407, "pokemon": "Roserade", "native_region": "Sinnoh", "type_1": "Grass", "type_2": "Poison", "hp": 60, "attack": 70, "defense": 65, "special_attack": 125, "special_defense": 105, "speed": 90, "sprite_url": _sprite_url(407), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 448, "pokemon": "Lucario", "native_region": "Sinnoh", "type_1": "Fighting", "type_2": "Steel", "hp": 70, "attack": 110, "defense": 70, "special_attack": 115, "special_defense": 70, "speed": 90, "sprite_url": _sprite_url(448), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 461, "pokemon": "Weavile", "native_region": "Sinnoh", "type_1": "Dark", "type_2": "Ice", "hp": 70, "attack": 120, "defense": 65, "special_attack": 45, "special_defense": 85, "speed": 125, "sprite_url": _sprite_url(461), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 468, "pokemon": "Togekiss", "native_region": "Sinnoh", "type_1": "Fairy", "type_2": "Flying", "hp": 85, "attack": 50, "defense": 95, "special_attack": 120, "special_defense": 115, "speed": 80, "sprite_url": _sprite_url(468), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 812, "pokemon": "Rillaboom", "native_region": "Galar", "type_1": "Grass", "type_2": "", "hp": 100, "attack": 125, "defense": 90, "special_attack": 60, "special_defense": 70, "speed": 85, "sprite_url": _sprite_url(812), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 815, "pokemon": "Cinderace", "native_region": "Galar", "type_1": "Fire", "type_2": "", "hp": 80, "attack": 116, "defense": 75, "special_attack": 65, "special_defense": 75, "speed": 119, "sprite_url": _sprite_url(815), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 818, "pokemon": "Inteleon", "native_region": "Galar", "type_1": "Water", "type_2": "", "hp": 70, "attack": 85, "defense": 65, "special_attack": 125, "special_defense": 65, "speed": 120, "sprite_url": _sprite_url(818), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 823, "pokemon": "Corviknight", "native_region": "Galar", "type_1": "Flying", "type_2": "Steel", "hp": 98, "attack": 87, "defense": 105, "special_attack": 53, "special_defense": 85, "speed": 67, "sprite_url": _sprite_url(823), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 839, "pokemon": "Coalossal", "native_region": "Galar", "type_1": "Rock", "type_2": "Fire", "hp": 110, "attack": 80, "defense": 120, "special_attack": 80, "special_defense": 90, "speed": 30, "sprite_url": _sprite_url(839), "is_legendary": False, "is_mythical": False, "is_paradox": False},
    {"id": 887, "pokemon": "Dragapult", "native_region": "Galar", "type_1": "Dragon", "type_2": "Ghost", "hp": 88, "attack": 120, "defense": 75, "special_attack": 100, "special_defense": 75, "speed": 142, "sprite_url": _sprite_url(887), "is_legendary": False, "is_mythical": False, "is_paradox": False},
]


def load_pokemon_data() -> list[dict[str, Any]]:
    cached = _read_cache()
    if cached:
        return cached

    fetched = _fetch_pokemon_data()
    data = fetched or FALLBACK_POKEMON
    _write_cache(data)
    return data


def load_region_pokemon_data(region: str) -> list[dict[str, Any]]:
    """Load cached data, expanding one native region from PokeAPI when needed."""
    target_region = region.strip().title()
    cached = _read_cache()
    region_range = REGION_DEX_RANGES.get(target_region)

    if not region_range:
        return cached

    cached_region_ids = {
        int(entry.get("id") or 0)
        for entry in cached
        if entry.get("native_region", "").lower() == target_region.lower()
    }
    expected_ids = set(region_range)

    if expected_ids.issubset(cached_region_ids):
        return cached

    fetched = _fetch_pokemon_data_for_ids(region_range)
    if not fetched:
        return cached

    merged = _merge_pokemon_rows(cached, fetched)
    _write_cache(merged)
    return merged


def load_region_type_pokemon_data(region: str, pokemon_type: str) -> list[dict[str, Any]]:
    """Load cached data, fetching only the selected native region/type when possible."""
    target_region = region.strip().title()
    target_type = pokemon_type.strip().title()
    cached = _read_cache()
    region_range = REGION_DEX_RANGES.get(target_region)

    if not region_range:
        return cached

    type_ids = _fetch_type_pokemon_ids(target_type)
    if not type_ids:
        return load_region_pokemon_data(target_region)

    expected_ids = set(region_range).intersection(type_ids)
    cached_ids = {
        int(entry.get("id") or 0)
        for entry in cached
        if entry.get("native_region", "").lower() == target_region.lower()
        and (
            entry.get("type_1", "").lower() == target_type.lower()
            or entry.get("type_2", "").lower() == target_type.lower()
        )
    }
    missing_ids = sorted(expected_ids - cached_ids)

    if not missing_ids:
        return cached

    fetched = _fetch_pokemon_data_for_ids(missing_ids)
    if not fetched:
        return cached

    merged = _merge_pokemon_rows(cached, fetched)
    _write_cache(merged)
    return merged


def load_pokemon_by_name(name: str) -> dict[str, Any] | None:
    normalized_name = name.strip().lower()
    if not normalized_name:
        return None

    cached = _read_cache()
    for entry in cached:
        if entry.get("pokemon", "").lower() == normalized_name:
            return entry

    fetched = _fetch_pokemon_by_name(normalized_name)
    if not fetched:
        return None

    _write_cache(_merge_pokemon_rows(cached, [fetched]))
    return fetched


def build_team_display(team_names: list[str], pokemon_data: list[dict[str, Any]]) -> list[dict[str, str | None]]:
    by_name = {entry.get("pokemon", "").lower(): entry for entry in pokemon_data}
    return [{"pokemon": name, "sprite_url": _sprite_for_name(name, by_name)} for name in team_names]


def _read_cache() -> list[dict[str, Any]]:
    if not CACHE_PATH.exists() or CACHE_PATH.stat().st_size == 0:
        return []

    with CACHE_PATH.open(newline="", encoding="utf-8-sig") as cache_file:
        rows = list(csv.DictReader(cache_file))

    return [_normalize_row(row) for row in rows if row.get("pokemon")]


def _write_cache(rows: list[dict[str, Any]]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_PATH.open("w", newline="", encoding="utf-8") as cache_file:
        writer = csv.DictWriter(cache_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _fetch_pokemon_data() -> list[dict[str, Any]]:
    return _fetch_pokemon_data_for_ids(ALLOWED_REGION_IDS)


def _fetch_pokemon_data_for_ids(pokemon_ids) -> list[dict[str, Any]]:
    if requests is None:
        return []

    results = []
    pokemon_ids = list(pokemon_ids)
    workers = min(POKEAPI_MAX_WORKERS, max(1, len(pokemon_ids)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(_fetch_pokemon_by_id, pokemon_id) for pokemon_id in pokemon_ids]
        for future in as_completed(futures):
            row = future.result()
            if row:
                results.append(row)

    return sorted(results, key=lambda entry: int(entry.get("id") or 0))


def _fetch_type_pokemon_ids(pokemon_type: str) -> set[int]:
    if requests is None:
        return set()

    try:
        response = requests.get(f"https://pokeapi.co/api/v2/type/{pokemon_type.strip().lower()}", timeout=POKEAPI_TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return set()

    ids = set()
    for item in payload.get("pokemon", []):
        url = item.get("pokemon", {}).get("url", "").rstrip("/")
        try:
            ids.add(int(url.rsplit("/", 1)[-1]))
        except ValueError:
            continue
    return ids


def _fetch_pokemon_by_id(pokemon_id: int) -> dict[str, Any] | None:
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}", timeout=POKEAPI_TIMEOUT_SECONDS)
        response.raise_for_status()
        pokemon = response.json()

        species_response = requests.get(pokemon["species"]["url"], timeout=POKEAPI_TIMEOUT_SECONDS)
        species_response.raise_for_status()
        species = species_response.json()
    except requests.RequestException:
        return None

    return _build_pokemon_row(pokemon, species)


def _fetch_pokemon_by_name(name: str) -> dict[str, Any] | None:
    if requests is None:
        return None

    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.replace(' ', '-')}", timeout=POKEAPI_TIMEOUT_SECONDS)
        response.raise_for_status()
        pokemon = response.json()

        species_response = requests.get(pokemon["species"]["url"], timeout=POKEAPI_TIMEOUT_SECONDS)
        species_response.raise_for_status()
        species = species_response.json()
    except requests.RequestException:
        return None

    return _build_pokemon_row(pokemon, species)


def _build_pokemon_row(pokemon: dict[str, Any], species: dict[str, Any]) -> dict[str, Any]:
    pokemon_id = int(pokemon["id"])
    stats = {item["stat"]["name"]: item["base_stat"] for item in pokemon["stats"]}
    types = [slot["type"]["name"].title() for slot in pokemon["types"]]
    display_name = pokemon["name"].replace("-", " ").title()

    return {
        "id": pokemon_id,
        "pokemon": display_name,
        "native_region": _region_for_id(pokemon_id),
        "type_1": types[0],
        "type_2": types[1] if len(types) > 1 else "",
        "hp": stats["hp"],
        "attack": stats["attack"],
        "defense": stats["defense"],
        "special_attack": stats["special-attack"],
        "special_defense": stats["special-defense"],
        "speed": stats["speed"],
        "sprite_url": _extract_sprite_url(pokemon, pokemon_id),
        "is_legendary": bool(species.get("is_legendary")),
        "is_mythical": bool(species.get("is_mythical")),
        "is_paradox": display_name in PARADOX_NAMES,
    }


def _merge_pokemon_rows(existing: list[dict[str, Any]], fetched: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged_by_id = {int(entry.get("id") or 0): entry for entry in existing}
    for entry in fetched:
        merged_by_id[int(entry.get("id") or 0)] = entry
    return sorted(merged_by_id.values(), key=lambda entry: int(entry.get("id") or 0))


def _sprite_for_name(name: str, by_name: dict[str, dict[str, Any]]) -> str | None:
    normalized = name.strip().lower()
    if not normalized:
        return None

    cached = by_name.get(normalized)
    if cached and cached.get("sprite_url"):
        return cached["sprite_url"]

    if normalized in POKEMON_ID_OVERRIDES:
        return _sprite_url(POKEMON_ID_OVERRIDES[normalized])

    if requests is None:
        return None

    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{normalized.replace(' ', '-')}", timeout=4)
        response.raise_for_status()
        pokemon = response.json()
    except requests.RequestException:
        return None

    return _extract_sprite_url(pokemon, pokemon.get("id"))


def _extract_sprite_url(pokemon: dict[str, Any], pokemon_id: int | None) -> str | None:
    official_artwork = (
        pokemon.get("sprites", {})
        .get("other", {})
        .get("official-artwork", {})
        .get("front_default")
    )
    return official_artwork or _sprite_url(pokemon_id)


def _region_for_id(pokemon_id: int) -> str:
    for region, dex_range in REGION_DEX_RANGES.items():
        if pokemon_id in dex_range:
            return region
    return "Unknown"


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(row)
    for key in ("id", "hp", "attack", "defense", "special_attack", "special_defense", "speed"):
        normalized[key] = int(normalized.get(key) or 0)
    for key in ("is_legendary", "is_mythical", "is_paradox"):
        normalized[key] = str(normalized.get(key, "")).lower() in {"true", "1", "yes"}
    normalized["type_2"] = normalized.get("type_2") or ""
    normalized["sprite_url"] = normalized.get("sprite_url") or _sprite_url(normalized.get("id"))
    return normalized
