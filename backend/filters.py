from typing import Any


ALLOWED_CHALLENGER_REGIONS = {"Hoenn", "Sinnoh", "Galar"}
NATIONAL_DEX_BANNED_POKEMON = {"dragapult", "sneasler"}


def apply_native_region_filter(pokemon: list[dict[str, Any]], challenger_region: str) -> list[dict[str, Any]]:
    target_region = challenger_region.strip().lower()
    return [entry for entry in pokemon if entry.get("native_region", "").lower() == target_region]


def apply_restriction_filter(
    pokemon: list[dict[str, Any]],
    gym_leader_team: list[str],
) -> list[dict[str, Any]]:
    blocked_names = {name.strip().lower() for name in gym_leader_team if name.strip()}
    return [
        entry
        for entry in pokemon
        if not _is_restricted(entry)
        and entry.get("pokemon", "").lower() not in NATIONAL_DEX_BANNED_POKEMON
        and entry.get("pokemon", "").lower() not in blocked_names
    ]


def _is_restricted(pokemon: dict[str, Any]) -> bool:
    return bool(
        pokemon.get("is_legendary")
        or pokemon.get("is_mythical")
        or pokemon.get("is_paradox")
    )
