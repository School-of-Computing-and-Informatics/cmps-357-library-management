# Workflow Directory

This directory contains workflow diagrams and process flows for library operations.

## Contents

- **reserve_room.mmd** - Mermaid diagram source for the room reservation workflow
- **check-out-item.mmd** - Mermaid diagram source for the item checkout workflow

Workflow diagrams illustrate the step-by-step processes for various library operations, showing decision points, validation steps, and outcomes. These diagrams are useful for understanding system behavior and designing implementation logic.

## How to Render/Preview

- In VS Code: install a Mermaid preview extension (e.g., “Markdown Preview Mermaid Support”) and open the `.mmd` file to preview the diagram.
- With Mermaid CLI (optional):

	```powershell
	# Install mermaid-cli (requires Node.js)
	npm install -g @mermaid-js/mermaid-cli

	# Render to SVG
	mmdc -i reserve_room.mmd -o reserve_room.svg
	mmdc -i check-out-item.mmd -o check-out-item.svg
	```

Note: Rendered SVGs are not committed by default; generate them locally as needed.
