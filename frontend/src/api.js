const API_BASE_URL = "http://localhost:8000";
const API_URL = `${API_BASE_URL}/recommend`;

export async function generateChallengerLineup(payload) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Unable to generate challenger lineup.");
  }

  return data;
}

export async function fetchAvailableGymPokemon(region, type) {
  const params = new URLSearchParams({ region, type });
  const response = await fetch(`${API_BASE_URL}/available-gym-pokemon?${params.toString()}`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Unable to load recommended Gym Leader Pokemon.");
  }

  return data;
}

export async function fetchPokemonLookup(name) {
  const params = new URLSearchParams({ name });
  const response = await fetch(`${API_BASE_URL}/pokemon-lookup?${params.toString()}`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Unable to load Pokemon preview.");
  }

  return data;
}
