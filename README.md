# LLM Wiki: Your Portable 2nd Brain

This system is a portable, Obsidian-free implementation of the "LLM Wiki" concept popularized by Andrej Karpathy. It focuses on building a persistent, interlinked knowledge base where an LLM acts as the primary maintainer.

## Structure

- `raw/`: Place your original source files (PDFs, Markdown, Text) here.
- `wiki/`: The core knowledge base.
    - `entities/`: Pages for people, organizations, and tools.
    - `concepts/`: Pages for ideas and methodologies.
    - `sources/`: Summaries of your raw documents.
    - `index.md`: A master index of all wiki pages.
    - `log.md`: A chronological log of all operations.
- `scripts/`: Utility scripts for managing the wiki.
- `schema.md`: The "instruction manual" for your LLM agent.

## Getting Started

1. **Setup**: Ensure you have Python installed with the `PyYAML` library (`pip install pyyaml`).
2. **Ingest**: To add a new document to your wiki, run:
   ```bash
   python3 scripts/ingest.py raw/your_document.md
   ```
3. **LLM Integration**: Point your favorite LLM agent (Claude Code, ChatGPT, etc.) to this folder. Share the `schema.md` file with it so it understands how to maintain the wiki for you.

## Core Philosophy

Unlike traditional RAG (Retrieval-Augmented Generation) which retrieves raw chunks at query time, this system compiles knowledge into a **persistent wiki**. The LLM updates existing pages and creates new ones as you add sources, ensuring that your knowledge base grows more structured and useful over time.

## Usage Tips

- **Obsidian Compatible**: While this system doesn't require Obsidian, it is fully compatible with it. You can open the `wiki/` folder as an Obsidian vault to visualize the graph of your knowledge.
- **Git Ready**: Since everything is plain text, you can initialize a Git repository in this folder to track changes and sync across devices.
- **Customizable**: Edit `schema.md` to change how the LLM organizes your data.
