import csv
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from battle_plan import generate_battle_plan
from data_loader import build_team_display, load_pokemon_by_name, load_region_pokemon_data, load_region_type_pokemon_data
from filters import apply_native_region_filter, apply_restriction_filter
from models import RecommendRequest, RecommendResponse
from scoring import recommend_top_six


LOG_PATH = Path(__file__).resolve().parent / "logs" / "challenger_outputs.csv"
MODEL_NAMES = {
    "balanced": "Balanced Counter Mode",
    "fast_win": "Fast-Win Race Mode",
}
MIN_BACKUP_SCORE = {
    "balanced": 70,
    "fast_win": 75,
}
GYM_TEAM_SCORE_FIELDS = ("hp", "attack", "defense", "special_attack", "special_defense", "speed")

app = FastAPI(title="Challenger Selection Engine - Engine 2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/available-gym-pokemon")
def available_gym_pokemon(region: str, type: str) -> list[dict[str, object]]:
    pokemon = load_region_type_pokemon_data(region, type)
    region_pool = apply_native_region_filter(pokemon, region)
    eligible_pool = apply_restriction_filter(region_pool, [])
    target_type = type.strip().lower()

    matches = [
        entry
        for entry in eligible_pool
        if entry.get("type_1", "").lower() == target_type
        or entry.get("type_2", "").lower() == target_type
    ]

    matches.sort(key=_gym_team_candidate_sort_key)
    return [
        {
            "name": entry["pokemon"],
            "native_region": entry["native_region"],
            "type_1": entry["type_1"],
            "type_2": entry.get("type_2") or None,
            "image_url": entry.get("sprite_url"),
            "hp": entry["hp"],
            "attack": entry["attack"],
            "defense": entry["defense"],
            "special_attack": entry["special_attack"],
            "special_defense": entry["special_defense"],
            "speed": entry["speed"],
            "base_stat_total": _base_stat_total(entry),
            "gym_candidate_score": _gym_team_candidate_score(entry),
        }
        for entry in matches
    ]


@app.get("/pokemon-lookup")
def pokemon_lookup(name: str) -> dict[str, object]:
    entry = load_pokemon_by_name(name)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' was not found.")

    return {
        "name": entry["pokemon"],
        "native_region": entry["native_region"],
        "type_1": entry["type_1"],
        "type_2": entry.get("type_2") or None,
        "image_url": entry.get("sprite_url"),
        "hp": entry["hp"],
        "attack": entry["attack"],
        "defense": entry["defense"],
        "special_attack": entry["special_attack"],
        "special_defense": entry["special_defense"],
        "speed": entry["speed"],
        "base_stat_total": _base_stat_total(entry),
        "gym_candidate_score": _gym_team_candidate_score(entry),
    }


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest) -> RecommendResponse:
    pokemon = load_region_pokemon_data(request.challenger_region)
    region_pool = apply_native_region_filter(pokemon, request.challenger_region)

    if not region_pool:
        raise HTTPException(
            status_code=404,
            detail=f"No Pokemon data available for challenger region '{request.challenger_region}'.",
        )

    eligible_pool = apply_restriction_filter(region_pool, request.gym_leader_team)
    backup_used = False
    backup_note = None

    recommended_team = recommend_top_six(
        eligible_pool,
        request.gym_leader_type,
        request.gym_leader_team,
        pokemon,
        request.selection_mode,
    )
    gym_leader_team_data = _resolve_gym_leader_team_data(request.gym_leader_team, request.gym_leader_type)
    battle_plan = generate_battle_plan(recommended_team, gym_leader_team_data, request.selection_mode)

    if len(recommended_team) < 6:
        backup_used = True
        backup_note = (
            f"Only {len(recommended_team)} legal native {request.challenger_region} Pokemon were available. "
            "No cross-region backups were added because backup Pokemon must be from the same challenger region."
        )
    generated_at = datetime.now(timezone.utc).isoformat()

    response = RecommendResponse(
        target_gym_leader=request.gym_leader_name,
        gym_leader_team=build_team_display(request.gym_leader_team, pokemon),
        challenger_region=request.challenger_region,
        model_used=MODEL_NAMES[request.selection_mode],
        generated_at=generated_at,
        backup_used=backup_used,
        backup_note=backup_note,
        recommended_team=recommended_team,
        battle_plan=battle_plan,
    )
    save_output_log(request, response)
    return response


def _resolve_gym_leader_team_data(team_names: list[str], gym_leader_type: str) -> list[dict[str, object]]:
    resolved_team = []
    for name in team_names:
        resolved = load_pokemon_by_name(name)
        if resolved:
            resolved_team.append(resolved)
        else:
            resolved_team.append(
                {
                    "pokemon": name,
                    "sprite_url": None,
                    "type_1": gym_leader_type.strip().title(),
                    "type_2": "",
                    "hp": 75,
                    "attack": 75,
                    "defense": 75,
                    "special_attack": 75,
                    "special_defense": 75,
                    "speed": 75,
                }
            )
    return resolved_team


def _base_stat_total(pokemon: dict[str, object]) -> int:
    return sum(int(pokemon.get(field) or 0) for field in GYM_TEAM_SCORE_FIELDS)


def _gym_team_candidate_score(pokemon: dict[str, object]) -> int:
    offense = max(int(pokemon.get("attack") or 0), int(pokemon.get("special_attack") or 0))
    bulk = (
        int(pokemon.get("hp") or 0)
        + int(pokemon.get("defense") or 0)
        + int(pokemon.get("special_defense") or 0)
    )
    speed = int(pokemon.get("speed") or 0)
    return _base_stat_total(pokemon) + offense + (bulk // 3) + speed


def _gym_team_candidate_sort_key(pokemon: dict[str, object]) -> tuple[int, int, str]:
    return (
        -_gym_team_candidate_score(pokemon),
        -_base_stat_total(pokemon),
        str(pokemon.get("pokemon", "")),
    )


def save_output_log(request: RecommendRequest, response: RecommendResponse) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not LOG_PATH.exists() or LOG_PATH.stat().st_size == 0

    with LOG_PATH.open("a", newline="", encoding="utf-8") as log_file:
        writer = csv.DictWriter(
            log_file,
            fieldnames=[
                "generated_at",
                "gym_leader_name",
                "gym_leader_region",
                "gym_leader_type",
                "gym_leader_team",
                "challenger_region",
                "model_used",
                "selection_mode",
                "backup_used",
                "backup_note",
                "recommended_team",
            ],
        )
        if write_header:
            writer.writeheader()
        writer.writerow(
            {
                "generated_at": response.generated_at,
                "gym_leader_name": request.gym_leader_name,
                "gym_leader_region": request.gym_leader_region,
                "gym_leader_type": request.gym_leader_type,
                "gym_leader_team": ", ".join(request.gym_leader_team),
                "challenger_region": request.challenger_region,
                "model_used": response.model_used,
                "selection_mode": request.selection_mode,
                "backup_used": response.backup_used,
                "backup_note": response.backup_note or "",
                "recommended_team": ", ".join(member.pokemon for member in response.recommended_team),
            }
        )
