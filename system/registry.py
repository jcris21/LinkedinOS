"""
Memoria persistente de decisiones: qué se propuso, qué confirmó o rechazó
el humano, y qué señales quedaron sin cubrir (gaps). Sirve para:
  1) auditar por qué se eligió cada arquetipo
  2) detectar gaps recurrentes y priorizarlos al componer un layout propio
  3) promover una composición repetida a arquetipo "confiable"
"""
import json, os, datetime

PATH = os.path.join(os.path.dirname(__file__), "registry.json")
from archetypes import PROMOTION_THRESHOLD


def _default():
    return {
        "decisions": [],
        "gap_counts": {},
        # se siembra con el estado real: H_hub_red ya se usó y se aprobó una vez
        # en la sesión anterior (el post "El Software Cambia de Paradigma").
        "learned_archetypes": {"H_hub_red": {"approvals": 1, "promoted": False}},
    }


def load():
    if not os.path.exists(PATH):
        data = _default()
        save(data)
        return data
    with open(PATH) as f:
        return json.load(f)


def save(data):
    with open(PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def log_decision(case_id, propose_result, chosen_key, human_confirmed, gaps=None):
    data = load()
    entry = {
        "case_id": case_id,
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "best_proposed": propose_result["best"]["archetype"],
        "best_score": propose_result["best"]["score"],
        "chosen": chosen_key,
        "human_confirmed": human_confirmed,
        "composed_custom": chosen_key is None,
        "gaps": gaps or [],
    }
    data["decisions"].append(entry)
    for g in (gaps or []):
        data["gap_counts"][g] = data["gap_counts"].get(g, 0) + 1
    save(data)
    return entry


def recurring_gaps(min_count=2):
    data = load()
    items = [(g, c) for g, c in data["gap_counts"].items() if c >= min_count]
    return sorted(items, key=lambda x: -x[1])


def bump_approval(arche_key):
    data = load()
    rec = data["learned_archetypes"].setdefault(arche_key, {"approvals": 0, "promoted": False})
    rec["approvals"] += 1
    promoted_now = False
    if rec["approvals"] >= PROMOTION_THRESHOLD and not rec["promoted"]:
        rec["promoted"] = True
        promoted_now = True
    save(data)
    return rec, promoted_now


def get_learned_state(arche_key):
    data = load()
    return data["learned_archetypes"].get(arche_key, {"approvals": 0, "promoted": False})
