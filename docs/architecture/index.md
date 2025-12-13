# 架构设计

## 📐 整体架构

auto-back-media 采用三层架构设计，确保代码的可维护性、可扩展性和可测试性。

### 三层架构

1. **表示层 (Presentation Layer)**
   - 处理 HTTP 请求和响应
   - 路由配置和参数验证
   - 位于 `application/apis.py` 和各模块的 `apis/` 目录

2. **业务逻辑层 (Business Logic Layer)**
   - 实现核心业务逻辑
   - 处理数据转换和业务规则
   - 位于各模块的 `services/` 目录

3. **数据访问层 (Data Access Layer)**
   - 与数据库交互
   - 定义数据模型和 ORM 映射
   - 位于各模块的 `models/` 目录

## 📁 目录结构

```
application/
├── __init__.py              # 应用初始化
├── apis.py                  # API 路由配置
├── app_base/                # 基础模块
│   ├── apis/                # 基础 API
│   ├── models/              # 基础数据模型
│   ├── serializers/         # 基础序列化器
│   ├── services/            # 基础服务
│   └── utils.py             # 基础工具
├── app_manage/              # 管理模块
│   ├── apis/                # 管理 API
│   ├── models/              # 管理数据模型
│   ├── serializers/         # 管理序列化器
│   └── services/            # 管理服务
├── app_system/              # 系统模块
│   ├── apis/                # 系统 API
│   ├── models/              # 系统数据模型
│   ├── serializers/         # 系统序列化器
│   └── services/            # 系统服务
├── authentication.py        # 认证相关
├── enums.py                 # 枚举定义
├── models.py                # 数据模型导入
├── pagination.py            # 分页功能
└── wsgi.py                  # WSGI 入口
```

## 🧩 核心模块

### 1. 基础模块 (app_base)

提供系统基础功能：
- 文件管理
- 部门管理
- 角色管理
- 权限管理
- 审计日志

### 2. 管理模块 (app_manage)

提供媒体内容管理功能：
- 媒体用户管理
- 任务管理
- 网站管理

### 3. 系统模块 (app_system)

提供系统配置和用户管理功能：
- 用户管理
- 系统设置
- 登录认证

## 🔧 技术组件

### 认证与授权

- **JWT**: 用于生成和验证访问令牌
- **RBAC**: 基于角色的访问控制模型
- **密码加密**: 使用 Argon2 和 bcrypt 进行密码哈希

### 数据库

- **PostgreSQL**: 主数据库，存储结构化数据
- **Tortoise ORM**: 异步 ORM 框架
- **Aerich**: 数据库迁移工具

### 缓存

- **Redis**: 用于缓存热点数据和存储会话信息

### 任务调度

- **APScheduler**: 用于执行定时任务和异步任务

### 日志

- **Loguru**: 提供结构化日志记录

## 📡 API 设计

采用 RESTful API 设计风格：

- **GET**: 获取资源
- **POST**: 创建资源
- **PUT**: 更新资源
- **DELETE**: 删除资源

所有 API 都遵循统一的响应格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 🛡️ 安全设计

- **输入验证**: 使用 Pydantic 进行严格的输入验证
- **SQL 注入防护**: 使用 ORM 避免直接 SQL 操作
- **XSS 防护**: 对输出内容进行适当转义
- **CSRF 防护**: 实现 CSRF 令牌验证
- **请求限流**: 使用 SlowAPI 实现请求速率限制

## 📈 性能优化

- **异步处理**: 使用 FastAPI 的异步特性提高并发性能
- **缓存策略**: 对热点数据进行缓存
- **分页查询**: 避免一次性加载大量数据
- **数据库索引**: 合理设计数据库索引