# Trading Agent Wiki Design

## Goal

Initialize an Obsidian-based LLM wiki for the `trading-agent` project that serves two collaborators and supports three overlapping needs:

- project knowledge accumulation
- operational project tracking
- software-specific documentation

The vault should start simple, stay readable, and expand gradually as more sources and project state accumulate.

## Project Shape

This vault is not a generic personal second brain. It is a focused project wiki for a broad initiative that combines:

- software development
- research
- economic and market reasoning

The vault should therefore avoid over-specializing too early around only one of these dimensions.

## Users

The primary readers and maintainers are two collaborators working on the same project. The wiki must therefore optimize for:

- shared readability
- explicit project state
- durable memory across sessions
- clear separation between raw inputs, distilled knowledge, and active work

## Design Principles

1. Start with a minimal structure that can absorb growth without immediate refactoring.
2. Keep `raw/` as the single intake surface for new material.
3. Make the vault operational on day one, not only archival.
4. Preserve a wiki-first model underneath a task-oriented surface.
5. Let visual artifacts coexist with markdown knowledge rather than replace it.

## Recommended Structure

```text
trading-agent-wiki/
├── AGENTS.md
├── raw/
│   ├── articles/
│   ├── papers/
│   ├── audio/
│   ├── transcripts/
│   ├── notes/
│   └── archived/
├── wiki/
│   ├── _meta/
│   │   ├── index.md
│   │   ├── log.md
│   │   ├── taxonomy.md
│   │   └── hot-cache.md
│   ├── overview.md
│   ├── sources/
│   ├── concepts/
│   ├── entities/
│   ├── syntheses/
│   ├── questions/
│   ├── decisions/
│   ├── ops/
│   ├── build/
│   └── artifacts/
└── docs/
    └── superpowers/
        └── specs/
```

## Folder Roles

### `raw/`

The intake layer for all incoming material. It should accept both formal and informal sources, including:

- conversation audio
- transcripts
- research papers
- articles
- raw ideas
- unstructured notes

`raw/archived/` stores sources after ingest. Nothing should be deleted.

### `wiki/sources/`

Normalized pages representing ingested source material. Each meaningful raw source should map to one source page that captures summary, relevance, and downstream links.

### `wiki/concepts/`

Reusable project ideas and abstractions, such as strategies, modeling concepts, metrics, frameworks, patterns, and terminology.

### `wiki/entities/`

Named things that matter to the project, such as brokers, APIs, exchanges, companies, assets, libraries, tools, institutions, or people.

### `wiki/syntheses/`

High-value derived knowledge. This includes analyses, comparisons, summaries, memos, and durable answers worth preserving after research or discussion.

### `wiki/questions/`

Open problems, unresolved assumptions, validation gaps, and research questions.

### `wiki/decisions/`

Decision records for meaningful project choices. These pages should explain what was chosen, why, under what constraints, and what remains uncertain.

### `wiki/ops/`

The live operational layer of the project. This is where the current state, priorities, workstreams, and near-term execution context should live.

This folder gives the vault its task-oriented surface.

### `wiki/build/`

The software-specific layer. This section is reserved for knowledge tightly coupled to the software itself, including:

- architecture
- components
- flows
- integrations
- technical constraints
- infrastructure notes
- implementation-oriented design knowledge

This keeps software detail visible without polluting general research or project notes.

### `wiki/artifacts/`

A home for visual and structured artifacts that coexist with the wiki, especially:

- concept maps
- mind maps
- Obsidian canvas files
- diagrams
- structured supporting views

Artifacts should supplement markdown pages, not replace them. A decision, synthesis, or build note can link to an artifact when a visual representation adds value.

## Operational Model

The vault should follow this information flow:

1. New material lands in `raw/`.
2. Important material is ingested into `wiki/sources/`.
3. Knowledge is distilled into `concepts/`, `entities/`, `syntheses/`, and `questions/`.
4. Actionable impact flows into `decisions/`, `ops/`, and `build/`.
5. `wiki/overview.md` reflects the current high-level picture of the project.
6. `wiki/_meta/` maintains continuity, governance, and discoverability.

This creates a clear progression from intake to understanding to execution.

## Information Architecture Strategy

The vault should be task-oriented at the top and wiki-oriented underneath.

In practice, this means:

- the surface experience should help collaborators understand project status quickly
- the deeper structure should preserve cumulative knowledge in a durable, linkable format

This balance is preferable to either extreme:

- a pure wiki would underserve day-to-day execution
- a pure project tracker would underserve long-term reasoning and memory

## Governance

### Local Constitution

The vault should contain a local `AGENTS.md` in its root. It will serve as the vault-specific operating contract for future agents working inside this directory.

### Meta Files

The initial governance layer should include:

- `wiki/_meta/index.md` for discoverability
- `wiki/_meta/log.md` for append-only operational history
- `wiki/_meta/taxonomy.md` for canonical tags
- `wiki/_meta/hot-cache.md` for session continuity

### Frontmatter Strategy

Use one standard frontmatter shape across wiki pages, with a small number of extra fields when useful for project and software material.

Recommended baseline fields:

- `title`
- `type`
- `tags`
- `sources`
- `created`
- `updated`
- `status`
- `related`
- `confidence`

Recommended optional fields for this vault:

- `priority`
- `area`
- `decision_status`

The taxonomy should start small and intentional. Avoid premature over-classification.

## Artifact Strategy

Artifacts are a first-class part of the vault, but not the primary storage format for knowledge.

The intended model is:

- markdown remains the source of durable prose knowledge
- artifacts provide visual leverage where text alone is insufficient
- artifact files live alongside the wiki, link back to notes, and remain navigable from the same structure

This allows the project to accumulate diagrams and mental maps without creating a second disconnected knowledge system.

## Non-Goals

The bootstrap should not attempt to solve all future structure in advance. It should specifically avoid:

- deep folder specialization before enough material exists
- heavy workflow automation before usage patterns are known
- splitting the vault into separate software, research, and business silos too early

## Initialization Outcome

The initialization phase should produce:

1. the folder structure described above
2. a local `AGENTS.md` aligned with this project
3. bootstrap files under `wiki/_meta/`
4. an initial `wiki/overview.md`
5. a taxonomy small enough to evolve safely

## Success Criteria

The initialization is successful if:

- both collaborators can understand where new information goes
- project state is visible without searching across random pages
- software-specific knowledge has a dedicated home
- research and market knowledge can accumulate without clutter
- artifacts can live in the same system as notes
- the vault can grow for several weeks without structural regret

## Scope Check

This design is intentionally limited to vault initialization and information architecture. It does not define detailed ingest mechanics, templates for every note type, or advanced automations yet.

That narrower scope is appropriate for the first implementation plan.
