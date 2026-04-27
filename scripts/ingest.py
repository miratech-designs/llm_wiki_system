#!/usr/bin/env python3

import os
import sys
import datetime
import re
import yaml

# Configuration
WIKI_DIR = "wiki"
RAW_DIR = "raw"
SOURCES_DIR = os.path.join(WIKI_DIR, "sources")
ENTITIES_DIR = os.path.join(WIKI_DIR, "entities")
CONCEPTS_DIR = os.path.join(WIKI_DIR, "concepts")
INDEX_PATH = os.path.join(WIKI_DIR, "index.md")
LOG_PATH = os.path.join(WIKI_DIR, "log.md")

def ensure_dirs():
    for d in [SOURCES_DIR, ENTITIES_DIR, CONCEPTS_DIR, RAW_DIR]:
        os.makedirs(d, exist_ok=True)

def generate_frontmatter(title, summary, tags, source_links=None):
    if source_links is None:
        source_links = []
    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    data = {
        "title": title,
        "summary": summary,
        "tags": tags,
        "created": current_time,
        "last_updated": current_time,
        "source_links": source_links
    }
    return "---\n" + yaml.dump(data, sort_keys=False) + "---\n"

def update_index(page_title, relative_path, section="Sources"):
    if not os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "w") as f:
            f.write("# Wiki Index\n\n## Entities\n\n## Concepts\n\n## Sources\n")

    with open(INDEX_PATH, "r") as f:
        lines = f.readlines()

    new_lines = []
    section_found = False
    entry_exists = False
    entry_text = f"- [[{page_title}]] ({relative_path})\n"

    for line in lines:
        new_lines.append(line)
        if line.strip() == f"## {section}":
            section_found = True
        
        if section_found and line.strip() == entry_text.strip():
            entry_exists = True

    if section_found and not entry_exists:
        # Find the end of the section or next section
        idx = 0
        for i, line in enumerate(new_lines):
            if line.strip() == f"## {section}":
                idx = i + 1
                break
        new_lines.insert(idx, entry_text)
    elif not section_found:
        new_lines.append(f"\n## {section}\n")
        new_lines.append(entry_text)

    with open(INDEX_PATH, "w") as f:
        f.writelines(new_lines)

def update_log(entry):
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            f.write("# Wiki Log\n\n")
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(LOG_PATH, "a") as f:
        f.write(f"## [{timestamp}] {entry}\n")

def extract_metadata_placeholder(content, filename):
    """
    In a real system, this would call an LLM.
    Here we use regex and heuristics for demonstration.
    """
    title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
    summary = f"Automated ingestion of {filename}."
    tags = ["#ingested"]
    
    # Heuristic: find capitalized words as potential entities
    potential_entities = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', content)
    entities = list(set([e for e in potential_entities if len(e) > 3]))[:5] # Limit to 5
    
    return title, summary, tags, entities

def ingest_file(file_path):
    ensure_dirs()
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    filename = os.path.basename(file_path)
    with open(file_path, "r", errors="ignore") as f:
        content = f.read()

    title, summary, tags, entities = extract_metadata_placeholder(content, filename)
    
    # 1. Create Source Page
    source_filename = f"{title.replace(' ', '_')}.md"
    source_path = os.path.join(SOURCES_DIR, source_filename)
    
    frontmatter = generate_frontmatter(title, summary, tags)
    with open(source_path, "w") as f:
        f.write(frontmatter)
        f.write(f"\n# {title}\n\n")
        f.write("## Summary\n")
        f.write(f"{summary}\n\n")
        f.write("## Entities Mentioned\n")
        for entity in entities:
            f.write(f"- [[{entity}]]\n")
        f.write("\n## Raw Content Reference\n")
        f.write(f"Source file: `{file_path}`\n")

    update_index(title, os.path.join("sources", source_filename), "Sources")
    
    # 2. Create/Update Entity Pages (Simplified)
    for entity in entities:
        entity_filename = f"{entity.replace(' ', '_')}.md"
        entity_path = os.path.join(ENTITIES_DIR, entity_filename)
        
        if not os.path.exists(entity_path):
            e_frontmatter = generate_frontmatter(entity, f"Entity: {entity}", ["#entity"], [f"[[{title}]]"])
            with open(entity_path, "w") as f:
                f.write(e_frontmatter)
                f.write(f"\n# {entity}\n\n")
                f.write(f"This entity was first mentioned in [[{title}]].\n")
            update_index(entity, os.path.join("entities", entity_filename), "Entities")
        else:
            # In a real system, the LLM would update the existing page
            update_log(f"Updated entity page for [[{entity}]] with reference to [[{title}]]")

    update_log(f"Ingested source: [[{title}]]")
    print(f"Successfully ingested: {title}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/ingest.py <file1> <file2> ...")
    else:
        for arg in sys.argv[1:]:
            ingest_file(arg)
