from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "auto_back_media_depts" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "name" VARCHAR(20) NOT NULL UNIQUE,
    "desc" VARCHAR(500),
    "order" INT NOT NULL DEFAULT 0,
    "parent_id" INT NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_66f21c" ON "auto_back_media_depts" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_7100b5" ON "auto_back_media_depts" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_8c92b4" ON "auto_back_media_depts" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_7a0ed2" ON "auto_back_media_depts" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_e6702e" ON "auto_back_media_depts" ("is_deleted");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_name_081710" ON "auto_back_media_depts" ("name");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_order_082632" ON "auto_back_media_depts" ("order");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_parent__a30239" ON "auto_back_media_depts" ("parent_id");
COMMENT ON COLUMN "auto_back_media_depts"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_depts"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_depts"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_depts"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_depts"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_depts"."name" IS '部门名称';
COMMENT ON COLUMN "auto_back_media_depts"."desc" IS '备注';
COMMENT ON COLUMN "auto_back_media_depts"."order" IS '排序';
COMMENT ON COLUMN "auto_back_media_depts"."parent_id" IS '父部门ID';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "auto_back_media_depts";"""


MODELS_STATE = (
    "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"
)
