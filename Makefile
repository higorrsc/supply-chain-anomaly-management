# =========================
# Config
# =========================

UV := uv
RUFF := ruff
PYTEST := pytest

APP :=
HOST := 0.0.0.0
PORT := 8000

# =========================
# Help
# =========================

.PHONY: help
help:
	@echo "Comandos disponíveis:"
	@echo "  make install       -> Instala dependências"
	@echo "  make sync          -> Sincroniza ambiente"
	@echo "  make run           -> Executa FastAPI"
	@echo "  make dev           -> Executa FastAPI com reload"
	@echo "  make lint          -> Executa lint com Ruff"
	@echo "  make format        -> Formata código"
	@echo "  make fix           -> Corrige problemas automaticamente"
	@echo "  make test          -> Executa testes"
	@echo "  make test-cov      -> Executa testes com cobertura"
	@echo "  make check         -> Lint + testes"
	@echo "  make clean         -> Remove caches"

# =========================
# Dependencies
# =========================

.PHONY: install
install:
	$(UV) sync

.PHONY: sync
sync:
	$(UV) sync

.PHONY: add
add:
	@read -p "Pacote: " pkg; \
	$(UV) add $$pkg

.PHONY: add-dev
add-dev:
	@read -p "Pacote dev: " pkg; \
	$(UV) add --dev $$pkg

# =========================
# FastAPI with Uvicorn
# =========================

.PHONY: run
run:
	$(UV) run uvicorn $(APP) --host $(HOST) --port $(PORT)

.PHONY: dev
dev:
	$(UV) run uvicorn $(APP) --reload --host $(HOST) --port $(PORT)

# =========================
# Quality
# =========================

.PHONY: lint
lint:
	$(UV) run $(RUFF) check .

.PHONY: format
format:
	$(UV) run $(RUFF) format .

.PHONY: fix
fix:
	$(UV) run $(RUFF) check . --fix

# =========================
# Tests
# =========================

.PHONY: test
test:
	$(UV) run $(PYTEST)

.PHONY: test-cov
test-cov:
	$(UV) run $(PYTEST) --cov=. --cov-report=term-missing

.PHONY: check
check: lint test

# =========================
# Clean
# =========================

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
