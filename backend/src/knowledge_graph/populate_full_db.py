import json
import os

# --- VEDIC KEYWORDS ---
PLANET_NATURE = {
    "Sun": "authority, vitality, and the soul",
    "Moon": "emotions, mind, and comfort",
    "Mars": "energy, courage, and technical skill",
    "Mercury": "intellect, communication, and business",
    "Jupiter": "wisdom, expansion, and wealth",
    "Venus": "luxury, relationships, and art",
    "Saturn": "discipline, delay, and hard work",
    "Rahu": "desire, illusion, and foreign things",
    "Ketu": "detachment, spirituality, and liberation",
}

HOUSE_NATURE = {
    1: "the Self, appearance, and general vitality",
    2: "accumulated wealth, family, and speech",
    3: "siblings, courage, and self-effort",
    4: "mother, home, land, and happiness",
    5: "children, intelligence, and speculation",
    6: "enemies, debts, and diseases",
    7: "marriage, partnership, and legal bindings",
    8: "longevity, transformation, and occult knowledge",
    9: "dharma, father, guru, and fortune",
    10: "career, reputation, and social standing",
    11: "gains, older siblings, and networks",
    12: "losses, liberation, and foreign residence",
}

OUTPUT_FILE = "./data/processed_graph/synthetic_rules.json"


def generate_synthetic_rules():
    rules = []

    print("🔮 Synthesizing Vedic Rules...")

    for planet, p_desc in PLANET_NATURE.items():
        for house, h_desc in HOUSE_NATURE.items():
            # Construct a "Synthetic" Rule Text
            # Example: "The Sun in the 10th House illuminates career..."

            text = (
                f"When {planet} is placed in the {house} House, it brings the energy of {p_desc} "
                f"into the domain of {h_desc}. "
            )

            # Add specific flavor based on natural benefics/malefics
            if planet in ["Jupiter", "Venus", "Moon", "Mercury"]:
                text += f"This is generally a favorable placement that expands the native's {h_desc.split(',')[0]}."
            elif planet in ["Saturn", "Mars", "Rahu", "Ketu", "Sun"]:
                text += f"This placement may require discipline or intensity regarding {h_desc.split(',')[0]}."

            rule_entry = {
                "id": f"SYN_{planet}_{house}",
                "text": text,
                "source": "Synthesized Vedic Logic",
                "condition": {"planet": planet, "house": house},
            }
            rules.append(rule_entry)

    # Save to JSON
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(rules, f, indent=2)

    print(f"  Generated {len(rules)} rules covering all 108 planetary positions.")
    print(f"📂 Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_synthetic_rules()
