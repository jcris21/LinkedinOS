# LinkedIn Thought-Leader Content OS — Blueprint de Skills
**v0.1 — documento vivo para iterar antes de testear y replicar en `/mnt/skills`**

Objetivo: posicionar a Cris como experto en IA para Mid/Enterprise leaders mediante un sistema de contenido automatizado (branding + calendario + publicación) que produce posts de LinkedIn de alto engagement con animación (GIF/clip en loop corto).

---

## 1. 🧩 AI AGENT BLUEPRINT™ (aplicado con `/ai-agent-blueprint`)

```
Tarea: Pipeline de generación + publicación automatizada de posts LinkedIn
       con animación, para posicionamiento de thought-leadership en IA.

¿Necesita agente?: Parcial — NO como agente autónomo único end-to-end.
  La mayoría de pasos tiene secuencia conocida de antemano (Workflow) o
  requiere criterio puntual y acotado (Skill). Solo el escaneo semanal de
  tendencias/competencia justifica un patrón de agente (no se puede fijar
  de antemano qué fuentes consultar ni cuántas vueltas dar). Además, dado
  el riesgo reputacional de publicar en tu nombre, el pipeline NO debe ser
  autónomo de punta a punta: necesita un gate humano antes de publicar
  (consistente con tu arquitectura actual: n8n determinístico + Claude
  razonando + aprobación humana).

Tipo de agente: Orquestador + subagentes (research) con un tramo de
  Agente supervisado (human-in-the-loop) en el gate de publicación.

Patrón(es): Routing (idea → pilar de contenido) · Tool Use (Canva vs
  RunComfy según el brief) · Reflection (QA de marca antes de aprobar) ·
  Planning (calendario editorial).

Modalidad de implementación recomendada:
  - Skills de Claude (paquete reutilizable, formato Anthropic) para cada
    paso con criterio editorial/creativo.
  - Subagente (Agent tool) solo para el research semanal de tendencias.
  - n8n para lo determinístico: calendario, triggers, publicación vía
    Unipile, logging a Airtable/Attio.
  - MCP conectores: Canva / RunComfy (generación de animación), Unipile
    (publicación LinkedIn), Airtable (calendario/tracking).

Siguiente paso concreto: construir y testear la Fase B (ciclo semanal)
  con UN post real de punta a punta antes de automatizar el trigger n8n.
```

---

## 2. Arquitectura general

```mermaid
flowchart TD
    subgraph FASE_A["FASE A — Fundamentos (setup, 1 vez / trimestral)"]
        A1[A1 · ai-positioning-foundation]
        A2[A2 · linkedin-brand-kit]
        A1 --> A2
    end

    subgraph FASE_B["FASE B — Ciclo semanal (recurrente)"]
        B1[B1 · linkedin-trend-scout\n(subagente research)]
        B2[B2 · linkedin-hook-copywriter]
        B3[B3 · linkedin-animated-post-builder\n(Canva / RunComfy)]
        B4[B4 · linkedin-post-qa-brand-check\n(Reflection)]
        B5[B5 · linkedin-calendar-scheduler\n(n8n + Airtable)]
        B6{{B6 · linkedin-publish-gate\n✋ aprobación humana}}
        B7[B7 · linkedin-engagement-learner\n(+48h)]

        B1 --> B2 --> B3 --> B4
        B4 -- rechazado --> B2
        B4 -- aprobado --> B5 --> B6
        B6 -- publica --> B7
        B7 -. feedback .-> B1
    end

    A2 ==> B1
```

**Orquestador:** `linkedin-thought-leader-os` — meta-skill que encadena B1→B7 con checkpoints, siguiendo el mismo patrón que ya usas en los skills `*-flow` de ai-native-os.

---

## 3. Secuencia de skills — tabla maestra

| # | Skill | Modalidad | Patrón | Input | Output | Herramienta/MCP |
|---|-------|-----------|--------|-------|--------|------------------|
| A1 | `ai-positioning-foundation` *(reutiliza `positioning-content-engine-builder`)* | Skill | Planning | Perfil de Cris, ICP (Mid/Ent leaders) | Statement de posicionamiento + pilares + roadmap de piezas | — |
| A2 | `linkedin-brand-kit` *(nueva; apoya en `design:design-system` + `brand-voice:generate-guidelines`)* | Skill | — | Pilares de A1, assets existentes | Paleta, tipografía, plantilla de animación, tono de voz LinkedIn | Figma/Canva (opcional) |
| B1 | `linkedin-trend-scout` **(nueva)** | Subagente | Tool Use + Research | Pilares, fecha | 3–5 ideas priorizadas con ángulo | WebSearch, share-of-model (opcional) |
| B2 | `linkedin-hook-copywriter` **(nueva)** | Skill | — | Idea priorizada | 3 variantes de copy/hook on-brand | `brand-voice-enforcement` |
| B3 | `linkedin-animated-post-builder` **(construida — motor propio, no Canva/RunComfy)** | Skill | Tool Use + Reflection | Copy ganador | Par ES+EN: póster diagrama (HTML→PNG) + MP4 en loop con Ken Burns + pulsos animados, por idioma | HTML/CSS/SVG + Playwright + ffmpeg (ver `system/`) |
| B4 | `linkedin-post-qa-brand-check` **(nueva)** | Skill | Reflection | Copy + visual | Aprobado / devuelto con feedback | Brand kit (A2) |
| B5 | `linkedin-calendar-scheduler` | Workflow (n8n) + Skill ligera | Planning | Post aprobado | Slot en calendario editorial | Airtable, n8n |
| B6 | `linkedin-publish-gate` | Human-in-the-loop + Workflow | — | Post + slot | Post publicado | Unipile (LinkedIn API), n8n |
| B7 | `linkedin-engagement-learner` **(nueva)** | Skill | — | Métricas 48h | Aprendizaje anotado, ajuste de hipótesis | Unipile/LinkedIn analytics |

---

## 4. Specs cortas de las skills nuevas (formato Anthropic — para construir en `/mnt/skills`)

### `linkedin-trend-scout`
- **description:** "Escanea señales de la semana (noticias de IA aplicada a negocio, movimientos de competidores/voces del sector, preguntas recurrentes de la audiencia Mid/Enterprise) y devuelve 3–5 ideas de post priorizadas, cada una mapeada a un pilar de contenido."
- **Guardrails:** nunca inventa datos/cifras; cada idea cita su fuente; se detiene a pedir aprobación del pilar si ninguna idea calza con los pilares vigentes.
- **Condición de parada:** entrega las ideas y termina — no decide el copy final.

### `linkedin-hook-copywriter`
- **description:** "Convierte una idea priorizada en 3 variantes de hook/copy para thought-leadership B2B (ej. contraintuitivo, dato + insight, historia corta), aplicando brand-voice-enforcement."
- **Formato de salida:** 3 variantes numeradas + recomendación de cuál testear primero y por qué.

### `linkedin-animated-post-builder` — ✅ construida, ver spec completa en `linkedin-animated-post-builder-SKILL.md`
- **Qué es en producción:** no usa Canva ni RunComfy — es un motor propio (HTML/CSS/SVG → Playwright → ffmpeg) con matching determinístico copy↔arquetipo, composición de módulos reusables, y animación real (pulsos viajando por rutas SVG vía `offset-path`, controlables con la Web Animations API para captura frame-exacta).
- **Arquetipos validados con contenido real:** proceso con mejora medible (A), jerarquía de capas (B), evolución/timeline (E), hub/red de categorías con grafo en anillo (H — motor `graph.py`, 4ª iteración tras calibrar contra 4 referencias reales de LinkedIn).
- **Paleta y componentes:** cuando hay una imagen de referencia "maestra", se extrae la paleta real por muestreo de píxeles (no a ojo) y se replica la anatomía de sus componentes (card con píldora de encabezado, panel punteado con leyenda, barra de hitos) — ver `system/palette.py`.
- **Manejo de errores:** si el matching no califica para ningún arquetipo (score < 55) o el humano rechaza la propuesta, el composer arma un layout propio desde la librería de módulos y registra el gap (`registry.json`) para priorizarlo o promoverlo a arquetipo de catálogo.
- **Salida bilingüe (regla de pipeline, no solo de este componente):** cada ejecución entrega dos activos del mismo post — `post_<id>_es.mp4`/`.png` y `post_<id>_en.mp4`/`.png` —, mismo data/layout/arquetipo, copy traducido. Cualquier etiqueta de UI fija en un módulo (ej. "Sí"/"No" en el rombo de decisión de `graph.py`) debe ser parametrizable, nunca quedar hardcodeada en español, o la variante en inglés sale con texto mezclado.

### `linkedin-post-qa-brand-check`
- **description:** "Valida copy + visual contra el brand kit (A2) y un checklist de LinkedIn: longitud de copy, legibilidad sin sonido, alt-text, hashtags (3–5), fuerza del hook en las primeras 2 líneas."
- **Patrón:** Reflection — puede rechazar y devolver a B2/B3 con feedback específico, máximo 2 ciclos antes de escalar a revisión humana.

### `linkedin-engagement-learner`
- **description:** "A las 48h de publicado, recoge métricas de engagement, las compara contra la hipótesis del pilar que originó el post, y anota el aprendizaje (qué hook/formato funcionó) para ajustar el próximo ciclo de `linkedin-trend-scout`."
- **Memoria:** apéndice a un log fechado (no reescribe el histórico), mismo patrón que `capture-learning` de tu paquete ai-native-os.

---

## 5. Skills/herramientas existentes que se reutilizan (no reinventar)

- `anthropic-skills:positioning-content-engine-builder` → base de A1.
- `brand-voice:generate-guidelines` / `brand-voice:discover-brand` → insumo para A2 si ya tienes materiales de marca dispersos.
- `brand-voice:brand-voice-enforcement` → se invoca dentro de B2 y B4.
- `design:design-system` → opcional para formalizar el brand kit visual de A2.
- `anthropic-skills:capture-learning` (patrón) → referencia de formato para B7.
- Tu arquitectura n8n existente (Docker, Airtable/Attio) → base de B5/B6, solo se agregan nodos nuevos (Unipile para publish, trigger semanal para B1).

---

## 6. Punto de aprobación humana (no negociable)

Consistente con tu filosofía ya documentada ("n8n determinístico + Claude razonando + aprobación humana"): **B6 siempre pausa y espera tu aprobación 1-click** antes de publicar. Nada en este pipeline publica en tu nombre sin ese gate.

---

## 7. Plan de testeo antes de replicar en el file system

1. Correr A1 y A2 una sola vez, a mano, conversacionalmente — validar que el brand kit y los pilares te representan.
2. Correr B1→B4 con una sola idea real, en esta misma conversación (sin n8n todavía) — validar calidad de copy y del GIF.
3. Recién ahí formalizar B1–B7 como paquetes de skill en `/mnt/skills` (tu flujo habitual: copy-to-tmp, editar, instalar).
4. Conectar B5/B6 a n8n con Unipile — probar publicación en modo "borrador" antes de activar el trigger automático.
5. Dejar correr B7 un ciclo completo antes de automatizar el loop de feedback hacia B1.

---

## 8. Siguiente paso concreto

¿Arrancamos por A1 (statement de posicionamiento + pilares) ahora mismo en esta conversación, o preferís que primero desarrolle el spec completo de `linkedin-animated-post-builder` (el componente nuevo más riesgoso del pipeline)?
