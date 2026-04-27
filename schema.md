# Schema for LLM Wiki

This document outlines the structure, conventions, and workflows for maintaining the LLM Wiki. It serves as the primary instruction set for the LLM agent.

## 1. Wiki Structure

The wiki is organized into the following top-level directories:

- `raw/`: Contains original, immutable source documents (e.g., articles, papers, web pages). These files are never modified by the LLM.
- `wiki/`: Contains all LLM-generated markdown files, forming the knowledge base.
    - `wiki/entities/`: Dedicated pages for specific entities (people, organizations, products, tools).
    - `wiki/concepts/`: Dedicated pages for abstract concepts, theories, and methodologies.
    - `wiki/sources/`: Summaries and key takeaways from ingested raw source documents.
    - `wiki/index.md`: A comprehensive, categorized index of all pages within the `wiki/` directory.
    - `wiki/log.md`: A chronological record of all LLM operations (ingestions, queries, linting).
- `scripts/`: Stores Python scripts and other executable files for ingestion, querying, and maintenance.

## 2. File Conventions

### 2.1. Markdown Format
All wiki pages are standard Markdown (`.md`) files.

### 2.2. Page Naming
- Entity pages: `[Entity Name].md` (e.g., `Andrej Karpathy.md`)
- Concept pages: `[Concept Name].md` (e.g., `Retrieval Augmented Generation.md`)
- Source pages: `[Source Title or Identifier].md` (e.g., `Karpathy LLM Wiki Gist.md`)

### 2.3. Frontmatter
Each wiki page MUST include YAML frontmatter at the top, providing metadata. The required fields are:

```yaml
---
title: "Page Title"
summary: "A concise, one-sentence summary of the page content."
tags: ["#tag1", "#tag2"]
created: YYYY-MM-DDTHH:MM:SSZ
last_updated: YYYY-MM-DDTHH:MM:SSZ
source_links: ["[[Source 1]]", "[[Source 2]]"]
---
```

- `title`: The main title of the page.
- `summary`: A brief, descriptive summary used by the LLM for quick relevance assessment.
- `tags`: A list of relevant tags (e.g., `#LLMs`, `#AI`, `#KnowledgeManagement`).
- `created`: Timestamp of page creation in ISO 8601 format.
- `last_updated`: Timestamp of the last modification in ISO 8601 format.
- `source_links`: A list of internal wiki links to `wiki/sources/` pages that contributed to this page's content.

### 2.4. Content Structure
- Pages should be focused on a single entity, concept, or source summary.
- Use clear headings and subheadings to organize content.
- Employ `[[Wiki Links]]` to create connections between related pages within the `wiki/` directory. For example, `[[Andrej Karpathy]]` or `[[Retrieval Augmented Generation]]`.

## 3. Operations and Workflows

### 3.1. Ingestion Process
When a new raw source is provided:
1. The LLM reads the raw source document.
2. It extracts key information, main ideas, and relevant entities/concepts.
3. A new markdown file is created in `wiki/sources/` summarizing the raw document. This summary includes frontmatter and links to any new or updated entity/concept pages.
4. The LLM identifies existing `wiki/entities/` and `wiki/concepts/` pages that are relevant to the new source. These pages are updated to incorporate new information, resolve contradictions, and add `source_links` to the new source page.
5. If new entities or concepts are identified, new pages are created in their respective directories with appropriate frontmatter and initial content.
6. `wiki/index.md` is updated to include the new source page and any new entity/concept pages.
7. An entry is appended to `wiki/log.md` detailing the ingestion event.

### 3.2. Querying Process
When a query is received:
1. The LLM first consults `wiki/index.md` to identify potentially relevant wiki pages.
2. It then reads the identified pages, focusing on summaries and content.
3. The LLM synthesizes an answer based on the information found, citing relevant wiki pages.
4. If the answer itself contains valuable, synthesizable knowledge, the LLM may propose creating a new wiki page for it or updating existing ones.

### 3.3. Linting Process
Periodically, the LLM performs a linting operation to maintain wiki health:
1. **Contradiction Check**: Identifies conflicting information across pages.
2. **Stale Claims**: Flags information that might be outdated by newer sources.
3. **Orphan Pages**: Detects pages with no inbound links.
4. **Missing Pages**: Identifies mentioned concepts/entities that lack their own dedicated page.
5. **Cross-referencing Gaps**: Suggests new links between related pages.
6. **Data Gaps**: Recommends areas for further research or new sources.

## 4. LLM Interaction Guidelines

- **Transparency**: All modifications to the wiki MUST be logged in `wiki/log.md`.
- **Consistency**: Adhere strictly to the defined file conventions and structure.
- **Clarity**: Prioritize clear, concise, and unambiguous language in all generated content.
- **Modularity**: Keep pages focused; split large topics into smaller, interlinked pages when appropriate.
- **Human Guidance**: The LLM should seek clarification or guidance from the user when ambiguities arise or significant decisions need to be made regarding content integration or structural changes.
