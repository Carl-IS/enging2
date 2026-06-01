from data_loader import REGION_DEX_RANGES, load_region_pokemon_data
from filters import apply_native_region_filter, apply_restriction_filter


REGION_ORDER = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar", "Paldea"]


def main() -> None:
    print("Populating pokemon_cache.csv from PokeAPI...")
    for region in REGION_ORDER:
      pokemon = load_region_pokemon_data(region)
      region_pool = apply_native_region_filter(pokemon, region)
      eligible_pool = apply_restriction_filter(region_pool, [])
      expected = len(REGION_DEX_RANGES[region])
      print(f"{region}: cached {len(region_pool)}/{expected}, eligible {len(eligible_pool)}")
    print("Done.")


if __name__ == "__main__":
    main()
