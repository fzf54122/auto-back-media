from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "auto_back_media_api" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "path" VARCHAR(100) NOT NULL,
    "method" VARCHAR(6) NOT NULL,
    "summary" VARCHAR(500) NOT NULL,
    "tags" VARCHAR(100) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_bb4219" ON "auto_back_media_api" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_a8be53" ON "auto_back_media_api" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_d6b13b" ON "auto_back_media_api" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_ae2264" ON "auto_back_media_api" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_876d93" ON "auto_back_media_api" ("is_deleted");
COMMENT ON COLUMN "auto_back_media_api"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_api"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_api"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_api"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_api"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_api"."path" IS 'API路径';
COMMENT ON COLUMN "auto_back_media_api"."method" IS '请求方法';
COMMENT ON COLUMN "auto_back_media_api"."summary" IS '请求简介';
COMMENT ON COLUMN "auto_back_media_api"."tags" IS 'API标签';
COMMENT ON TABLE "auto_back_media_api" IS 'API模型';
CREATE TABLE IF NOT EXISTS "auto_back_media_menu" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(20) NOT NULL,
    "remark" JSONB,
    "menu_type" VARCHAR(7),
    "icon" VARCHAR(100),
    "path" VARCHAR(100) NOT NULL,
    "order" INT NOT NULL DEFAULT 0,
    "parent_id" INT NOT NULL DEFAULT 0,
    "is_hidden" BOOL NOT NULL DEFAULT False,
    "component" VARCHAR(100) NOT NULL,
    "keepalive" BOOL NOT NULL DEFAULT True,
    "redirect" VARCHAR(100)
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_83cff9" ON "auto_back_media_menu" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_0eebaa" ON "auto_back_media_menu" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_866a2f" ON "auto_back_media_menu" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_90339d" ON "auto_back_media_menu" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_7410f6" ON "auto_back_media_menu" ("is_deleted");
COMMENT ON COLUMN "auto_back_media_menu"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_menu"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_menu"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_menu"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_menu"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_menu"."name" IS '菜单名称';
COMMENT ON COLUMN "auto_back_media_menu"."remark" IS '保留字段';
COMMENT ON COLUMN "auto_back_media_menu"."menu_type" IS '菜单类型';
COMMENT ON COLUMN "auto_back_media_menu"."icon" IS '菜单图标';
COMMENT ON COLUMN "auto_back_media_menu"."path" IS '菜单路径';
COMMENT ON COLUMN "auto_back_media_menu"."order" IS '排序';
COMMENT ON COLUMN "auto_back_media_menu"."parent_id" IS '父菜单ID';
COMMENT ON COLUMN "auto_back_media_menu"."is_hidden" IS '是否隐藏';
COMMENT ON COLUMN "auto_back_media_menu"."component" IS '组件';
COMMENT ON COLUMN "auto_back_media_menu"."keepalive" IS '存活';
COMMENT ON COLUMN "auto_back_media_menu"."redirect" IS '重定向';
COMMENT ON TABLE "auto_back_media_menu" IS '菜单模型';
CREATE TABLE IF NOT EXISTS "auto_back_media_role" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(20) NOT NULL UNIQUE,
    "desc" VARCHAR(500)
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_47e7ea" ON "auto_back_media_role" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_8f4abf" ON "auto_back_media_role" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_38a1a1" ON "auto_back_media_role" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_a99037" ON "auto_back_media_role" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_1cf944" ON "auto_back_media_role" ("is_deleted");
COMMENT ON COLUMN "auto_back_media_role"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_role"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_role"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_role"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_role"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_role"."name" IS '角色名称';
COMMENT ON COLUMN "auto_back_media_role"."desc" IS '角色描述';
COMMENT ON TABLE "auto_back_media_role" IS '权限模型';
CREATE TABLE IF NOT EXISTS "auto_back_media_audit_log" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "user_id" INT NOT NULL,
    "username" VARCHAR(64) NOT NULL DEFAULT '',
    "module" VARCHAR(64) NOT NULL DEFAULT '',
    "summary" VARCHAR(128) NOT NULL DEFAULT '',
    "method" VARCHAR(10) NOT NULL DEFAULT '',
    "path" VARCHAR(255) NOT NULL DEFAULT '',
    "status" INT NOT NULL DEFAULT -1,
    "response_time" INT NOT NULL DEFAULT 0,
    "request_args" JSONB,
    "response_body" JSONB
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_1fcfb3" ON "auto_back_media_audit_log" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_77e7d0" ON "auto_back_media_audit_log" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_1a69ab" ON "auto_back_media_audit_log" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_30934b" ON "auto_back_media_audit_log" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_1a8cbb" ON "auto_back_media_audit_log" ("is_deleted");
COMMENT ON COLUMN "auto_back_media_audit_log"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_audit_log"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_audit_log"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_audit_log"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_audit_log"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_audit_log"."user_id" IS '用户ID';
COMMENT ON COLUMN "auto_back_media_audit_log"."username" IS '用户名称';
COMMENT ON COLUMN "auto_back_media_audit_log"."module" IS '功能模块';
COMMENT ON COLUMN "auto_back_media_audit_log"."summary" IS '请求描述';
COMMENT ON COLUMN "auto_back_media_audit_log"."method" IS '请求方法';
COMMENT ON COLUMN "auto_back_media_audit_log"."path" IS '请求路径';
COMMENT ON COLUMN "auto_back_media_audit_log"."status" IS '状态码';
COMMENT ON COLUMN "auto_back_media_audit_log"."response_time" IS '响应时间(单位ms)';
COMMENT ON COLUMN "auto_back_media_audit_log"."request_args" IS '请求参数';
COMMENT ON COLUMN "auto_back_media_audit_log"."response_body" IS '返回数据';
CREATE TABLE IF NOT EXISTS "auto_back_media_user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "alias" VARCHAR(30),
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "phone" VARCHAR(20),
    "password" VARCHAR(128),
    "is_superuser" BOOL NOT NULL DEFAULT False,
    "last_login" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_70608e" ON "auto_back_media_user" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_e73c95" ON "auto_back_media_user" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_1debeb" ON "auto_back_media_user" ("updated_at");
COMMENT ON COLUMN "auto_back_media_user"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_user"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_user"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_user"."is_active" IS '是否激活';
COMMENT ON COLUMN "auto_back_media_user"."is_deleted" IS '软删除标记';
COMMENT ON COLUMN "auto_back_media_user"."username" IS '用户名称';
COMMENT ON COLUMN "auto_back_media_user"."alias" IS '姓名';
COMMENT ON COLUMN "auto_back_media_user"."email" IS '邮箱';
COMMENT ON COLUMN "auto_back_media_user"."phone" IS '电话';
COMMENT ON COLUMN "auto_back_media_user"."password" IS '密码';
COMMENT ON COLUMN "auto_back_media_user"."is_superuser" IS '是否为超级管理员';
COMMENT ON COLUMN "auto_back_media_user"."last_login" IS '最后登录时间';
COMMENT ON TABLE "auto_back_media_user" IS '用户表';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "auto_back_media_role_auto_back_media_api" (
    "auto_back_media_role_id" BIGINT NOT NULL REFERENCES "auto_back_media_role" ("id") ON DELETE CASCADE,
    "apimodel_id" BIGINT NOT NULL REFERENCES "auto_back_media_api" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_auto_back_m_auto_ba_09779c" ON "auto_back_media_role_auto_back_media_api" ("auto_back_media_role_id", "apimodel_id");
CREATE TABLE IF NOT EXISTS "auto_back_media_role_auto_back_media_menu" (
    "auto_back_media_role_id" BIGINT NOT NULL REFERENCES "auto_back_media_role" ("id") ON DELETE CASCADE,
    "menumodel_id" BIGINT NOT NULL REFERENCES "auto_back_media_menu" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_auto_back_m_auto_ba_110c6f" ON "auto_back_media_role_auto_back_media_menu" ("auto_back_media_role_id", "menumodel_id");
CREATE TABLE IF NOT EXISTS "auto_back_media_user_auto_back_media_role" (
    "auto_back_media_user_id" BIGINT NOT NULL REFERENCES "auto_back_media_user" ("id") ON DELETE CASCADE,
    "rolemodel_id" BIGINT NOT NULL REFERENCES "auto_back_media_role" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_auto_back_m_auto_ba_895161" ON "auto_back_media_user_auto_back_media_role" ("auto_back_media_user_id", "rolemodel_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
