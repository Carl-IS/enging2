import { useRef, useState } from "react";
import normalIcon from "../assets/type-icons/normal.png";
import fireIcon from "../assets/type-icons/fire.png";
import waterIcon from "../assets/type-icons/water.png";
import electricIcon from "../assets/type-icons/electric.png";
import grassIcon from "../assets/type-icons/grass.png";
import iceIcon from "../assets/type-icons/ice.png";
import fightingIcon from "../assets/type-icons/fighting.png";
import poisonIcon from "../assets/type-icons/poison.png";
import groundIcon from "../assets/type-icons/ground.png";
import flyingIcon from "../assets/type-icons/flying.png";
import psychicIcon from "../assets/type-icons/psychic.png";
import bugIcon from "../assets/type-icons/bug.png";
import rockIcon from "../assets/type-icons/rock.png";
import ghostIcon from "../assets/type-icons/ghost.png";
import dragonIcon from "../assets/type-icons/dragon.png";
import darkIcon from "../assets/type-icons/dark.png";
import steelIcon from "../assets/type-icons/steel.png";
import fairyIcon from "../assets/type-icons/fairy.png";

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

function getMemberImage(member) {
  return member?.sprite_url || member?.image_url || "";
}

function getTypes(member) {
  if (Array.isArray(member?.types)) {
    return {
      type1: member.types[0] || "-",
      type2: member.types[1] || "-"
    };
  }

  return {
    type1: member?.type_1 || "-",
    type2: member?.type_2 || "-"
  };
}

function TypePill({ type }) {
  if (!type || type === "-") {
    return null;
  }

  return (
    <span className="trainer-type-pill" style={{ "--type-color": TYPE_COLORS[type] || "#687586" }} title={type}>
      <img src={TYPE_ICONS[type]} alt={`${type} type`} />
    </span>
  );
}

export default function TrainerIdModal({ isOpen, onClose, results, formData }) {
  const [trainerName, setTrainerName] = useState("");
  const [trainerSection, setTrainerSection] = useState("");
  const [trainerPhotoPreview, setTrainerPhotoPreview] = useState("");
  const [hasGenerated, setHasGenerated] = useState(false);
  const [formError, setFormError] = useState("");
  const [isDownloading, setIsDownloading] = useState(false);
  const [hideExternalImages, setHideExternalImages] = useState(false);
  const trainerIdRef = useRef(null);

  if (!isOpen) {
    return null;
  }

  const team = results?.recommended_team || [];
  const challengerRegion = results?.challenger_region || formData?.challenger_region || "-";
  const targetGymLeader = results?.target_gym_leader || formData?.gym_leader_name || "-";
  const gymRegion = formData?.gym_leader_region || "-";
  const gymType = formData?.gym_leader_type || "-";

  function handlePhotoUpload(event) {
    const file = event.target.files[0];
    if (!file) {
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => {
      setTrainerPhotoPreview(reader.result);
    };
    reader.readAsDataURL(file);
  }

  function handleGenerateId() {
    if (!trainerName.trim()) {
      setFormError("Trainer name is required.");
      return;
    }

    setFormError("");
    setHasGenerated(true);
  }

  async function createCanvas(html2canvas, shouldHideImages = false) {
    setHideExternalImages(shouldHideImages);
    await new Promise((resolve) => window.requestAnimationFrame(resolve));
    return html2canvas(trainerIdRef.current, {
      scale: 2,
      useCORS: true,
      backgroundColor: "#ffffff"
    });
  }

  async function downloadTrainerIdPdf() {
    if (!trainerIdRef.current || !trainerName.trim()) {
      return;
    }

    setIsDownloading(true);

    try {
      const [{ default: html2canvas }, { default: jsPDF }] = await Promise.all([
        import("html2canvas"),
        import("jspdf")
      ]);
      let canvas;
      try {
        canvas = await createCanvas(html2canvas, false);
      } catch {
        canvas = await createCanvas(html2canvas, true);
      }

      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("landscape", "mm", "a4");
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = pageWidth - 20;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      const x = 10;
      const y = Math.max(10, (pageHeight - imgHeight) / 2);

      pdf.addImage(imgData, "PNG", x, y, imgWidth, imgHeight);
      pdf.save(`${trainerName.trim() || "trainer"}-challenger-id.pdf`);
    } finally {
      setHideExternalImages(false);
      setIsDownloading(false);
    }
  }

  return (
    <div className="trainer-modal-overlay" role="dialog" aria-modal="true" aria-labelledby="trainer-id-title">
      <section className="trainer-modal">
        <div className="modal-heading">
          <div>
            <p className="step-count">Trainer Card</p>
            <h1 id="trainer-id-title">Generate Trainer ID</h1>
          </div>
          <button className="modal-close-button" type="button" onClick={onClose}>
            Close
          </button>
        </div>

        <div className="trainer-modal-content">
          <form className="trainer-form">
            <label>
              Trainer Name
              <input
                value={trainerName}
                onChange={(event) => {
                  setTrainerName(event.target.value);
                  setFormError("");
                }}
                placeholder="Enter your trainer name"
              />
            </label>

            <label>
              Section
              <input
                value={trainerSection}
                onChange={(event) => setTrainerSection(event.target.value)}
                placeholder="Example: 3ISA"
              />
            </label>

            <label>
              1x1 Photo
              <input accept="image/*" type="file" onChange={handlePhotoUpload} />
            </label>

            <div className="trainer-photo-preview">
              {trainerPhotoPreview ? <img src={trainerPhotoPreview} alt="Trainer preview" /> : <span>No Photo</span>}
            </div>

            {formError && <p className="error-message">{formError}</p>}

            <button className="trainer-id-button" type="button" onClick={handleGenerateId}>
              Generate ID
            </button>
          </form>

          {hasGenerated && (
            <section className="trainer-preview-panel">
              <div className="trainer-id-card" ref={trainerIdRef}>
                <header className="trainer-id-header">
                  <div>
                    <span>Pokemon Day II</span>
                    <h2>Challenger ID</h2>
                  </div>
                  <strong>{challengerRegion}</strong>
                </header>

                <div className="trainer-id-body">
                  <section className="trainer-profile-section">
                    <div className="trainer-card-photo">
                      {trainerPhotoPreview ? <img src={trainerPhotoPreview} alt={trainerName} /> : <span>No Photo</span>}
                    </div>
                    <div className="trainer-card-details">
                      <span>Trainer</span>
                      <strong>{trainerName.trim()}</strong>
                      <small>Region: {challengerRegion}</small>
                      <small>Section: {trainerSection.trim() || "-"}</small>
                    </div>
                  </section>

                  <section className="trainer-match-section">
                    <div>
                      <span>Target Gym Leader</span>
                      <strong>{targetGymLeader}</strong>
                    </div>
                    <div>
                      <span>Gym Region</span>
                      <strong>{gymRegion}</strong>
                    </div>
                    <div>
                      <span>Gym Type</span>
                      <strong>{gymType}</strong>
                    </div>
                  </section>

                  <section className="trainer-team-section">
                    <h3>Generated Challenger Team</h3>
                    <div className="trainer-team-grid">
                      {team.map((member) => {
                        const { type1, type2 } = getTypes(member);
                        const image = getMemberImage(member);
                        return (
                          <article className="trainer-pokemon-card" key={member.pokemon}>
                            {!hideExternalImages && image ? (
                              <img crossOrigin="anonymous" src={image} alt={member.pokemon} />
                            ) : (
                              <div className="trainer-pokemon-placeholder">?</div>
                            )}
                            <div>
                              <strong>{member.pokemon}</strong>
                              <div className="trainer-type-row">
                                <TypePill type={type1} />
                                <TypePill type={type2} />
                              </div>
                            </div>
                          </article>
                        );
                      })}
                    </div>
                  </section>
                </div>
              </div>

              <button className="download-pdf-button" type="button" onClick={downloadTrainerIdPdf} disabled={isDownloading}>
                {isDownloading ? "Preparing PDF..." : "Download PDF"}
              </button>
            </section>
          )}
        </div>
      </section>
    </div>
  );
}
