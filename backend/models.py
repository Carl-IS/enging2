from typing import Literal

from pydantic import BaseModel, Field


AllowedChallengerRegion = Literal["Hoenn", "Sinnoh", "Galar"]
SelectionMode = Literal["balanced", "fast_win"]


class RecommendRequest(BaseModel):
    gym_leader_name: str = Field(..., min_length=1)
    gym_leader_region: str = Field(..., min_length=1)
    gym_leader_type: str = Field(..., min_length=1)
    gym_leader_team: list[str] = Field(..., min_length=6, max_length=6)
    challenger_region: AllowedChallengerRegion
    selection_mode: SelectionMode = "fast_win"


class GymLeaderPokemon(BaseModel):
    pokemon: str
    sprite_url: str | None = None


class PokemonStats(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class ScoreComponents(BaseModel):
    type_offense: int
    defensive_resistance: int
    stat_matchup: int
    speed: int
    team_coverage: int
    role_balance: int
    weakness_penalty: int
    diversity_adjustment: int


class RecommendedPokemon(BaseModel):
    pokemon: str
    native_region: str
    is_backup: bool = False
    backup_note: str | None = None
    sprite_url: str | None = None
    types: list[str]
    role: str
    gender: str
    item: str
    ability: str
    evs: str
    nature: str
    moves: list[str]
    stats: PokemonStats
    counter_score: int
    score_components: ScoreComponents
    reason_selected: str


class BattlePlanItem(BaseModel):
    challenger_pokemon: str
    challenger_image_url: str | None = None
    best_match_against: str
    best_match_image_url: str | None = None
    matchup_score: int
    recommended_move: str
    recommended_move_type: str | None = None
    reason: str
    suggested_sequence: list[str]


class RecommendResponse(BaseModel):
    target_gym_leader: str
    gym_leader_team: list[GymLeaderPokemon]
    challenger_region: AllowedChallengerRegion
    model_used: str
    generated_at: str
    backup_used: bool = False
    backup_note: str | None = None
    recommended_team: list[RecommendedPokemon]
    battle_plan: list[BattlePlanItem] = []
