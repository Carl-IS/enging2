from typing import Any


TYPE_EFFECTIVENESS = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
    "Water": {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
    "Electric": {"Water": 2, "Electric": 0.5, "Grass": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dark": 2, "Steel": 2, "Fairy": 0.5},
    "Poison": {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Fairy": 2},
    "Ground": {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
    "Flying": {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
    "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Fighting": 0.5, "Psychic": 2, "Ghost": 2, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2, "Rock": 2, "Steel": 0.5, "Fairy": 2},
    "Fairy": {"Fire": 0.5, "Fighting": 2, "Poison": 0.5, "Dragon": 2, "Dark": 2, "Steel": 0.5},
}

SPECIAL_DAMAGE_TYPES = {"Fire", "Water", "Electric", "Grass", "Ice", "Psychic", "Dragon", "Dark", "Fairy"}
BALANCED_ROLE_TARGETS = {"Physical Attacker", "Special Attacker", "Tank", "Fast Attacker", "Balanced"}
SET_DETAILS = {
    "Swampert": {"gender": "M", "item": "Leftovers", "ability": "Torrent", "evs": "252 HP / 252 Atk / 4 SpD", "nature": "Adamant", "moves": ["Earthquake", "Waterfall", "Ice Punch", "Stealth Rock"]},
    "Flygon": {"gender": "M", "item": "Choice Scarf", "ability": "Levitate", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Earthquake", "Dragon Claw", "U-turn", "Stone Edge"]},
    "Breloom": {"gender": "M", "item": "Focus Sash", "ability": "Technician", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Spore", "Mach Punch", "Bullet Seed", "Rock Tomb"]},
    "Aggron": {"gender": "M", "item": "Leftovers", "ability": "Sturdy", "evs": "252 HP / 252 Atk / 4 SpD", "nature": "Adamant", "moves": ["Iron Head", "Stone Edge", "Earthquake", "Stealth Rock"]},
    "Gardevoir": {"gender": "F", "item": "Choice Specs", "ability": "Trace", "evs": "252 SpA / 4 SpD / 252 Spe", "nature": "Timid", "moves": ["Moonblast", "Psychic", "Thunderbolt", "Shadow Ball"]},
    "Camerupt": {"gender": "M", "item": "Soft Sand", "ability": "Solid Rock", "evs": "248 HP / 252 SpA / 8 SpD", "nature": "Modest", "moves": ["Earth Power", "Flamethrower", "Rock Slide", "Stealth Rock"]},
    "Salamence": {"gender": "M", "item": "Life Orb", "ability": "Intimidate", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Dragon Dance", "Dragon Claw", "Earthquake", "Fire Fang"]},
    "Luxray": {"gender": "M", "item": "Choice Band", "ability": "Intimidate", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Wild Charge", "Crunch", "Ice Fang", "Volt Switch"]},
    "Garchomp": {"gender": "M", "item": "Life Orb", "ability": "Rough Skin", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Earthquake", "Dragon Claw", "Stone Edge", "Swords Dance"]},
    "Roserade": {"gender": "F", "item": "Black Sludge", "ability": "Natural Cure", "evs": "252 SpA / 4 SpD / 252 Spe", "nature": "Timid", "moves": ["Giga Drain", "Sludge Bomb", "Sleep Powder", "Spikes"]},
    "Lucario": {"gender": "M", "item": "Life Orb", "ability": "Inner Focus", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Close Combat", "Meteor Mash", "Extreme Speed", "Swords Dance"]},
    "Weavile": {"gender": "F", "item": "Heavy-Duty Boots", "ability": "Pressure", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Icicle Crash", "Knock Off", "Ice Shard", "Low Kick"]},
    "Togekiss": {"gender": "F", "item": "Leftovers", "ability": "Serene Grace", "evs": "252 HP / 4 SpA / 252 Spe", "nature": "Timid", "moves": ["Air Slash", "Moonblast", "Thunder Wave", "Roost"]},
    "Rillaboom": {"gender": "M", "item": "Miracle Seed", "ability": "Overgrow", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Wood Hammer", "Grassy Glide", "Knock Off", "U-turn"]},
    "Cinderace": {"gender": "M", "item": "Heavy-Duty Boots", "ability": "Blaze", "evs": "252 Atk / 4 SpD / 252 Spe", "nature": "Jolly", "moves": ["Pyro Ball", "High Jump Kick", "U-turn", "Sucker Punch"]},
    "Inteleon": {"gender": "M", "item": "Scope Lens", "ability": "Sniper", "evs": "252 SpA / 4 SpD / 252 Spe", "nature": "Timid", "moves": ["Hydro Pump", "Ice Beam", "Dark Pulse", "U-turn"]},
    "Corviknight": {"gender": "M", "item": "Leftovers", "ability": "Pressure", "evs": "252 HP / 168 Def / 88 SpD", "nature": "Impish", "moves": ["Brave Bird", "Iron Head", "Roost", "Defog"]},
    "Coalossal": {"gender": "M", "item": "Leftovers", "ability": "Flame Body", "evs": "252 HP / 4 Def / 252 SpD", "nature": "Careful", "moves": ["Rock Blast", "Flare Blitz", "Rapid Spin", "Stealth Rock"]},
    "Dragapult": {"gender": "M", "item": "Choice Specs", "ability": "Infiltrator", "evs": "252 SpA / 4 SpD / 252 Spe", "nature": "Timid", "moves": ["Draco Meteor", "Shadow Ball", "Flamethrower", "U-turn"]},
}

LEGAL_MOVE_OPTIONS = {
    "Swampert": ["Earthquake", "Liquidation", "Waterfall", "Ice Punch", "Stealth Rock", "Protect"],
    "Flygon": ["Earthquake", "Dragon Claw", "U-turn", "Stone Edge", "Fire Punch", "Rock Slide"],
    "Breloom": ["Spore", "Mach Punch", "Bullet Seed", "Rock Tomb", "Seed Bomb", "Swords Dance"],
    "Aggron": ["Iron Head", "Stone Edge", "Earthquake", "Stealth Rock", "Rock Slide", "Protect"],
    "Gardevoir": ["Moonblast", "Psychic", "Thunderbolt", "Shadow Ball", "Calm Mind", "Energy Ball"],
    "Camerupt": ["Earth Power", "Flamethrower", "Rock Slide", "Stealth Rock", "Earthquake", "Will-O-Wisp"],
    "Salamence": ["Dragon Dance", "Dragon Claw", "Earthquake", "Fire Fang", "Aerial Ace", "Roost"],
    "Luxray": ["Wild Charge", "Crunch", "Ice Fang", "Volt Switch", "Thunder Wave", "Facade"],
    "Garchomp": ["Earthquake", "Dragon Claw", "Stone Edge", "Swords Dance", "Stealth Rock", "Fire Fang"],
    "Roserade": ["Giga Drain", "Sludge Bomb", "Sleep Powder", "Spikes", "Toxic Spikes", "Leaf Storm"],
    "Lucario": ["Close Combat", "Meteor Mash", "Extreme Speed", "Swords Dance", "Aura Sphere", "Flash Cannon"],
    "Weavile": ["Icicle Crash", "Knock Off", "Ice Shard", "Low Kick", "Swords Dance", "Brick Break"],
    "Togekiss": ["Air Slash", "Moonblast", "Thunder Wave", "Roost", "Aura Sphere", "Flamethrower"],
    "Rillaboom": ["Wood Hammer", "Grassy Glide", "Knock Off", "U-turn", "Drain Punch", "Swords Dance"],
    "Cinderace": ["Pyro Ball", "High Jump Kick", "U-turn", "Sucker Punch", "Gunk Shot", "Court Change"],
    "Inteleon": ["Hydro Pump", "Ice Beam", "Dark Pulse", "U-turn", "Surf", "Air Slash"],
    "Corviknight": ["Brave Bird", "Iron Head", "Roost", "Defog", "U-turn", "Bulk Up"],
    "Coalossal": ["Rock Blast", "Flamethrower", "Rapid Spin", "Stealth Rock", "Earth Power", "Will-O-Wisp"],
    "Dragapult": ["Draco Meteor", "Shadow Ball", "Flamethrower", "U-turn", "Dragon Darts", "Thunderbolt"],
}

FALLBACK_ABILITIES = {
    "Abomasnow": "Snow Warning",
    "Appletun": "Ripen",
    "Arctozolt": "Volt Absorb",
    "Barraskewda": "Swift Swim",
    "Boltund": "Strong Jaw",
    "Centiskorch": "Flash Fire",
    "Claydol": "Levitate",
    "Copperajah": "Sheer Force",
    "Drednaw": "Strong Jaw",
    "Dracovish": "Strong Jaw",
    "Duraludon": "Light Metal",
    "Eiscue Ice": "Ice Face",
    "Falinks": "Battle Armor",
    "Flapple": "Ripen",
    "Frosmoth": "Shield Dust",
    "Galarian Rapidash": "Run Away",
    "Galarian Weezing": "Levitate",
    "Grapploct": "Limber",
    "Grimmsnarl": "Prankster",
    "Hatterene": "Healer",
    "Indeedee Male": "Inner Focus",
    "Morpeko Full Belly": "Hunger Switch",
    "Mr. Rime": "Tangled Feet",
    "Obstagoon": "Reckless",
    "Orbeetle": "Swarm",
    "Perrserker": "Battle Armor",
    "Polteageist": "Weak Armor",
    "Runerigus": "Wandering Spirit",
    "Sandaconda": "Sand Spit",
    "Sirfetchd": "Steadfast",
    "Thievul": "Run Away",
    "Toxtricity Amped": "Punk Rock",
}

TYPE_FALLBACK_ABILITIES = {
    "Fire": "Blaze",
    "Water": "Torrent",
    "Grass": "Overgrow",
    "Electric": "Static",
    "Bug": "Swarm",
    "Flying": "Keen Eye",
    "Poison": "Poison Point",
    "Ground": "Sturdy",
    "Rock": "Sturdy",
    "Steel": "Sturdy",
    "Ice": "Ice Body",
    "Ghost": "Cursed Body",
    "Dragon": "Pressure",
    "Dark": "Pressure",
    "Psychic": "Synchronize",
    "Fighting": "Guts",
    "Fairy": "Cute Charm",
    "Normal": "Run Away",
}

def recommend_top_six(
    pokemon: list[dict[str, Any]],
    gym_leader_type: str,
    gym_leader_team: list[str],
    all_pokemon: list[dict[str, Any]] | None = None,
    selection_mode: str = "balanced",
) -> list[dict[str, Any]]:
    leader_context = _build_leader_context(gym_leader_type, gym_leader_team, all_pokemon or pokemon)
    scored = [score_pokemon(entry, leader_context, selection_mode) for entry in pokemon]
    selected = _select_diverse_team(scored, selection_mode)
    return [format_recommendation(entry) for entry in selected]


def score_pokemon(pokemon: dict[str, Any], leader_context: dict[str, Any], selection_mode: str = "balanced") -> dict[str, Any]:
    candidate_types = _pokemon_types(pokemon)
    role = _classify_role(pokemon)

    type_offense = _type_offense_score(candidate_types, leader_context["type"])
    defensive_resistance = _defensive_resistance_score(leader_context["type"], candidate_types)
    stat_matchup = _stat_matchup_score(pokemon, leader_context["damage_style"])
    speed = _speed_score(pokemon["speed"], leader_context["average_speed"])
    weakness_penalty = _weakness_penalty(pokemon, leader_context["type"], candidate_types)

    offensive_stat = _offensive_stat_score(pokemon)
    stab_bonus = 2 if type_offense >= 5 else 0
    low_bulk_penalty = _low_bulk_penalty(pokemon)

    if selection_mode == "fast_win":
        base_score = (
            type_offense * 2.0
            + speed * 1.5
            + offensive_stat * 1.5
            + stab_bonus
            + _coverage_score(candidate_types, leader_context["type"])
            - weakness_penalty
            - low_bulk_penalty
        )
    else:
        base_score = (
            type_offense * 1.5
            + defensive_resistance * 1.5
            + _bulk_score(pokemon)
            + stat_matchup
            + speed
            - weakness_penalty
        )
    selected = dict(pokemon)
    selected["role"] = role
    selected["score_components"] = {
        "type_offense": type_offense,
        "defensive_resistance": defensive_resistance,
        "stat_matchup": stat_matchup,
        "speed": speed,
        "team_coverage": 0,
        "role_balance": 0,
        "weakness_penalty": weakness_penalty,
        "diversity_adjustment": 0,
    }
    selected["base_counter_score"] = base_score
    selected["selection_mode"] = selection_mode
    selected["counter_score"] = _normalize_score(base_score)
    return selected


def format_recommendation(pokemon: dict[str, Any]) -> dict[str, Any]:
    return {
        "pokemon": pokemon["pokemon"],
        "native_region": pokemon["native_region"],
        "is_backup": bool(pokemon.get("is_backup", False)),
        "backup_note": pokemon.get("backup_note"),
        "sprite_url": pokemon.get("sprite_url"),
        "types": _pokemon_types(pokemon),
        "role": pokemon["role"],
        **_recommended_set(pokemon),
        "stats": {
            "hp": pokemon["hp"],
            "attack": pokemon["attack"],
            "defense": pokemon["defense"],
            "special_attack": pokemon["special_attack"],
            "special_defense": pokemon["special_defense"],
            "speed": pokemon["speed"],
        },
        "counter_score": pokemon["counter_score"],
        "score_components": pokemon["score_components"],
        "reason_selected": pokemon["reason_selected"],
    }




def _recommended_set(pokemon: dict[str, Any]) -> dict[str, Any]:
    if pokemon["pokemon"] in SET_DETAILS:
        recommended_set = dict(SET_DETAILS[pokemon["pokemon"]])
        recommended_set["moves"] = _validated_moves(pokemon, recommended_set["moves"])
        return recommended_set

    if pokemon["role"] in {"Special Attacker", "Fast Attacker"} and pokemon["special_attack"] >= pokemon["attack"]:
        item = "Choice Specs"
    elif pokemon["role"] in {"Physical Attacker", "Sweeper", "Fast Attacker"}:
        item = "Life Orb"
    elif pokemon["role"] == "Tank":
        item = "Leftovers"
    else:
        item = "Expert Belt"

    return {
        "gender": "M",
        "item": item,
        "ability": _fallback_ability(pokemon),
        "evs": _fallback_evs(pokemon),
        "nature": _fallback_nature(pokemon),
        "moves": _validated_moves(pokemon, _fallback_moves(pokemon)),
    }


def _validated_moves(pokemon: dict[str, Any], moves: list[str]) -> list[str]:
    legal_options = LEGAL_MOVE_OPTIONS.get(pokemon["pokemon"])
    if not legal_options:
        return moves[:4]

    selected = []
    for move in moves:
        if move in legal_options and move not in selected:
            selected.append(move)

    for move in legal_options:
        if len(selected) >= 4:
            break
        if move not in selected:
            selected.append(move)

    return selected[:4]




def _fallback_evs(pokemon: dict[str, Any]) -> str:
    if pokemon["role"] == "Tank":
        return "252 HP / 128 Def / 128 SpD"
    if pokemon["special_attack"] > pokemon["attack"]:
        return "252 SpA / 4 SpD / 252 Spe"
    return "252 Atk / 4 SpD / 252 Spe"


def _fallback_nature(pokemon: dict[str, Any]) -> str:
    if pokemon["role"] == "Tank":
        return "Impish" if pokemon["defense"] >= pokemon["special_defense"] else "Careful"
    if pokemon["special_attack"] > pokemon["attack"]:
        return "Timid"
    return "Jolly"


def _fallback_ability(pokemon: dict[str, Any]) -> str:
    if pokemon["pokemon"] in FALLBACK_ABILITIES:
        return FALLBACK_ABILITIES[pokemon["pokemon"]]

    for pokemon_type in _pokemon_types(pokemon):
        if pokemon_type in TYPE_FALLBACK_ABILITIES:
            return TYPE_FALLBACK_ABILITIES[pokemon_type]

    return "Pressure"


def _fallback_moves(pokemon: dict[str, Any]) -> list[str]:
    type_moves = {
        "Normal": "Return",
        "Fire": "Flamethrower",
        "Water": "Surf",
        "Electric": "Thunderbolt",
        "Grass": "Giga Drain",
        "Ice": "Ice Beam",
        "Fighting": "Close Combat",
        "Poison": "Sludge Bomb",
        "Ground": "Earthquake",
        "Flying": "Air Slash",
        "Psychic": "Psychic",
        "Bug": "X-Scissor",
        "Rock": "Stone Edge",
        "Ghost": "Shadow Ball",
        "Dragon": "Dragon Claw",
        "Dark": "Dark Pulse",
        "Steel": "Iron Head",
        "Fairy": "Moonblast",
    }
    moves = [type_moves[pokemon_type] for pokemon_type in _pokemon_types(pokemon) if pokemon_type in type_moves]
    for move in ["Protect", "Substitute", "Toxic", "Rest"]:
        if len(moves) >= 4:
            break
        moves.append(move)
    return moves[:4]
def _select_diverse_team(scored: list[dict[str, Any]], selection_mode: str = "balanced") -> list[dict[str, Any]]:
    remaining = sorted(scored, key=lambda entry: entry["base_counter_score"], reverse=True)
    selected: list[dict[str, Any]] = []

    while remaining and len(selected) < 6:
        best = max(remaining, key=lambda entry: entry["base_counter_score"] + _diversity_adjustment(entry, selected))
        remaining.remove(best)

        adjustment, coverage, role_balance = _diversity_details(best, selected)
        if selection_mode == "fast_win":
            adjustment = round(adjustment * 0.5)
            role_balance = max(0, round(role_balance * 0.5))
        best = dict(best)
        best["score_components"] = dict(best["score_components"])
        best["score_components"]["team_coverage"] = coverage
        best["score_components"]["role_balance"] = role_balance
        best["score_components"]["diversity_adjustment"] = adjustment
        best["counter_score"] = _normalize_score(best["base_counter_score"] + adjustment)
        best["reason_selected"] = _selection_reason(best, coverage, role_balance, adjustment, selection_mode)
        selected.append(best)

    return selected


def _diversity_adjustment(candidate: dict[str, Any], selected: list[dict[str, Any]]) -> int:
    adjustment, _, _ = _diversity_details(candidate, selected)
    return adjustment


def _diversity_details(candidate: dict[str, Any], selected: list[dict[str, Any]]) -> tuple[int, int, int]:
    if not selected:
        return 2, 2, 0

    selected_primary_types = [entry["type_1"] for entry in selected]
    selected_all_types = {pokemon_type for entry in selected for pokemon_type in _pokemon_types(entry)}
    selected_roles = [entry["role"] for entry in selected]

    coverage = 2 if any(pokemon_type not in selected_all_types for pokemon_type in _pokemon_types(candidate)) else -2
    primary_type_penalty = -4 if selected_primary_types.count(candidate["type_1"]) >= 2 else 0
    role_penalty = -6 if selected_roles.count(candidate["role"]) >= 2 else 0

    missing_roles = BALANCED_ROLE_TARGETS - set(selected_roles)
    role_balance = 2 if candidate["role"] in missing_roles else 0
    if "Tank" not in selected_roles and candidate["role"] == "Tank":
        role_balance += 2
    if "Fast Attacker" not in selected_roles and candidate["role"] == "Fast Attacker":
        role_balance += 2

    return coverage + role_balance + primary_type_penalty + role_penalty, coverage, role_balance


def _type_offense_score(candidate_types: list[str], leader_type: str) -> int:
    multipliers = [_attack_multiplier(candidate_type, leader_type) for candidate_type in candidate_types]
    best = max(multipliers, default=1)
    if best > 1:
        return 5
    if best == 1:
        return 1
    return -3


def _defensive_resistance_score(attack_type: str, defender_types: list[str]) -> int:
    multiplier = _defensive_multiplier(attack_type, defender_types)
    if multiplier == 0:
        return 5
    if multiplier < 1:
        return 3
    if multiplier > 1:
        return -4
    return 0


def _stat_matchup_score(pokemon: dict[str, Any], damage_style: str) -> int:
    score = 0
    if max(pokemon["attack"], pokemon["special_attack"]) >= 100:
        score += 2
    if damage_style == "Special" and pokemon["special_defense"] >= 90:
        score += 2
    if damage_style == "Physical" and pokemon["defense"] >= 90:
        score += 2
    if pokemon["hp"] >= 80:
        score += 1
    return score


def _speed_score(speed: int, leader_average_speed: float) -> int:
    if speed > leader_average_speed:
        return 2
    if speed >= leader_average_speed - 10:
        return 1
    if speed < leader_average_speed - 25:
        return -1
    return 0


def _weakness_penalty(pokemon: dict[str, Any], leader_type: str, candidate_types: list[str]) -> int:
    penalty = 0
    if _defensive_multiplier(leader_type, candidate_types) > 1:
        penalty += 3
    bulk = (pokemon["hp"] + pokemon["defense"] + pokemon["special_defense"]) / 3
    if bulk < 65:
        penalty += 2
    return penalty




def _offensive_stat_score(pokemon: dict[str, Any]) -> int:
    best_attack = max(pokemon["attack"], pokemon["special_attack"])
    if best_attack >= 120:
        return 5
    if best_attack >= 100:
        return 3
    if best_attack >= 85:
        return 1
    return 0


def _bulk_score(pokemon: dict[str, Any]) -> int:
    bulk = (pokemon["hp"] + pokemon["defense"] + pokemon["special_defense"]) / 3
    if bulk >= 100:
        return 4
    if bulk >= 80:
        return 2
    if bulk >= 65:
        return 1
    return 0


def _coverage_score(candidate_types: list[str], leader_type: str) -> int:
    best = max((_attack_multiplier(candidate_type, leader_type) for candidate_type in candidate_types), default=1)
    if best > 1:
        return 2
    if best == 1:
        return 1
    return 0


def _low_bulk_penalty(pokemon: dict[str, Any]) -> int:
    bulk = (pokemon["hp"] + pokemon["defense"] + pokemon["special_defense"]) / 3
    return 2 if bulk < 65 else 0
def _classify_role(pokemon: dict[str, Any]) -> str:
    bulk = (pokemon["hp"] + pokemon["defense"] + pokemon["special_defense"]) / 3
    physical = pokemon["attack"]
    special = pokemon["special_attack"]
    speed = pokemon["speed"]

    if speed >= 105 and max(physical, special) >= 95:
        return "Fast Attacker"
    if bulk >= 95:
        return "Tank"
    if physical >= 105 and physical >= special:
        return "Physical Attacker"
    if special >= 105 and special > physical:
        return "Special Attacker"
    if speed >= 90 or max(physical, special) >= 90:
        return "Sweeper"
    return "Balanced"


def _build_leader_context(
    gym_leader_type: str,
    gym_leader_team: list[str],
    all_pokemon: list[dict[str, Any]],
) -> dict[str, Any]:
    team_names = {name.strip().lower() for name in gym_leader_team}
    matched_team = [entry for entry in all_pokemon if entry.get("pokemon", "").lower() in team_names]
    average_speed = _average([entry["speed"] for entry in matched_team]) if matched_team else 75
    leader_type = gym_leader_type.strip().title()
    return {
        "type": leader_type,
        "average_speed": average_speed,
        "damage_style": "Special" if leader_type in SPECIAL_DAMAGE_TYPES else "Physical",
    }


def _selection_reason(candidate: dict[str, Any], coverage: int, role_balance: int, adjustment: int, selection_mode: str) -> str:
    mode_intro = "fast-win potential" if selection_mode == "fast_win" else "balanced countering"
    pieces = [
        f"{candidate['pokemon']} is native to {candidate['native_region']}",
        f"was selected for {mode_intro}",
        f"fills a {candidate['role']} role",
    ]
    components = candidate["score_components"]
    if components["type_offense"] >= 5:
        pieces.append("has strong offensive type pressure")
    if selection_mode == "fast_win":
        if components["speed"] >= 2:
            pieces.append("has fast-win speed value")
        if components["stat_matchup"] >= 2:
            pieces.append("has high knockout potential")
    else:
        if components["defensive_resistance"] >= 3:
            pieces.append("offers defensive resistance or immunity")
        if components["stat_matchup"] >= 4:
            pieces.append("has a strong stat matchup")
        if role_balance > 0:
            pieces.append("improves lineup balance")
    if coverage > 0:
        pieces.append("adds team coverage")
    if adjustment < 0:
        pieces.append("but was slightly limited by overlap with the current team")
    if candidate.get("is_backup"):
        pieces.append(candidate.get("backup_note") or "used as a legal backup pick")
    return ", ".join(pieces) + "."


def _pokemon_types(pokemon: dict[str, Any]) -> list[str]:
    return [pokemon_type for pokemon_type in [pokemon["type_1"], pokemon.get("type_2") or ""] if pokemon_type]


def _attack_multiplier(attack_type: str, defender_type: str) -> float:
    return TYPE_EFFECTIVENESS.get(attack_type, {}).get(defender_type, 1)


def _defensive_multiplier(attack_type: str, defender_types: list[str]) -> float:
    multiplier = 1.0
    for defender_type in defender_types:
        multiplier *= TYPE_EFFECTIVENESS.get(attack_type, {}).get(defender_type, 1)
    return multiplier


def _normalize_score(score: int) -> int:
    return max(0, min(100, round(50 + score * 5)))


def _average(values: list[int]) -> float:
    return sum(values) / len(values)
