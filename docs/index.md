# auto-back-media

自动化媒体发布后端项目

## 📖 项目简介

auto-back-media 是一个基于 FastAPI 构建的自动化媒体发布后端项目，提供完整的媒体内容管理、用户权限控制和自动化发布功能。

## ✨ 核心功能

- **媒体内容管理**：支持多种媒体类型的上传、存储和管理
- **用户权限控制**：基于 RBAC 模型的细粒度权限管理
- **自动化发布**：支持定时任务和批量发布功能
- **API 文档**：自动生成的交互式 API 文档
- **日志系统**：完善的日志记录和监控功能

![核心特性一览](images/features-overview.svg)

## 🛠️ 技术栈

- **后端框架**：FastAPI
- **数据库**：PostgreSQL
- **ORM**：Tortoise ORM
- **认证**：JWT
- **文档**：MkDocs + Material
- **任务调度**：APScheduler
- **缓存**：Redis

![技术栈](images/tech-stack.svg)

## 📦 快速开始

请参考 [快速开始](guide/index.md) 文档来搭建项目。

## 📚 文档目录

- [快速开始](guide/index.md)
- [架构设计](architecture/index.md)
- [API 文档](api/index.md)
- [更新日志](changelog.md)
- [常见问题](faq.md)