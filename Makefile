# =========================
# Configuration
# =========================

UV := uv

APP := src.main:app
HOST := 0.0.0.0
PORT := 8000

PYTHON_PATHS := src tests

# =========================
# Default target
# =========================

.DEFAULT_GOAL := help

# =========================
# Help
# =========================

.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "Dependencies:"
	@echo "  make sync          Sync project dependencies"
	@echo "  make sync-prod     Sync production dependencies only"
	@echo "  make add           Add a runtime dependency"
	@echo "  make add-dev       Add a development dependency"
	@echo "  make remove        Remove a dependency"
	@echo ""
	@echo "Application:"
	@echo "  make run           Run FastAPI"
	@echo "  make dev           Run FastAPI with reload"
	@echo ""
	@echo "Quality:"
	@echo "  make lint          Run Ruff linter"
	@echo "  make format        Format code with Ruff"
	@echo "  make format-check  Check code formatting"
	@echo "  make type-check    Run MyPy type checking"
	@echo "  make fix           Fix lint and formatting issues"
	@echo ""
	@echo "Tests:"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage"
	@echo "  make check         Run all quality checks and tests"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         Remove caches and generated files"

# =========================
# Dependencies
# =========================

.PHONY: sync
sync:
	@echo "Syncing project dependencies..."
	@$(UV) sync

.PHONY: sync-prod
sync-prod:
	@echo "Syncing production dependencies..."
	@$(UV) sync --frozen --no-dev

.PHONY: add
add:
	@read -p "Package: " pkg; \
	echo "Adding runtime dependency: $$pkg"; \
	$(UV) add $$pkg

.PHONY: add-dev
add-dev:
	@read -p "Development package: " pkg; \
	echo "Adding development dependency: $$pkg"; \
	$(UV) add --dev $$pkg

.PHONY: remove
remove:
	@read -p "Package: " pkg; \
	echo "Removing dependency: $$pkg"; \
	$(UV) remove $$pkg

# =========================
# FastAPI / Uvicorn
# =========================

.PHONY: run
run:
	@echo "Starting FastAPI..."
	@$(UV) run uvicorn $(APP) --host $(HOST) --port $(PORT)

.PHONY: dev
dev:
	@echo "Starting FastAPI in development mode..."
	@$(UV) run uvicorn $(APP) --reload --host $(HOST) --port $(PORT)

# =========================
# Quality
# =========================

.PHONY: lint
lint:
	@echo "Running Ruff linter..."
	@$(UV) run ruff check $(PYTHON_PATHS)

.PHONY: format
format:
	@echo "Formatting code with Ruff..."
	@$(UV) run ruff format $(PYTHON_PATHS)

.PHONY: format-check
format-check:
	@echo "Checking code formatting..."
	@$(UV) run ruff format --check $(PYTHON_PATHS)

.PHONY: type-check
type-check:
	@echo "Running MyPy type checking..."
	@$(UV) run mypy $(PYTHON_PATHS)

.PHONY: fix
fix:
	@echo "Fixing lint issues..."
	@$(UV) run ruff check $(PYTHON_PATHS) --fix
	@echo "Formatting code..."
	@$(UV) run ruff format $(PYTHON_PATHS)

# =========================
# Tests
# =========================

.PHONY: test
test:
	@echo "Running tests..."
	@$(UV) run pytest

.PHONY: test-cov
test-cov:
	@echo "Running tests with coverage..."
	@$(UV) run pytest \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=html

.PHONY: check
check: lint format-check type-check test
	@echo "All checks passed."

# =========================
# Maintenance
# =========================

.PHONY: clean
clean:
	@echo "Cleaning caches and generated files..."

	@find . -type d \( \
		-name "__pycache__" \
		-o -name ".pytest_cache" \
		-o -name ".ruff_cache" \
		-o -name ".mypy_cache" \
		-o -name "htmlcov" \
	\) -prune -exec rm -rf {} +

	@find . -type f \( \
		-name "*.pyc" \
		-o -name "*.pyo" \
	\) -delete

	@echo "Cleanup completed."
