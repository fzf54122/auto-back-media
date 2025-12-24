# Makefile for auto-back-media
.DEFAULT_GOAL := help
SHELL := /bin/bash

# -------- Config (按需改) --------
APP ?= application.main:app         # FastAPI app import path（不对就改这里）
HOST ?= 0.0.0.0
PORT ?= 10001
ENV  ?= dev                         # dev/prod 之类（你也可以不用）
PYTHONPATH ?= application

# -------- Detect runner: uv > hatch > python --------
HAS_UV    := $(shell command -v uv >/dev/null 2>&1 && echo 1 || echo 0)
HAS_HATCH := $(shell command -v hatch >/dev/null 2>&1 && echo 1 || echo 0)

ifeq ($(HAS_UV),1)
	RUN := uv run
	INSTALL_DEV := uv sync --group dev
	INSTALL_DOCS := uv sync --group docs
	INSTALL_ALL := uv sync --group dev --group docs
else ifeq ($(HAS_HATCH),1)
	RUN := hatch run
	# hatch 自己不负责“安装 group”，通常你用 pip/uv 来装依赖；
	# 这里给个兜底：直接按 extras 装（你 pyproject 里也有 optional-dependencies: dev/test）
	INSTALL_DEV := python -m pip install -U pip && python -m pip install -e ".[dev,test]"
	INSTALL_DOCS := python -m pip install -U pip && python -m pip install -e ".[dev,test]" && python -m pip install -U "mkdocs" "mkdocs-material"
	INSTALL_ALL := $(INSTALL_DEV) && $(INSTALL_DOCS)
else
	RUN := python
	INSTALL_DEV := python -m pip install -U pip && python -m pip install -e ".[dev,test]"
	INSTALL_DOCS := python -m pip install -U pip && python -m pip install -U "mkdocs" "mkdocs-material"
	INSTALL_ALL := $(INSTALL_DEV) && $(INSTALL_DOCS)
endif

# -------- Common env --------
export PYTHONPATH := $(PYTHONPATH)

.PHONY: help info install install-dev install-docs \
        run run-reload test cov lint fmt format check type \
        aerich-init aerich-migrate aerich-upgrade aerich-downgrade aerich-history \
        docs docs-serve clean

help: ## 显示帮助
	@awk 'BEGIN {FS=":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

info: ## 打印当前执行器（uv/hatch/python）
	@echo "HAS_UV=$(HAS_UV) HAS_HATCH=$(HAS_HATCH)"
	@echo "RUN='$(RUN)'"
	@echo "APP='$(APP)' HOST=$(HOST) PORT=$(PORT)"
	@echo "PYTHONPATH=$(PYTHONPATH)"

install: ## 安装 dev+docs 依赖（uv: group；无 uv: extras/兜底）
	$(INSTALL_ALL)

install-dev: ## 只安装开发依赖
	$(INSTALL_DEV)

install-docs: ## 只安装文档依赖
	$(INSTALL_DOCS)

# ---------- Run ----------
run: ## 启动服务（生产模式）
	$(RUN) uvicorn $(APP) --host $(HOST) --port $(PORT)

run-reload: ## 启动服务（开发热重载）
	$(RUN) uvicorn $(APP) --reload --host $(HOST) --port $(PORT)

# ---------- Quality ----------
format: fmt ## alias

fmt: ## 格式化（ruff format）
	$(RUN) ruff format .

lint: ## 静态检查（ruff check）
	$(RUN) ruff check .

check: lint type test ## 一键检查：lint + type + test

type: ## 类型检查（mypy）
	$(RUN) mypy .

test: ## 跑测试（pytest）
	$(RUN) pytest

cov: ## 测试覆盖率
	$(RUN) pytest --cov=application --cov-report=term-missing

# ---------- DB Migrations (Aerich) ----------
aerich-init: ## 初始化迁移（首次使用：会创建 migration 表）
	$(RUN) aerich init-db

aerich-migrate: ## 生成迁移文件（需要写 message：make aerich-migrate m="xxx"）
	@if [ -z "$(m)" ]; then echo "❌ 缺少参数 m，例如：make aerich-migrate m='add user table'"; exit 2; fi
	$(RUN) aerich migrate --name "$(m)"

aerich-upgrade: ## 应用迁移
	$(RUN) aerich upgrade

aerich-downgrade: ## 回滚一次迁移
	$(RUN) aerich downgrade

aerich-history: ## 查看迁移历史
	$(RUN) aerich history

# ---------- Docs ----------
docs: ## 构建文档（mkdocs build）
	$(RUN) mkdocs build

docs-serve: ## 本地预览文档（mkdocs serve）
	$(RUN) mkdocs serve -a 127.0.0.1:8001

# ---------- Clean ----------
clean: ## 清理缓存/构建产物
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml htmlcov dist build *.egg-info
	find . -type d -name "__pycache__" -print0 | xargs -0 rm -rf
