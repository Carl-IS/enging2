import { useEffect, useMemo, useState } from "react";
import gachaponBackground from "../assets/gachapon/gachapon-background.png";
import gachaponSpotlight from "../assets/gachapon/gachapon-spotlight.png";

const OPENING_DURATION_MS = 500;
const SHADOW_DURATION_MS = 300;

function pokemonImage(pokemon) {
  return pokemon?.image_url || pokemon?.sprite_url || "";
}

function pokemonTypes(pokemon) {
  if (pokemon?.types?.length) {
    return pokemon.types.join(" / ");
  }

  return [pokemon?.type_1, pokemon?.type_2].filter(Boolean).join(" / ");
}

function PokemonRevealImage({ pokemon, isShadow }) {
  const image = pokemonImage(pokemon);

  if (!image) {
    return (
      <div className={`pokemon-reveal-placeholder${isShadow ? " pokemon-silhouette" : " pokemon-revealed"}`}>
        {isShadow ? "?" : pokemon?.pokemon}
      </div>
    );
  }

  return (
    <img
      className={isShadow ? "pokemon-silhouette" : "pokemon-revealed"}
      src={image}
      alt={pokemon.pokemon}
    />
  );
}

function Pokeball({ className = "" }) {
  return (
    <div className={`pokeball ${className}`}>
      <div className="pokeball-top"></div>
      <div className="pokeball-bottom"></div>
      <div className="pokeball-center"></div>
    </div>
  );
}

export default function GachaponPull({ loading, error, results, onViewResults, onRetry }) {
  const team = useMemo(() => results?.recommended_team || [], [results]);
  const [phase, setPhase] = useState("pulling");
  const [currentRevealIndex, setCurrentRevealIndex] = useState(0);
  const [revealedCount, setRevealedCount] = useState(0);
  const [isShadow, setIsShadow] = useState(true);

  useEffect(() => {
    if (loading || error || !team.length) {
      setPhase("pulling");
      setCurrentRevealIndex(0);
      setRevealedCount(0);
      setIsShadow(true);
      return undefined;
    }

    setPhase("opening");
    setCurrentRevealIndex(0);
    setRevealedCount(0);
    setIsShadow(true);

    const openingTimer = window.setTimeout(() => {
      setPhase("revealing");
    }, OPENING_DURATION_MS);

    return () => window.clearTimeout(openingTimer);
  }, [loading, error, team]);

  useEffect(() => {
    if (phase !== "revealing" || !team.length) {
      return undefined;
    }

    setIsShadow(true);
    const shadowTimer = window.setTimeout(() => {
      setIsShadow(false);
    }, SHADOW_DURATION_MS);

    return () => {
      window.clearTimeout(shadowTimer);
    };
  }, [phase, currentRevealIndex, team]);

  function handleNextReveal() {
    const nextCount = currentRevealIndex + 1;
    setRevealedCount(nextCount);

    if (nextCount >= team.length) {
      setPhase("complete");
      return;
    }

    setCurrentRevealIndex(nextCount);
  }

  const currentPokemon = team[currentRevealIndex];

  return (
    <main className="gachapon-page" style={{ "--gachapon-bg": `url(${gachaponBackground})` }}>
      <section className="gachapon-card">
        {error && (
          <div className="error-box">
            <h2>Pull Failed</h2>
            <p>{error}</p>
            <button type="button" onClick={onRetry} disabled={loading}>
              {loading ? "Trying..." : "Try Again"}
            </button>
          </div>
        )}

        {!error && phase === "pulling" && (
          <>
            <Pokeball className="shaking" />
            <h1>Pulling Challenger Lineup...</h1>
            <p>Analyzing matchup and counter options.</p>
          </>
        )}

        {!error && phase === "opening" && (
          <>
            <Pokeball className="opening" />
            <h1>Opening Poke Ball...</h1>
            <p>Your recommended team is ready to reveal.</p>
          </>
        )}

        {!error && phase === "revealing" && currentPokemon && (
          <section className="reveal-screen">
            <div className="reveal-visual">
              <img className="spotlight" src={gachaponSpotlight} alt="" aria-hidden="true" />
              <PokemonRevealImage pokemon={currentPokemon} isShadow={isShadow} />
            </div>
            <div className="reveal-copy">
              {!isShadow && <h1>{currentPokemon.pokemon}</h1>}
              {!isShadow && <p>Counter Score: {currentPokemon.counter_score}</p>}
              <span className="reveal-count">{currentRevealIndex + 1} / {team.length}</span>
              {!isShadow && (
                <button className="reveal-next-button" type="button" onClick={handleNextReveal}>
                  {currentRevealIndex + 1 >= team.length ? "Finish Reveal" : "Next"}
                </button>
              )}
            </div>
          </section>
        )}

        {!error && phase === "complete" && (
          <>
            <h1>Challenger Lineup Revealed!</h1>
            <div className="revealed-team-grid">
              {team.map((pokemon) => (
                <div className="revealed-mini-card" key={pokemon.pokemon}>
                  {pokemonImage(pokemon) ? (
                    <img src={pokemonImage(pokemon)} alt={pokemon.pokemon} />
                  ) : (
                    <div className="revealed-placeholder">{pokemon.pokemon.charAt(0)}</div>
                  )}
                  <h3>{pokemon.pokemon}</h3>
                  <p>{pokemonTypes(pokemon) || "-"}</p>
                  <p>Score: {pokemon.counter_score}</p>
                </div>
              ))}
            </div>
            <button type="button" onClick={onViewResults}>View Full Results</button>
          </>
        )}
      </section>
    </main>
  );
}
