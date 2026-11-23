"""4 casos de prueba reales, basados en los mismos 2 papers ya usados.
`signals` simula lo que el paso de extracción (LLM) produciría; `content`
es el texto/datos ya redactados que los módulos necesitan para pintarse.
"""

import os

REFS = ["Feng et al. (2026). Graph Engineering in the Era of LLM Agents. arXiv:2608.21156",
        "Cao, Z. (2026). The End of Software Engineering. arXiv:2606.05608"]

_avatar_path = os.path.join(os.path.dirname(__file__), "avatar_b64.txt")
AVATAR_B64 = open(_avatar_path).read().strip() if os.path.exists(_avatar_path) else None

AUTHOR = dict(author="Christian Cobián", role="AI PRODUCT / SYSTEMS", refs=REFS,
              cta="Lee el análisis completo →", avatar_b64=AVATAR_B64)

CASES = {}

# ---- Caso 1: roadmap de 4 etapas (paper 2, Tabla 3) -> esperado: E ----
CASES["roadmap"] = {
    "signals": {
        "structure_type": "timeline", "n_items": 4, "has_before_after": False,
        "has_metrics": False, "has_roles_evolution": True, "has_dates": True,
        "has_hub_center": False, "n_satellite_categories": 0, "has_recap_chain": True,
        "has_named_alternatives": False,
    },
    "content": {
        "title": "El Roadmap Hacia<br>la Ingeniería Agéntica",
        "subtitle": "4 etapas, de autocompletado a ecosistemas que se auto-mejoran",
        "tagline": "Roadmap propuesto por el paper -- proyección de los autores, no un hecho consumado.",
        "stages": [
            dict(tag="I", period="2023-25", name="Tool-Augmented", desc="Autocompletado, fixes de un solo issue", color="#FF8A5B"),
            dict(tag="II", period="2025-27", name="Autonomía de tarea única", desc="Features y PRs de punta a punta", color="#2EE6F0"),
            dict(tag="III", period="2026-29", name="Equipos multiagente", desc="PM, arquitecto, dev y QA coordinando", color="#2EE6F0"),
            dict(tag="IV", period="2028+", name="Ecosistemas auto-evolutivos", desc="Mejora auto-dirigida, sub-agentes", color="#3EE08C"),
        ],
        "recap": ["Autor+revisor", "Arquitecto de intención", "PM+arquitecto+auditor", "Gobernanza ética"],
        **AUTHOR,
    },
}

# ---- Caso 2: jerarquía de capas (paper 1) -> esperado: B ----
CASES["jerarquia"] = {
    "signals": {
        "structure_type": "hierarchy", "n_items": 4, "has_before_after": False,
        "has_metrics": False, "has_roles_evolution": False, "has_dates": False,
        "has_hub_center": False, "n_satellite_categories": 3, "has_recap_chain": True,
        "has_named_alternatives": False,
    },
    "content": {
        "title": "De la Inteligencia Individual<br>a la Inteligencia de Sistema",
        "subtitle": "Por qué agregar más agentes no alcanza -- hay que organizar el sistema",
        "layers": [
            dict(tag="CAPA 1", name="Model Intelligence", desc="Pre/post-entrenamiento + Prompt &amp; Context Engineering", color="#FF8A5B"),
            dict(tag="CAPA 2", name="Individual Intelligence", desc="Harness + Loop Engineering -- Agent = Loop(LLM + Harness)", color="#2EE6F0"),
            dict(tag="CAPA 3", name="System Intelligence", desc="Graph Engineering organiza agentes y estado con grafos", color="#2EE6F0"),
            dict(tag="FUTURO", name="Ontology Engineering", desc="Semántica compartida, vocabulario de evaluación", color="#3EE08C", future=True),
        ],
        "recap": ["Model", "Individual", "System", "Ontology (futuro)"],
        **AUTHOR,
    },
}

# ---- Caso 3: hub/red (paper 1) -> esperado: H (ya "aprendido", 1 aprobación previa) ----
CASES["hub"] = {
    "signals": {
        "structure_type": "hub_network", "n_items": 5, "has_before_after": True,
        "has_metrics": True, "has_roles_evolution": True, "has_dates": False,
        "has_hub_center": True, "n_satellite_categories": 5, "has_recap_chain": False,
        "has_named_alternatives": False,
    },
    "content": {
        "title": "Graph Engineering<br>para Sistemas Agénticos",
        "subtitle": "Organiza, coordina y evoluciona agentes con arquitecturas basadas en grafos",
        "hub_center": "Grafo multiagente",
        "satellites": ["Organización de tareas", "Coordinación de agentes", "Recursos compartidos",
                       "Estado en runtime", "Evolución del sistema"],
        "roles": ["Arquitecto de intención", "Coordinador", "Auditor"],
        "roles_caption": "De programador a orquestador de sistemas inteligentes",
        "metrics": [
            dict(icon="⭐", text="<b>-93%</b> en tiempo de diagnóstico de causa raíz (piloto multiagente, +200h ahorradas/mes)"),
            dict(icon="⚠️", text="En evolución continua el éxito cae de <b>&gt;80% a ≤38%</b> (benchmark EvoClaw)"),
        ],
        **AUTHOR,
    },
}

# ---- Caso 4: topologías de equipos de agentes (paper 1) -> esperado: NINGÚN match, composer ----
CASES["topologias"] = {
    "signals": {
        "structure_type": "comparison", "n_items": 3, "has_before_after": False,
        "has_metrics": False, "has_roles_evolution": False, "has_dates": False,
        "has_hub_center": False, "n_satellite_categories": 0, "has_recap_chain": False,
        "has_named_alternatives": True,
    },
    "content": {
        "title": "3 Formas de Organizar<br>un Equipo de Agentes",
        "subtitle": "No hay un ganador único -- cada topología resuelve un problema distinto de coordinación",
        "alternatives": [
            dict(name="Cadena (MetaGPT, ChatDev)", items=[
                "Roles fijos en secuencia (ej. PM -> Dev -> QA)",
                "Simple y predecible",
                "No se adapta si una subtarea cambia a mitad de camino"]),
            dict(name="Routing / Supervisor (Magentic-One)", items=[
                "Un supervisor asigna cada subtarea al agente adecuado",
                "Buen control central",
                "El supervisor es un cuello de botella y un punto único de falla"]),
            dict(name="Fan-out / Fan-in (Mixture-of-Agents, MacNet)", items=[
                "Varios agentes trabajan la misma subtarea en paralelo y se combinan resultados",
                "Mejor calidad vía diversidad de enfoques",
                "Más caro en cómputo por el paralelismo"]),
        ],
        **AUTHOR,
    },
}

# ---- Caso 5: ciclo agéntico + grilla de fases (inspirado en la FORMA del post
# real "From SDLC to ADLC", +4200 likes -- contenido propio de Cris sobre los
# 2 papers de prueba, no una reproducción) ----
# Con has_metrics ya opcional en A, este caso anota ~65 (recomendado con
# advertencia) -- pero un antes/después de 2 paneles no alcanza a cubrir el
# ciclo ni la grilla de fases, así que el humano rechaza y se compone con
# compare2 + cycle_flow + cards_grid juntos por primera vez.
CASES["ciclo_agentico"] = {
    "signals": {
        "structure_type": "sequence", "n_items": 2, "has_before_after": True,
        "has_metrics": False, "has_roles_evolution": False, "has_dates": False,
        "has_hub_center": False, "n_satellite_categories": 0, "has_recap_chain": False,
        "has_named_alternatives": False, "has_cycle": True, "n_cards": 6,
    },
    "content": {
        "kicker": "INGENIERÍA AGÉNTICA",
        "title": "Del SDLC al Ciclo Agéntico",
        "subtitle": "Por qué el desarrollo de software deja de ser lineal",
        "tagline": "La cadena de artefactos reemplaza a los handoffs: cada commit "
                   "deja el rastro de auditoría que antes vivía en reuniones.",
        "titles": {
            "compare2": "El contraste: lineal vs. continuo",
            "cycle_flow": "La cadena de artefactos (el rastro de auditoría)",
            "cards_grid": "Qué cambia en cada fase",
            "metrics_row": "La evidencia",
        },
        "left": dict(title="SDLC tradicional", icon="📐", formula="LINEAL · HANDOFFS HUMANOS", items=[
            "Requisitos → diseño → build → QA → release, en ese orden",
            "Cada etapa espera a que termine la anterior",
            "El humano mueve el trabajo entre etapas"]),
        "right": dict(title="Ciclo agéntico", icon="🔄", formula="CONTINUO · DIRIGIDO POR ARTEFACTOS", items=[
            "Intent → spec → plan → build → review → producción, sin handoffs",
            "La señal de producción genera el siguiente intent automáticamente",
            "El agente ejecuta; el humano audita los puntos críticos"]),
        "annotation": "El ciclo no termina en el deploy: la señal de producción es el "
                      "input del siguiente intent, y ahí es donde deja de ser una línea.",
        "cycle_nodes": [
            dict(icon="🎯", name="intent.md", desc="qué construir"),
            dict(icon="📄", name="spec.md", desc="diseño y enfoque"),
            dict(icon="🗺️", name="plan.md", desc="plan de implementación"),
            dict(icon="💻", name="código + tests", desc="el diff"),
            dict(icon="🔍", name="review", desc="aprobación y deploy"),
            dict(icon="📡", name="señal de producción", desc="incidente / métrica"),
        ],
        "cards": [
            dict(icon="📋", title="Plan", color="#D9661E", desc="El agente redacta el intent en lenguaje humano-legible"),
            dict(icon="✏️", title="Diseño", color="#D9661E", desc="Requisitos y diseño convergen en una sola sesión"),
            dict(icon="🔨", title="Build", color="#2EE6F0", desc="El conocimiento institucional vive en archivos de contexto"),
            dict(icon="✅", title="Test", color="#2EE6F0", desc="Evals continuas reemplazan el QA por etapas"),
            dict(icon="🚀", title="Deploy", color="#3EE08C", desc="Revisión agéntica con gobernanza ejecutable"),
            dict(icon="🔁", title="Maintain", color="#3EE08C", desc="Una alerta de producción escribe el siguiente intent"),
        ],
        "metrics_row": [
            dict(value="-93%", label="tiempo de diagnóstico de causa raíz (piloto multiagente)", color="#3EE08C"),
            dict(value="+200h", label="ahorradas por mes en el mismo piloto", color="#2EE6F0"),
            dict(value="≤38%", label="éxito en evolución continua: cae desde >80% (EvoClaw)", color="#D9661E"),
        ],
        **AUTHOR,
    },
}
