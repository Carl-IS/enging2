export default function BattlePlanModal({ isOpen, onClose, battlePlan }) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="battle-plan-title">
      <section className="battle-plan-modal">
        <div className="modal-heading">
          <div>
            <p className="step-count">Strategy</p>
            <h1 id="battle-plan-title">Recommended Battle Plan</h1>
          </div>
          <button className="modal-close-button" type="button" onClick={onClose} aria-label="Close battle plan">
            Close
          </button>
        </div>

        <div className="battle-plan-grid">
          {(battlePlan || []).map((plan) => (
            <article className="battle-plan-card" key={`${plan.challenger_pokemon}-${plan.best_match_against}`}>
              <div className="battle-matchup-row">
                <div className="battle-side challenger-side">
                  {plan.challenger_image_url ? (
                    <img src={plan.challenger_image_url} alt={plan.challenger_pokemon} />
                  ) : (
                    <div className="battle-plan-placeholder">{plan.challenger_pokemon.charAt(0)}</div>
                  )}
                  <strong>{plan.challenger_pokemon}</strong>
                </div>

                <div className="battle-vs">
                  <span>VS</span>
                  <strong>{plan.matchup_score}</strong>
                </div>

                <div className="battle-side target-side">
                  {plan.best_match_image_url ? (
                    <img src={plan.best_match_image_url} alt={plan.best_match_against} />
                  ) : (
                    <div className="battle-plan-placeholder">{plan.best_match_against.charAt(0)}</div>
                  )}
                  <span>Gym Matchup</span>
                  <strong>{plan.best_match_against}</strong>
                </div>
              </div>

              <span className="matchup-score-badge">Matchup Score: {plan.matchup_score}</span>
              <div className="recommended-move-box">
                <span>Recommended Move</span>
                <strong>{plan.recommended_move}</strong>
                {plan.recommended_move_type && <small>{plan.recommended_move_type}-type</small>}
              </div>
              <p className="battle-plan-reason">{plan.reason}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
