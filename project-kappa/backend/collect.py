import json
import os
import sys

sys.path.append(r"C:\Users\FELIX TECNIX\Desktop\kappa-brain")
from engine.smart_cdi import calculate_smart_cdi

PROMPTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_prompts.json")
RESPONSES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/responses")

def load_prompts():
    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_prompts(data):
    with open(PROMPTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_response_file(prompt_id, model, condition):
    filename = f"{prompt_id}_{model}_{condition}.txt"
    filepath = os.path.join(RESPONSES_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return content if content else None

def score_all():
    data = load_prompts()
    models = ["chatgpt", "gemini", "claude"]
    conditions = ["anonymous", "identified"]
    updated = 0
    skipped = 0

    for prompt in data["prompts"]:
        pid = prompt["id"]
        prompt_text = prompt.get("prompt", "")

        for model in models:
            for condition in conditions:
                existing = prompt["responses"][model][condition]
                if existing.get("cdi") is not None:
                    skipped += 1
                    continue

                text = read_response_file(pid, model, condition)
                if not text:
                    continue

                scores = calculate_smart_cdi(
                    response=text,
                    prompt=prompt_text,
                    model_name=model
                )

                prompt["responses"][model][condition]["text"] = text[:500]
                prompt["responses"][model][condition]["cdi"] = scores["cdi"]
                prompt["responses"][model][condition]["ras"] = scores["ras"]
                prompt["responses"][model][condition]["atd"] = scores["atd"]
                prompt["responses"][model][condition]["lls"] = scores["lls"]
                prompt["responses"][model][condition]["flagged_terms"] = scores["western_flagged"]

                updated += 1
                print(f"✅ {pid} | {model} | {condition} → CDI: {scores['cdi']} | PROD: {scores['prod']} | {scores['lls_interpretation']}")

        if "control_responses" in prompt:
            for model in models:
                ctrl = prompt["control_responses"][model]
                if ctrl.get("cdi") is not None:
                    continue
                text = read_response_file(pid, model, "control")
                if not text:
                    continue
                scores = calculate_smart_cdi(
                    response=text,
                    prompt=prompt_text,
                    model_name=model
                )
                ctrl["text"] = text[:500]
                ctrl["cdi"] = scores["cdi"]
                ctrl["ras"] = scores["ras"]
                ctrl["atd"] = scores["atd"]
                ctrl["lls"] = scores["lls"]
                updated += 1
                print(f"✅ {pid} | {model} | control → CDI: {scores['cdi']} | PROD: {scores['prod']}")

    save_prompts(data)
    print(f"\nDone. {updated} responses scored, {skipped} already had scores.")

def show_missing():
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

    print(f"\n{len(missing)} response files missing:\n")
    for f in missing[:30]:
        print(f"  ❌ {f}")
    if len(missing) > 30:
        print(f"  ... and {len(missing) - 30} more")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "missing":
        show_missing()
    else:
        score_all()