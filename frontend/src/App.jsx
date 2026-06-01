import { useEffect, useState } from "react";
import { fetchAvailableGymPokemon, fetchPokemonLookup, generateChallengerLineup } from "./api";
import BattlePlanModal from "./components/BattlePlanModal";
import GachaponPull from "./components/GachaponPull";
import TrainerIdModal from "./components/TrainerIdModal";
import normalIcon from "./assets/type-icons/normal.png";
import fireIcon from "./assets/type-icons/fire.png";
import waterIcon from "./assets/type-icons/water.png";
import electricIcon from "./assets/type-icons/electric.png";
import grassIcon from "./assets/type-icons/grass.png";
import iceIcon from "./assets/type-icons/ice.png";
import fightingIcon from "./assets/type-icons/fighting.png";
import poisonIcon from "./assets/type-icons/poison.png";
import groundIcon from "./assets/type-icons/ground.png";
import flyingIcon from "./assets/type-icons/flying.png";
import psychicIcon from "./assets/type-icons/psychic.png";
import bugIcon from "./assets/type-icons/bug.png";
import rockIcon from "./assets/type-icons/rock.png";
import ghostIcon from "./assets/type-icons/ghost.png";
import dragonIcon from "./assets/type-icons/dragon.png";
import darkIcon from "./assets/type-icons/dark.png";
import steelIcon from "./assets/type-icons/steel.png";
import fairyIcon from "./assets/type-icons/fairy.png";

const REGIONS = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar", "Paldea"];
const CHALLENGER_REGIONS = ["Hoenn", "Sinnoh", "Galar"];
const TYPES = [
  "Normal",
  "Fire",
  "Water",
  "Electric",
  "Grass",
  "Ice",
  "Fighting",
  "Poison",
  "Ground",
  "Flying",
  "Psychic",
  "Bug",
  "Rock",
  "Ghost",
  "Dragon",
  "Dark",
  "Steel",
  "Fairy"
];
const TYPE_COLORS = {
  Normal: "#A8A77A",
  Fire: "#EE8130",
  Water: "#6390F0",
  Electric: "#F7D02C",
  Grass: "#7AC74C",
  Ice: "#96D9D6",
  Fighting: "#C22E28",
  Poison: "#A33EA1",
  Ground: "#E2BF65",
  Flying: "#A98FF3",
  Psychic: "#F95587",
  Bug: "#A6B91A",
  Rock: "#B6A136",
  Ghost: "#735797",
  Dragon: "#6F35FC",
  Dark: "#705746",
  Steel: "#B7B7CE",
  Fairy: "#D685AD"
};
const TYPE_ICONS = {
  Normal: normalIcon,
  Fire: fireIcon,
  Water: waterIcon,
  Electric: electricIcon,
  Grass: grassIcon,
  Ice: iceIcon,
  Fighting: fightingIcon,
  Poison: poisonIcon,
  Ground: groundIcon,
  Flying: flyingIcon,
  Psychic: psychicIcon,
  Bug: bugIcon,
  Rock: rockIcon,
  Ghost: ghostIcon,
  Dragon: dragonIcon,
  Dark: darkIcon,
  Steel: steelIcon,
  Fairy: fairyIcon
};
const SELECTION_MODES = [
  {
    label: "Balanced Counter Mode",
    value: "balanced",
    description: "Prioritizes safer counters using type advantage, resistance, bulk, stat balance, and team diversity."
  },
  {
    label: "Fast-Win Race Mode",
    value: "fast_win",
    description: "Prioritizes quick victories using super-effective damage, speed, offensive stats, STAB, and fast knockout potential."
  }
];
const POKEMON_FIELDS = ["pokemon_1", "pokemon_2", "pokemon_3", "pokemon_4", "pokemon_5", "pokemon_6"];

const INITIAL_FORM = {
  gym_leader_name: "",
  gym_leader_region: "",
  gym_leader_type: "",
  challenger_region: "",
  selection_mode: "fast_win",
  pokemon_1: "",
  pokemon_2: "",
  pokemon_3: "",
  pokemon_4: "",
  pokemon_5: "",
  pokemon_6: ""
};

const QUICK_GENERATE_FORM = {
  gym_leader_name: "Juan",
  gym_leader_region: "Kanto",
  gym_leader_type: "Electric",
  challenger_region: "Hoenn",
  selection_mode: "fast_win",
  pokemon_1: "Pikachu",
  pokemon_2: "Raichu",
  pokemon_3: "Electabuzz",
  pokemon_4: "Magneton",
  pokemon_5: "Voltorb",
  pokemon_6: "Electrode"
};

function PokemonImage({ src, name }) {
  if (!src) {
    return <div className="pokemon-image placeholder">?</div>;
  }

  return <img className="pokemon-image" src={src} alt={name} loading="lazy" />;
}

function OptionCard({ title, description, selected, onClick }) {
  return (
    <button className={`option-card${selected ? " selected" : ""}`} type="button" onClick={onClick}>
      <span>{title}</span>
      {description && <small>{description}</small>}
    </button>
  );
}

function PreviousAnswers({ currentStep, form, onJump }) {
  const team = POKEMON_FIELDS.map((field) => form[field].trim()).filter(Boolean);
  const selectedMode = SELECTION_MODES.find((mode) => mode.value === form.selection_mode);
  const answers = [
    { step: 1, label: "Name", value: form.gym_leader_name },
    { step: 2, label: "Gym Region", value: form.gym_leader_region },
    { step: 3, label: "Type", value: form.gym_leader_type },
    { step: 4, label: "Gym Team", value: team.length ? team.join(", ") : "" },
    { step: 5, label: "Challenger Region", value: form.challenger_region },
    { step: 6, label: "Method", value: selectedMode?.label || "" }
  ].filter((answer) => answer.step < currentStep && answer.value);

  if (!answers.length) {
    return null;
  }

  return (
    <section className="previous-answers" aria-label="Previous answers">
      <h2>Edit</h2>
      <div className="answer-chip-grid">
        {answers.map((answer) => (
          <button className="answer-chip" key={answer.step} type="button" onClick={() => onJump(answer.step)}>
            <span>{answer.label}</span>
          </button>
        ))}
      </div>
    </section>
  );
}

function TypeCard({ type, selected, onClick }) {
  return (
    <button
      className={`type-choice${selected ? " selected" : ""}`}
      type="button"
      onClick={onClick}
      style={{
        "--type-color": TYPE_COLORS[type],
        "--type-text": "#ffffff"
      }}
    >
      <img className="type-icon" src={TYPE_ICONS[type]} alt={`${type} type icon`} />
      <span className={`type-card${selected ? " selected" : ""}`}>
        <span className="type-name">{type}</span>
      </span>
    </button>
  );
}

function TypeBadge({ type }) {
  if (!type || type === "-") {
    return <span className="result-type-badge empty">-</span>;
  }

  return (
    <span className="result-type-badge" style={{ "--type-color": TYPE_COLORS[type] || "#687586" }}>
      {type}
    </span>
  );
}

function PokemonComboCard({ field, index, value, option, options, isOpen, isResolving, lookupError, onChange, onSelect, onManualLookup, onOpen, onToggle }) {
  const query = value.trim().toLowerCase();
  const filteredOptions = query
    ? options.filter((pokemon) => pokemon.name.toLowerCase().startsWith(query))
    : options;

  function handleKeyDown(event) {
    if (event.key !== "Enter") {
      return;
    }

    event.preventDefault();
    if (filteredOptions.length > 0) {
      onSelect(field, filteredOptions[0].name);
    } else if (value.trim()) {
      onManualLookup(field, value.trim());
    }
  }

  function handleBlur() {
    if (value.trim() && !option) {
      onManualLookup(field, value.trim());
    }
  }

  function handleSelect(pokemonName) {
    onSelect(field, pokemonName);
  }

  function handlePreviewKeyDown(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      onManualLookup(field, value.trim());
    }
  }

  return (
    <section className="pokemon-slot-card">
      <label>
        Pokemon {index + 1}
        <div className="combo-box">
          <input
            name={field}
              value={value}
              onChange={onChange}
              onFocus={() => onOpen(field)}
              onBlur={handleBlur}
              onKeyDown={handleKeyDown}
              placeholder="Type or choose a Pokemon"
            />
          <button className="combo-toggle" type="button" onClick={() => onToggle(field)} aria-label={`Show recommendations for Pokemon ${index + 1}`}>
            ▾
          </button>
        </div>
      </label>
      {isOpen && (
        <div className="combo-menu">
          {filteredOptions.length > 0 ? (
              filteredOptions.map((pokemon) => (
                <button key={pokemon.name} type="button" onMouseDown={(event) => event.preventDefault()} onClick={() => handleSelect(pokemon.name)}>
                <span>{pokemon.name}</span>
                <small>{pokemon.native_region} • {pokemon.type_1}{pokemon.type_2 ? ` / ${pokemon.type_2}` : ""}</small>
              </button>
            ))
          ) : (
            <p>No matching recommendation. Press Next after typing manually.</p>
          )}
        </div>
      )}
      {option ? (
        <div className="pokemon-preview">
          <PokemonImage src={option.image_url} name={option.name} />
          <div>
            <strong>{option.name}</strong>
            <span>{option.native_region}</span>
            <span>{option.type_1}{option.type_2 ? ` / ${option.type_2}` : ""}</span>
          </div>
        </div>
        ) : (
          <p className="manual-entry" tabIndex="0" onKeyDown={handlePreviewKeyDown}>
            {isResolving ? "Loading preview..." : lookupError || "Manual entry"}
          </p>
        )}
      </section>
    );
  }

function StepNavigation({ canContinue = true, nextLabel = "Next", onBack, onNext, isLoading }) {
  return (
    <div className="step-navigation">
      {onBack && <button className="ghost-button" type="button" onClick={onBack}>Back</button>}
      <button type="button" onClick={onNext} disabled={!canContinue || isLoading}>
        {isLoading ? "Generating..." : nextLabel}
      </button>
    </div>
  );
}

function buildShowdownExport(team) {
  return team.map((member) => {
    const gender = member.gender ? ` (${member.gender})` : "";
    const item = member.item ? ` @ ${member.item}` : "";
    const ability = member.ability ? `Ability: ${member.ability}` : "";
    const evs = member.evs ? `EVs: ${member.evs}` : "";
    const nature = member.nature ? `${member.nature} Nature` : "";
    const moves = (member.moves || []).map((move) => `- ${move}`).join("\n");
    return [`${member.pokemon}${gender}${item}`, ability, evs, nature, moves].filter(Boolean).join("\n");
  }).join("\n\n");
}

function buildPayload(formData) {
  return {
    gym_leader_name: formData.gym_leader_name.trim(),
    gym_leader_region: formData.gym_leader_region,
    gym_leader_type: formData.gym_leader_type,
    gym_leader_team: POKEMON_FIELDS.map((field) => formData[field].trim()),
    challenger_region: formData.challenger_region,
    selection_mode: formData.selection_mode
  };
}

function splitTypes(types = []) {
  return {
    type1: types[0] || "-",
    type2: types[1] || "-"
  };
}

export default function App() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copyStatus, setCopyStatus] = useState("");
  const [isBattlePlanOpen, setIsBattlePlanOpen] = useState(false);
  const [isTrainerIdOpen, setIsTrainerIdOpen] = useState(false);
  const [showLanding, setShowLanding] = useState(true);
  const [step, setStep] = useState(1);
  const [recommendedPokemonOptions, setRecommendedPokemonOptions] = useState([]);
  const [isLoadingOptions, setIsLoadingOptions] = useState(false);
  const [optionsError, setOptionsError] = useState("");
  const [openComboField, setOpenComboField] = useState("");
  const [manualPokemonPreviews, setManualPokemonPreviews] = useState({});
  const [manualLookupErrors, setManualLookupErrors] = useState({});
  const [resolvingManualFields, setResolvingManualFields] = useState({});

  useEffect(() => {
    if (step !== 4 || !form.gym_leader_region || !form.gym_leader_type) {
      return;
    }

    let isCurrent = true;
    setIsLoadingOptions(true);
    setOptionsError("");

    fetchAvailableGymPokemon(form.gym_leader_region, form.gym_leader_type)
      .then((options) => {
        if (isCurrent) {
          setRecommendedPokemonOptions(options);
        }
      })
      .catch((requestError) => {
        if (isCurrent) {
          setRecommendedPokemonOptions([]);
          setOptionsError(requestError.message);
        }
      })
      .finally(() => {
        if (isCurrent) {
          setIsLoadingOptions(false);
        }
      });

    return () => {
      isCurrent = false;
    };
  }, [step, form.gym_leader_region, form.gym_leader_type]);

  function updateField(event) {
    const { name, value } = event.target;
    setOpenComboField(event.target.name);
    setForm((current) => ({
      ...current,
      [name]: value
    }));
    setManualLookupErrors((current) => ({ ...current, [name]: "" }));
    setManualPokemonPreviews((current) => {
      if (!current[name] || current[name].name.toLowerCase() === value.trim().toLowerCase()) {
        return current;
      }

      const next = { ...current };
      delete next[name];
      return next;
    });
  }

  function updateValue(name, value) {
    setForm((current) => ({
      ...current,
      [name]: value
    }));
    setManualLookupErrors((current) => ({ ...current, [name]: "" }));
    setManualPokemonPreviews((current) => {
      const next = { ...current };
      delete next[name];
      return next;
    });
    setOpenComboField("");
  }

  async function resolveManualPokemon(field, pokemonName) {
    const trimmedName = pokemonName.trim();
    if (!trimmedName) {
      return;
    }

    setResolvingManualFields((current) => ({ ...current, [field]: true }));
    setManualLookupErrors((current) => ({ ...current, [field]: "" }));

    try {
      const preview = await fetchPokemonLookup(trimmedName);
      setForm((current) => ({ ...current, [field]: preview.name }));
      setManualPokemonPreviews((current) => ({ ...current, [field]: preview }));
      setOpenComboField("");
    } catch {
      setManualPokemonPreviews((current) => {
        const next = { ...current };
        delete next[field];
        return next;
      });
      setManualLookupErrors((current) => ({ ...current, [field]: "Pokemon not found. Manual entry will still be used." }));
    } finally {
      setResolvingManualFields((current) => ({ ...current, [field]: false }));
    }
  }

  async function requestLineup(formData, options = {}) {
    const skipAnimation = Boolean(options.skipAnimation);
    setError("");
    setResult(null);
    setIsLoading(true);
    setCopyStatus("");
    setShowLanding(false);
    setStep(skipAnimation ? 8 : 7);

    try {
      const data = await generateChallengerLineup(buildPayload(formData));
      setResult(data);
      setIsLoading(false);
      if (skipAnimation) {
        setStep(8);
      }
    } catch (requestError) {
      setError(requestError.message);
      setIsLoading(false);
    }
  }

  function startOver() {
    setForm(INITIAL_FORM);
    setResult(null);
    setError("");
    setCopyStatus("");
    setIsBattlePlanOpen(false);
    setIsTrainerIdOpen(false);
    setShowLanding(false);
    setStep(1);
  }

  function createTeam() {
    setForm(INITIAL_FORM);
    setResult(null);
    setError("");
    setCopyStatus("");
    setIsBattlePlanOpen(false);
    setIsTrainerIdOpen(false);
    setShowLanding(false);
    setStep(1);
  }

  function backToHome() {
    setError("");
    setCopyStatus("");
    setIsBattlePlanOpen(false);
    setIsTrainerIdOpen(false);
    setShowLanding(true);
  }

  async function handleQuickGenerate() {
    setForm(QUICK_GENERATE_FORM);
    await requestLineup(QUICK_GENERATE_FORM, { skipAnimation: true });
  }

  async function copyShowdownTeam() {
    if (!result) {
      return;
    }

    const exportText = buildShowdownExport(result.recommended_team);

    try {
      await navigator.clipboard.writeText(exportText);
      setCopyStatus("Copied for Pokemon Showdown");
    } catch {
      setCopyStatus(exportText);
    }
  }

  function autofillRecommendedPokemon() {
    setForm((current) => {
      const nextForm = { ...current };
      const usedNames = new Set(
        POKEMON_FIELDS.map((field) => current[field].trim().toLowerCase()).filter(Boolean)
      );
      let optionIndex = 0;

      POKEMON_FIELDS.forEach((field) => {
        if (nextForm[field].trim()) {
          return;
        }

        while (
          optionIndex < recommendedPokemonOptions.length
          && usedNames.has(recommendedPokemonOptions[optionIndex].name.toLowerCase())
        ) {
          optionIndex += 1;
        }

        if (optionIndex < recommendedPokemonOptions.length) {
          const name = recommendedPokemonOptions[optionIndex].name;
          nextForm[field] = name;
          usedNames.add(name.toLowerCase());
          optionIndex += 1;
        }
      });

      return nextForm;
    });
    setOpenComboField("");
  }

  function renderStep() {
    if (step === 1) {
      return (
        <section className="wizard-card">
          <p className="step-count">Step 1 of 6</p>
          <h1>Gym Leader Name</h1>
          <label>
            Gym Leader Name
            <input name="gym_leader_name" value={form.gym_leader_name} onChange={updateField} autoFocus />
          </label>
          <StepNavigation canContinue={form.gym_leader_name.trim().length > 0} onNext={() => setStep(2)} />
        </section>
      );
    }

    if (step === 2) {
      return (
        <section className="wizard-card">
          <p className="step-count">Step 2 of 6</p>
          <h1>Select Gym Leader Region</h1>
          <div className="option-grid region-grid">
            {REGIONS.map((region) => (
              <OptionCard key={region} title={region} selected={form.gym_leader_region === region} onClick={() => updateValue("gym_leader_region", region)} />
            ))}
          </div>
          <StepNavigation canContinue={Boolean(form.gym_leader_region)} onBack={() => setStep(1)} onNext={() => setStep(3)} />
        </section>
      );
    }

    if (step === 3) {
      return (
        <section className="wizard-card">
          <p className="step-count">Step 3 of 6</p>
          <h1>Select Gym Leader Type</h1>
          <div className="option-grid type-grid">
            {TYPES.map((type) => (
              <TypeCard key={type} type={type} selected={form.gym_leader_type === type} onClick={() => updateValue("gym_leader_type", type)} />
            ))}
          </div>
          <StepNavigation canContinue={Boolean(form.gym_leader_type)} onBack={() => setStep(2)} onNext={() => setStep(4)} />
        </section>
      );
    }

    if (step === 4) {
      const hasAllPokemon = POKEMON_FIELDS.every((field) => form[field].trim());
      const normalizedNames = POKEMON_FIELDS.map((field) => form[field].trim().toLowerCase()).filter(Boolean);
      const hasDuplicates = new Set(normalizedNames).size !== normalizedNames.length;
      const optionsByName = new Map(recommendedPokemonOptions.map((option) => [option.name.toLowerCase(), option]));

      return (
        <section className="wizard-card">
          <p className="step-count">Step 4 of 6</p>
          <h1>Choose Gym Leader Pokemon</h1>
          <p className="wizard-help">
            Recommended choices are based on {form.gym_leader_region} and {form.gym_leader_type}. You can still type any Pokemon manually.
          </p>
          {isLoadingOptions && <p className="copy-status">Loading recommended Pokemon...</p>}
          {optionsError && <p className="error-message">{optionsError}</p>}
          <div className="step-toolbar">
            <button className="copy-button" type="button" onClick={autofillRecommendedPokemon} disabled={recommendedPokemonOptions.length === 0}>
              Auto Fill Recommendations
            </button>
          </div>
          <div className="pokemon-slot-grid">
            {POKEMON_FIELDS.map((field, index) => (
              <PokemonComboCard
                key={field}
                field={field}
                index={index}
                value={form[field]}
                option={optionsByName.get(form[field].trim().toLowerCase()) || manualPokemonPreviews[field]}
                options={recommendedPokemonOptions}
                isOpen={openComboField === field}
                isResolving={Boolean(resolvingManualFields[field])}
                lookupError={manualLookupErrors[field]}
                onChange={updateField}
                onSelect={updateValue}
                onManualLookup={resolveManualPokemon}
                onOpen={setOpenComboField}
                onToggle={(targetField) => setOpenComboField((current) => current === targetField ? "" : targetField)}
              />
            ))}
          </div>
          {hasDuplicates && <p className="error-message">Duplicate Pokemon are not allowed in the Gym Leader team.</p>}
          <StepNavigation canContinue={hasAllPokemon && !hasDuplicates} onBack={() => setStep(3)} onNext={() => setStep(5)} />
        </section>
      );
    }

    if (step === 5) {
      return (
        <section className="wizard-card">
          <p className="step-count">Step 5 of 6</p>
          <h1>Select Challenger Region</h1>
          <div className="option-grid challenger-grid">
            {CHALLENGER_REGIONS.map((region) => (
              <OptionCard key={region} title={region} selected={form.challenger_region === region} onClick={() => updateValue("challenger_region", region)} />
            ))}
          </div>
          <StepNavigation canContinue={Boolean(form.challenger_region)} onBack={() => setStep(4)} onNext={() => setStep(6)} />
        </section>
      );
    }

    if (step === 6) {
      return (
        <section className="wizard-card">
          <p className="step-count">Step 6 of 6</p>
          <h1>Select Recommendation Method</h1>
          <div className="option-grid method-grid">
            {SELECTION_MODES.map((mode) => (
              <OptionCard key={mode.value} title={mode.label} description={mode.description} selected={form.selection_mode === mode.value} onClick={() => updateValue("selection_mode", mode.value)} />
            ))}
          </div>
          {error && <p className="error-message">{error}</p>}
          <StepNavigation canContinue={Boolean(form.selection_mode)} isLoading={isLoading} onBack={() => setStep(5)} onNext={() => requestLineup(form)} nextLabel="Generate Challenger Lineup" />
        </section>
      );
    }

    return null;
  }

  if (showLanding) {
    return (
      <main className="landing-page">
        <section className="landing-content">
          <p className="landing-kicker">Challenger Selection Engine</p>
          <h1>Welcome Trainer</h1>
          <p className="landing-copy">Are you ready to win your Gym battle?</p>
          {error && <p className="error-message">{error}</p>}
          <div className="landing-actions">
            <button type="button" onClick={createTeam}>Create Team</button>
            <button className="secondary-button" type="button" onClick={handleQuickGenerate} disabled={isLoading}>
              {isLoading ? "Generating..." : "Quick Generate"}
            </button>
          </div>
        </section>
      </main>
    );
  }

  if (step === 7) {
    return (
      <GachaponPull
        loading={isLoading}
        error={error}
        results={result}
        onViewResults={() => setStep(8)}
        onRetry={() => requestLineup(form)}
      />
    );
  }

  if (step !== 8) {
    return <main className="wizard-shell">{renderStep()}</main>;
  }

  return (
    <main className="app-shell results-shell">
      <section className="results-panel">
        <div className="output-heading">
          <div>
            <p className="step-count">Results</p>
            <h1>Recommended Challenger Team</h1>
          </div>
          <div className="result-actions">
            <button className="trainer-id-button" type="button" onClick={() => setIsTrainerIdOpen(true)} disabled={!result}>
              Generate Trainer ID
            </button>
            <button className="copy-button" type="button" onClick={copyShowdownTeam}>Copy Showdown Team</button>
            <button className="copy-button" type="button" onClick={() => setIsBattlePlanOpen(true)}>View Battle Plan</button>
            <button className="ghost-button" type="button" onClick={backToHome}>Back to Home</button>
            <button className="ghost-button" type="button" onClick={startOver}>Start Over</button>
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}
        {copyStatus && <p className="copy-status">{copyStatus}</p>}

        {result ? (
          <>
            <PreviousAnswers currentStep={8} form={form} onJump={setStep} />

            <section className="summary-grid">
              <div><span>Target Gym Leader</span><strong>{result.target_gym_leader}</strong></div>
              <div><span>Gym Leader Region</span><strong>{form.gym_leader_region}</strong></div>
              <div><span>Gym Leader Type</span><strong>{form.gym_leader_type}</strong></div>
              <div><span>Challenger Region</span><strong>{result.challenger_region}</strong></div>
              <div><span>Selection Method</span><strong>{result.model_used}</strong></div>
            </section>

            {result.backup_used && <p className="backup-notice">{result.backup_note}</p>}

            <section className="team-preview" aria-label="Enemy team">
              <h3>Enemy Team</h3>
              <div className="team-grid">
                {result.gym_leader_team.map((member, index) => (
                  <div className="team-card" key={`${member.pokemon}-${index}`}>
                    <PokemonImage src={member.sprite_url || member.image_url} name={member.pokemon} />
                    <span>{member.pokemon}</span>
                  </div>
                ))}
              </div>
            </section>

            <section className="team-preview" aria-label="Recommended challenger team">
              <h3>Recommended Challenger Team</h3>
              <div className="team-grid">
                {result.recommended_team.map((member) => (
                  <div className="team-card" key={member.pokemon}>
                    <PokemonImage src={member.sprite_url || member.image_url} name={member.pokemon} />
                    <span>{member.pokemon}</span>
                  </div>
                ))}
              </div>
            </section>

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Image</th>
                    <th>Pokemon</th>
                    <th>Native Region</th>
                    <th>Type 1</th>
                    <th>Type 2</th>
                    <th>HP</th>
                    <th>Attack</th>
                    <th>Defense</th>
                    <th>Special Attack</th>
                    <th>Special Defense</th>
                    <th>Speed</th>
                    <th>Counter Score</th>
                    <th>Reason Selected</th>
                  </tr>
                </thead>
                <tbody>
                  {result.recommended_team.map((member) => {
                    const { type1, type2 } = splitTypes(member.types);
                    return (
                      <tr key={member.pokemon}>
                        <td><PokemonImage src={member.sprite_url || member.image_url} name={member.pokemon} /></td>
                        <td>{member.pokemon}</td>
                        <td>{member.native_region}</td>
                        <td><TypeBadge type={type1} /></td>
                        <td><TypeBadge type={type2} /></td>
                        <td>{member.stats.hp}</td>
                        <td>{member.stats.attack}</td>
                        <td>{member.stats.defense}</td>
                        <td>{member.stats.special_attack}</td>
                        <td>{member.stats.special_defense}</td>
                        <td>{member.stats.speed}</td>
                        <td>{member.counter_score}</td>
                        <td>{member.reason_selected}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </>
        ) : (
          <p className="empty-state">No recommendation yet.</p>
        )}
      </section>
      <BattlePlanModal isOpen={isBattlePlanOpen} onClose={() => setIsBattlePlanOpen(false)} battlePlan={result?.battle_plan || []} />
      <TrainerIdModal isOpen={isTrainerIdOpen} onClose={() => setIsTrainerIdOpen(false)} results={result} formData={form} />
    </main>
  );
}
