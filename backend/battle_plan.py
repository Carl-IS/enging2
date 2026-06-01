from typing import Any

from scoring import TYPE_EFFECTIVENESS

MOVE_TYPES = {
    "Aerial Ace": "Flying",
    "Air Slash": "Flying",
    "Aura Sphere": "Fighting",
    "Brave Bird": "Flying",
    "Brick Break": "Fighting",
    "Bullet Seed": "Grass",
    "Close Combat": "Fighting",
    "Crunch": "Dark",
    "Dark Pulse": "Dark",
    "Draco Meteor": "Dragon",
    "Dragon Claw": "Dragon",
    "Dragon Darts": "Dragon",
    "Drain Punch": "Fighting",
    "Earth Power": "Ground",
    "Earthquake": "Ground",
    "Energy Ball": "Grass",
    "Extreme Speed": "Normal",
    "Facade": "Normal",
    "Fire Fang": "Fire",
    "Fire Punch": "Fire",
    "Flamethrower": "Fire",
    "Flare Blitz": "Fire",
    "Flash Cannon": "Steel",
    "Giga Drain": "Grass",
    "Grassy Glide": "Grass",
    "Gunk Shot": "Poison",
    "High Jump Kick": "Fighting",
    "Hydro Pump": "Water",
    "Ice Beam": "Ice",
    "Ice Fang": "Ice",
    "Ice Punch": "Ice",
    "Ice Shard": "Ice",
    "Icicle Crash": "Ice",
    "Iron Head": "Steel",
    "Knock Off": "Dark",
    "Leaf Storm": "Grass",
    "Liquidation": "Water",
    "Low Kick": "Fighting",
    "Mach Punch": "Fighting",
    "Meteor Mash": "Steel",
    "Moonblast": "Fairy",
    "Psychic": "Psychic",
    "Pyro Ball": "Fire",
    "Return": "Normal",
    "Rock Blast": "Rock",
    "Rock Slide": "Rock",
    "Seed Bomb": "Grass",
    "Shadow Ball": "Ghost",
    "Sludge Bomb": "Poison",
    "Stone Edge": "Rock",
    "Surf": "Water",
    "Thunderbolt": "Electric",
    "U-turn": "Bug",
    "Waterfall": "Water",
    "Wild Charge": "Electric",
    "Wood Hammer": "Grass",
    "X-Scissor": "Bug",
}

STATUS_MOVES = {
    "Bulk Up", "Calm Mind", "Court Change", "Defog", "Dragon Dance", "Protect",
    "Rapid Spin", "Rest", "Roost", "Sleep Powder", "Spikes", "Spore",
    "Stealth Rock", "Substitute", "Swords Dance", "Thunder Wave", "Toxic",
    "Toxic Spikes", "Will-O-Wisp",
}


def generate_battle_plan(
    recommended_team: list[dict[str, Any]],
    gym_leader_team_data: list[dict[str, Any]],
    selection_mode: str,
) -> list[dict[str, Any]]:
    battle_plan = []
    used_targets: set[str] = set()
    for challenger in recommended_team:
        available_targets = [
            target for target in gym_leader_team_data
            if _target_key(target) not in used_targets
        ] or gym_leader_team_data
        matchups = [_score_matchup(challenger, target, selection_mode) for target in available_targets]
        best = max(matchups, key=lambda item: item["raw_score"]) if matchups else None
        if not best:
            continue

        used_targets.add(best["target_key"])
        recommended_move = _select_recommended_move(challenger, best, selection_mode)
        battle_plan.append(
            {
                "challenger_pokemon": challenger["pokemon"],
                "challenger_image_url": challenger.get("sprite_url") or challenger.get("image_url"),
                "best_match_against": best["target_name"],
                "best_match_image_url": best.get("target_image_url"),
                "matchup_score": _normalize_score(best["raw_score"]),
                "recommended_move": recommended_move["move"],
                "recommended_move_type": recommended_move.get("type"),
                "reason": _matchup_reason(challenger, best, selection_mode, recommended_move),
                "suggested_sequence": _suggested_sequence(challenger, best, selection_mode, recommended_move),
            }
        )
    return battle_plan


def _score_matchup(challenger: dict[str, Any], target: dict[str, Any], selection_mode: str) -> dict[str, Any]:
    challenger_types = _types_from_recommendation(challenger)
    target_types = _types_from_entry(target)
    offense_multiplier = max((_attack_multiplier(attack_type, target_types) for attack_type in challenger_types), default=1)
    defense_multiplier = max((_attack_multiplier(attack_type, challenger_types) for attack_type in target_types), default=1)
    stats = challenger["stats"]
    target_speed = int(target.get("speed") or 75)
    offense = max(int(stats["attack"]), int(stats["special_attack"]))
    target_bulk = _bulk(target)
    speed_advantage = int(stats["speed"]) - target_speed
    bulk = (int(stats["hp"]) + int(stats["defense"]) + int(stats["special_defense"])) / 3

    type_score = 12 if offense_multiplier > 1 else 4 if offense_multiplier == 1 else -8
    resistance_score = 10 if defense_multiplier == 0 else 5 if defense_multiplier < 1 else -8 if defense_multiplier > 1 else 1
    speed_score = 6 if speed_advantage > 0 else 2 if speed_advantage >= -10 else -3
    offense_score = 5 if offense >= target_bulk else 2 if offense + 15 >= target_bulk else -2
    bulk_score = 5 if bulk >= 90 else 2 if bulk >= 70 else -2
    weakness_penalty = 8 if defense_multiplier > 1 else 0

    if selection_mode == "fast_win":
        raw_score = type_score * 1.8 + speed_score * 1.4 + offense_score * 1.5 - weakness_penalty
    else:
        raw_score = type_score + resistance_score * 1.5 + bulk_score + speed_score + offense_score - weakness_penalty

    return {
        "target_name": target.get("pokemon") or target.get("name") or "Unknown",
        "target_key": _target_key(target),
        "target_image_url": target.get("sprite_url") or target.get("image_url"),
        "target_types": target_types,
        "offense_multiplier": offense_multiplier,
        "defense_multiplier": defense_multiplier,
        "speed_advantage": speed_advantage,
        "bulk": bulk,
        "raw_score": raw_score,
    }


def _matchup_reason(
    challenger: dict[str, Any],
    matchup: dict[str, Any],
    selection_mode: str,
    recommended_move: dict[str, Any],
) -> str:
    mode = "quick knockout pressure" if selection_mode == "fast_win" else "safe counter value"
    pieces = [f"{challenger['pokemon']} is recommended for {mode} against {matchup['target_name']}"]
    if recommended_move["multiplier"] > 1:
        pieces.append(f"because {recommended_move['move']} hits super-effectively")
    elif matchup["offense_multiplier"] > 1:
        pieces.append("because its typing can pressure the target super-effectively")
    if matchup["defense_multiplier"] == 0:
        pieces.append("and it has an immunity in this matchup")
    elif matchup["defense_multiplier"] < 1:
        pieces.append("and it resists the target's likely attacks")
    elif matchup["defense_multiplier"] > 1:
        pieces.append("but it should watch for super-effective retaliation")
    if matchup["speed_advantage"] > 0:
        pieces.append("while also moving first")
    return ", ".join(pieces) + "."


def _suggested_sequence(
    challenger: dict[str, Any],
    matchup: dict[str, Any],
    selection_mode: str,
    recommended_move: dict[str, Any],
) -> list[str]:
    sequence = [f"Use {challenger['pokemon']} against {matchup['target_name']} when this matchup appears."]
    if recommended_move["type"]:
        move_detail = f"Open with {recommended_move['move']} ({recommended_move['type']}-type)."
    else:
        move_detail = f"Open with {recommended_move['move']}."
    sequence.append(move_detail)
    if recommended_move["multiplier"] > 1:
        sequence.append(f"{recommended_move['move']} is the best current move because it is super-effective here.")
    elif recommended_move["stab"]:
        sequence.append(f"{recommended_move['move']} is preferred because it gets STAB from {challenger['pokemon']}.")
    else:
        sequence.append(f"{recommended_move['move']} is the safest available move from this set.")
    if matchup["speed_advantage"] > 0:
        sequence.append("Use this Pokemon early to pressure the opponent before it can move.")
    if matchup["bulk"] >= 80:
        sequence.append("This Pokemon can safely absorb hits before attacking.")
    if matchup["defense_multiplier"] > 1:
        sequence.append("Avoid staying in if the opponent has super-effective coverage.")
    if selection_mode == "fast_win":
        sequence.append("Use aggressive attacks first to secure a quick knockout.")
    else:
        sequence.append("Use this matchup as a safe counter and preserve HP when possible.")
    return sequence


def _select_recommended_move(
    challenger: dict[str, Any],
    matchup: dict[str, Any],
    selection_mode: str,
) -> dict[str, Any]:
    moves = challenger.get("moves") or []
    challenger_types = _types_from_recommendation(challenger)
    target_types = matchup["target_types"]
    scored_moves = [_score_move(move, challenger_types, target_types, selection_mode) for move in moves]
    if not scored_moves:
        return {"move": "Best available attack", "type": None, "multiplier": 1, "stab": False}
    return max(scored_moves, key=lambda item: item["score"])


def _score_move(
    move: str,
    challenger_types: list[str],
    target_types: list[str],
    selection_mode: str,
) -> dict[str, Any]:
    move_type = MOVE_TYPES.get(move)
    if not move_type:
        utility_bonus = 4 if move in STATUS_MOVES and selection_mode == "balanced" else -4
        return {"move": move, "type": None, "multiplier": 1, "stab": False, "score": utility_bonus}

    multiplier = _attack_multiplier(move_type, target_types)
    stab = move_type in challenger_types
    score = multiplier * 10
    if stab:
        score += 4
    if multiplier > 1:
        score += 8
    if multiplier == 0:
        score -= 30
    if selection_mode == "fast_win" and multiplier >= 1:
        score += 3
    return {"move": move, "type": move_type, "multiplier": multiplier, "stab": stab, "score": score}


def _types_from_recommendation(pokemon: dict[str, Any]) -> list[str]:
    return [pokemon_type for pokemon_type in pokemon.get("types", []) if pokemon_type]


def _types_from_entry(pokemon: dict[str, Any]) -> list[str]:
    return [pokemon_type for pokemon_type in [pokemon.get("type_1"), pokemon.get("type_2")] if pokemon_type]


def _target_key(pokemon: dict[str, Any]) -> str:
    return str(pokemon.get("pokemon") or pokemon.get("name") or "").strip().lower()


def _attack_multiplier(attack_type: str, defender_types: list[str]) -> float:
    multiplier = 1.0
    for defender_type in defender_types:
        multiplier *= TYPE_EFFECTIVENESS.get(attack_type, {}).get(defender_type, 1)
    return multiplier


def _bulk(pokemon: dict[str, Any]) -> float:
    return (
        int(pokemon.get("hp") or 75)
        + int(pokemon.get("defense") or 75)
        + int(pokemon.get("special_defense") or 75)
    ) / 3


def _normalize_score(score: float) -> int:
    return max(0, min(100, round(55 + score * 2.2)))
