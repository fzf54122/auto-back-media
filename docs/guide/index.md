# 快速开始

本指南将帮助您快速搭建和运行 auto-back-media 项目。

## 📋 前置要求

- Python 3.12+
- PostgreSQL 14+
- Redis 6+
- Git
- UV (Python 包管理器)

## 🚀 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/fzf/auto-back-media.git
cd auto-back-media
```

### 2. 安装依赖

使用 UV 安装项目依赖：

```bash
uv sync
```

### 3. 配置环境变量

复制 `.env.example` 文件为 `.env` 并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库、Redis 等参数：

```env
# 数据库配置
DATABASE_URL=postgres://username:password@localhost:5432/auto_back_media

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# JWT 配置
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 应用配置
APP_NAME=auto-back-media
DEBUG=True
```

### 4. 数据库迁移

运行数据库迁移命令：

```bash
uv run aerich init-db
uv run aerich migrate
uv run aerich upgrade
```

### 5. 启动项目

```bash
uv run uvicorn application.wsgi:app --reload
```

项目将在 `http://localhost:8000` 启动。

## 📖 访问文档

### API 文档

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 项目文档

本地预览文档：

```bash
uv run mkdocs serve
```

文档将在 `http://localhost:8001` 访问。

## 🧪 运行测试

```bash
uv run pytest
```

## 📦 构建和部署

### 构建文档

```bash
uv run mkdocs build
```

### 部署到 GitHub Pages

```bash
uv run mkdocs gh-deploy
```

## 🔧 开发工具

- **代码格式化**: `uv run ruff format`
- **代码检查**: `uv run ruff check`
- **类型检查**: `uv run mypy`