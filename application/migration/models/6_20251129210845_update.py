from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "auto_back_media_media_user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "project_name" VARCHAR(255),
    "media_type" VARCHAR(255),
    "media_username" VARCHAR(255),
    "media_passwd" VARCHAR(255),
    "last_login" TIMESTAMPTZ,
    "token" VARCHAR(255),
    "status" INT NOT NULL DEFAULT 10
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_028591" ON "auto_back_media_media_user" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_af9460" ON "auto_back_media_media_user" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_fa5ab7" ON "auto_back_media_media_user" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_e22bc8" ON "auto_back_media_media_user" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_3d1c3d" ON "auto_back_media_media_user" ("is_deleted");
COMMENT ON COLUMN "auto_back_media_media_user"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_media_user"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_media_user"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_media_user"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_media_user"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_media_user"."project_name" IS '平台名称';
COMMENT ON COLUMN "auto_back_media_media_user"."media_type" IS '媒体类型';
COMMENT ON COLUMN "auto_back_media_media_user"."media_username" IS '媒体账号';
COMMENT ON COLUMN "auto_back_media_media_user"."media_passwd" IS '媒体密码';
COMMENT ON COLUMN "auto_back_media_media_user"."last_login" IS '最后使用时间';
COMMENT ON COLUMN "auto_back_media_media_user"."token" IS '用户Token';
COMMENT ON COLUMN "auto_back_media_media_user"."status" IS '用户状态';
        CREATE TABLE IF NOT EXISTS "auto_back_media_media_tasks" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "project_name" VARCHAR(255),
    "media_type" VARCHAR(255),
    "media_username" VARCHAR(255),
    "task_topic" VARCHAR(255),
    "crontab_time" TIMESTAMPTZ,
    "last_time" TIMESTAMPTZ,
    "status" INT NOT NULL DEFAULT 10
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_7e4bd2" ON "auto_back_media_media_tasks" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_126391" ON "auto_back_media_media_tasks" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_efd9ca" ON "auto_back_media_media_tasks" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_59061f" ON "auto_back_media_media_tasks" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_a765c4" ON "auto_back_media_media_tasks" ("is_deleted");
COMMENT ON COLUMN "auto_back_media_media_tasks"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_media_tasks"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_media_tasks"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_media_tasks"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_media_tasks"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_media_tasks"."project_name" IS '平台名称';
COMMENT ON COLUMN "auto_back_media_media_tasks"."media_type" IS '媒体类型';
COMMENT ON COLUMN "auto_back_media_media_tasks"."media_username" IS '媒体账号';
COMMENT ON COLUMN "auto_back_media_media_tasks"."task_topic" IS '任务话题';
COMMENT ON COLUMN "auto_back_media_media_tasks"."crontab_time" IS '最后使用时间';
COMMENT ON COLUMN "auto_back_media_media_tasks"."last_time" IS '最后使用时间';
COMMENT ON COLUMN "auto_back_media_media_tasks"."status" IS '任务状态';
        CREATE TABLE IF NOT EXISTS "auto_back_media_webs" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "project_type" VARCHAR(50) NOT NULL,
    "project_url" VARCHAR(100)
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_dccc2d" ON "auto_back_media_webs" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_52abf2" ON "auto_back_media_webs" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_9d601d" ON "auto_back_media_webs" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_project_545e12" ON "auto_back_media_webs" ("project_type");
COMMENT ON COLUMN "auto_back_media_webs"."description" IS '项目描述';
COMMENT ON COLUMN "auto_back_media_webs"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_webs"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_webs"."is_active" IS '是否激活';
COMMENT ON COLUMN "auto_back_media_webs"."is_deleted" IS '软删除标记';
COMMENT ON COLUMN "auto_back_media_webs"."project_type" IS '平台类型';
COMMENT ON COLUMN "auto_back_media_webs"."project_url" IS '平台URL';
COMMENT ON TABLE "auto_back_media_webs" IS '网站记录表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "auto_back_media_media_tasks";
        DROP TABLE IF EXISTS "auto_back_media_webs";
        DROP TABLE IF EXISTS "auto_back_media_media_user";"""


MODELS_STATE = (
    "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"
)
