# AgenticEngineer — the entry points, so they are discoverable without prose.
# Every target is a thin wrapper over a PEP 723 script under tools/.

.DEFAULT_GOAL := help
.PHONY: help validate catalog youtube manifest check-media clean

help: ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

validate: ## Prove the repository layout is intact (run this first)
	uv run tools/tests/validate_structure.py

catalog: ## Rebuild the lesson catalog, its symlinks and INDEX.json
	uv run tools/catalog/build_catalog.py

youtube: ## Run the weekly YouTube update, then rebuild the index
	uv run tools/youtube/weekly_update.py
	uv run tools/youtube/rebuild_index.py

manifest: ## Regenerate media/MANIFEST.md (path + size + SHA-256)
	uv run tools/media/make_manifest.py

check-media: ## Verify media/ against the tracked manifest
	uv run tools/media/make_manifest.py --check

clean: ## Remove Python caches
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[cod]' -delete 2>/dev/null || true
	@echo "caches cleared"
