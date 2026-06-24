import json
import os

# Load model profiles from GitHub-synced data file
PROFILES_PATH = os.path.join(os.path.dirname(__file__), "../data/model_profiles.json")

def load_model_profiles():
    try:
        with open(PROFILES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_model_profile(model_name: str) -> dict:
    """
    Returns the bias fingerprint for a given AI model.
    This is built from our 50 stress-test prompts (Phase 4).
    """
    profiles = load_model_profiles()
    model_key = model_name.lower().strip()
    
    # Return profile if exists, otherwise return neutral default
    return profiles.get(model_key, {
        "name": model_name,
        "avg_cdi": 0.5,
        "avg_ras": 0.5,
        "avg_atd": 0.5,
        "avg_lls": 0.5,
        "known_bias_patterns": [],
        "notes": "No profile yet — will be updated after stress testing."
    })

def get_bias_context(model_name: str, current_scores: dict) -> dict:
    """
    Compares current response scores against the model's known average.
    Tells us if this response is worse than usual for this model.
    """
    profile = get_model_profile(model_name)
    
    cdi_delta = current_scores.get("cdi", 0.5) - profile["avg_cdi"]
    
    if cdi_delta < -0.2:
        severity = "worse than usual for this model"
    elif cdi_delta > 0.2:
        severity = "better than usual for this model"
    else:
        severity = "typical for this model"
    
    return {
        "model_avg_cdi": profile["avg_cdi"],
        "current_cdi": current_scores.get("cdi", 0.5),
        "delta": round(cdi_delta, 3),
        "severity": severity,
        "known_patterns": profile.get("known_bias_patterns", [])
    }