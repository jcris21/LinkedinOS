"""
Matcher determinístico y auditable: copy/fuente -> señales -> score por
arquetipo + justificación explícita (qué cubre, qué le falta, qué se forzaría).

El LLM solo produce `signals` (extracción); el score y la justificación
los calcula este módulo con reglas fijas -- por eso es auditable y repetible.
"""
from archetypes import ARCHETYPES, REQUIRED_CAP


def _check(signals, sig_name, expected):
    val = signals.get(sig_name)
    if isinstance(expected, tuple) and len(expected) == 2 and isinstance(expected[0], int):
        lo, hi = expected
        return isinstance(val, int) and lo <= val <= hi
    return val == expected


def score_archetype(signals, arche_key):
    arche = ARCHETYPES[arche_key]
    total_possible = sum(c[2] for c in arche["criteria"])
    earned = 0
    satisfied, missing_required, missing_optional = [], [], []

    for sig_name, expected, points, required in arche["criteria"]:
        ok = _check(signals, sig_name, expected)
        label = f"{sig_name}={expected}"
        if ok:
            earned += points
            satisfied.append(label)
        elif required:
            missing_required.append(label)
        else:
            missing_optional.append(label)

    raw_score = round(100 * earned / total_possible) if total_possible else 0
    capped = bool(missing_required)
    final_score = min(raw_score, REQUIRED_CAP) if capped else raw_score

    return {
        "archetype": arche_key,
        "label": arche["label"],
        "score": final_score,
        "capped_by_missing_required": capped,
        "satisfied": satisfied,
        "missing_required": missing_required,
        "missing_optional": missing_optional,
        "learned": arche.get("learned", False),
        "promoted": arche.get("promoted", False),
        "approvals": arche.get("approvals", 0),
    }


def propose(signals):
    """Rankea todos los arquetipos y arma la justificación legible."""
    ranked = sorted(
        (score_archetype(signals, k) for k in ARCHETYPES),
        key=lambda r: r["score"],
        reverse=True,
    )
    best = ranked[0]
    return {
        "ranked": ranked,
        "best": best,
        "recommend": best["score"] >= 75,
        "recommend_with_warning": 55 <= best["score"] < 75,
        "needs_composition": best["score"] < 55,
    }


def explain(result):
    lines = []
    for r in result["ranked"]:
        tag = " [aprendido]" if r["learned"] else ""
        tag += " [confiable]" if r["promoted"] else ""
        lines.append(f"\n▸ {r['label']}{tag} — score {r['score']}/100")
        if r["satisfied"]:
            lines.append(f"    cubre: {', '.join(r['satisfied'])}")
        if r["missing_required"]:
            lines.append(f"    ❌ le falta (obligatorio): {', '.join(r['missing_required'])}")
        if r["missing_optional"]:
            lines.append(f"    (no tiene, opcional): {', '.join(r['missing_optional'])}")
    best = result["best"]
    if result["recommend"]:
        verdict = f"✅ Recomendado: {best['label']} (score {best['score']})"
    elif result["recommend_with_warning"]:
        verdict = f"⚠️  Match parcial: {best['label']} (score {best['score']}) — revisar qué se pierde"
    else:
        verdict = f"🧩 Ningún arquetipo califica (mejor score {best['score']}) — componer layout propio"
    return "\n".join(lines) + "\n\n" + verdict
