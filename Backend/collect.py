import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cdi_engine import calculate_cdi

# Paths
PROMPTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_prompts.json")
RESPONSES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/responses")

def load_prompts():
    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_prompts(data):
    with open(PROMPTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_response_file(prompt_id, model, condition):
    """
    Reads a plain text file from data/responses/
    File naming: RF-0-01_chatgpt_anonymous.txt
    """
    filename = f"{prompt_id}_{model}_{condition}.txt"
    filepath = os.path.join(RESPONSES_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()

def score_all():
    """
    Reads all response text files, scores them with CDI engine,
    and updates test_prompts.json automatically.
    """
    data = load_prompts()
    models = ["chatgpt", "gemini", "claude"]
    conditions = ["anonymous", "identified"]
    updated = 0
    skipped = 0

    for prompt in data["prompts"]:
        pid = prompt["id"]
        
        for model in models:
            for condition in conditions:
                # Skip if already scored
                existing = prompt["responses"][model][condition]
                if existing.get("cdi") is not None:
                    skipped += 1
                    continue
                
                # Try to read response file
                text = read_response_file(pid, model, condition)
                if not text:
                    continue
                
                # Score it
                scores = calculate_cdi(text, model)
                
                # Update the prompt data
                prompt["responses"][model][condition]["text"] = text
                prompt["responses"][model][condition]["cdi"] = scores["cdi"]
                prompt["responses"][model][condition]["ras"] = scores["ras"]
                prompt["responses"][model][condition]["atd"] = scores["atd"]
                prompt["responses"][model][condition]["lls"] = scores["lls"]
                prompt["responses"][model][condition]["flagged_terms"] = scores["flagged_terms"]
                
                updated += 1
                print(f"✅ Scored {pid} | {model} | {condition} → CDI: {scores['cdi']}")

        # Score control responses too
        if "control_responses" in prompt:
            for model in models:
                ctrl = prompt["control_responses"][model]
                if ctrl.get("cdi") is not None:
                    continue
                text = read_response_file(pid, model, "control")
                if not text:
                    continue
                scores = calculate_cdi(text, model)
                ctrl["text"] = text
                ctrl["cdi"] = scores["cdi"]
                ctrl["ras"] = scores["ras"]
                ctrl["atd"] = scores["atd"]
                ctrl["lls"] = scores["lls"]
                updated += 1
                print(f"✅ Scored {pid} | {model} | control → CDI: {scores['cdi']}")

    save_prompts(data)
    print(f"\nDone. {updated} responses scored, {skipped} already had scores.")

def show_missing():
    """Shows which response files are still missing."""
    data = load_prompts()
    models = ["chatgpt", "gemini", "claude"]
    conditions = ["anonymous", "identified"]
    missing = []

    for prompt in data["prompts"]:
        pid = prompt["id"]
        for model in models:
            for condition in conditions:
                filename = f"{pid}_{model}_{condition}.txt"
                filepath = os.path.join(RESPONSES_DIR, filename)
                if not os.path.exists(filepath):
                    missing.append(filename)
            if "control_responses" in prompt:
                filename = f"{pid}_{model}_control.txt"
                filepath = os.path.join(RESPONSES_DIR, filename)
                if not os.path.exists(filepath):
                    missing.append(filename)

    print(f"\n{len(missing)} response files missing:\n")
    for f in missing[:20]:
        print(f"  ❌ {f}")
    if len(missing) > 20:
        print(f"  ... and {len(missing) - 20} more")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "missing":
        show_missing()
    else:
        score_all()