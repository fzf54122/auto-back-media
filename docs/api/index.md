# API 文档

欢迎使用 auto-back-media 的 API 文档。本文档提供了系统所有 API 的详细说明，包括请求参数、响应格式和使用示例。

## 📖 文档说明

### API 基础信息

- **API 根路径**: `/api/v1`
- **认证方式**: JWT Token
- **响应格式**: JSON
- **错误处理**: 统一的错误响应格式

### 认证方式

所有需要认证的 API 都需要在请求头中携带 JWT Token：

```
Authorization: Bearer <your-token>
```

### 响应格式

#### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 响应数据
  }
}
```

#### 错误响应

```json
{
  "code": 400,
  "message": "错误信息",
  "details": {
    // 错误详情（可选）
  }
}
```

### 状态码

| 状态码 | 描述 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 📚 API 分类

### 基础 API

- [认证授权](base.md): 登录、注册、获取令牌等

### 用户管理 API

- [用户管理](users.md): 用户的增删改查、权限管理等

### 角色管理 API

- [角色管理](role.md): 角色的增删改查、权限分配等

### 文件管理 API

- [文件管理](files.md): 文件上传、下载、删除等

### API 权限管理

- [API 权限](api.md): API 权限的管理和分配

## 🧪 测试 API

您可以使用以下工具测试 API：

1. **Swagger UI**: `http://localhost:8000/docs`
2. **ReDoc**: `http://localhost:8000/redoc`
3. **Postman**: 导入 API 文档进行测试
4. **curl**: 命令行测试工具

## 📝 示例

### 使用 curl 测试 API

```bash
# 登录获取令牌
curl -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 使用令牌访问受保护的 API
curl -X GET "http://localhost:8000/api/v1/users" \
  -H "Authorization: Bearer <your-token>"
```