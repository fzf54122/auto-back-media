from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "auto_back_media_file" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "file_id" VARCHAR(255) NOT NULL UNIQUE,
    "original_filename" VARCHAR(255) NOT NULL,
    "file_type" VARCHAR(50) NOT NULL,
    "file_size" BIGINT,
    "upload_user_id" INT NOT NULL,
    "file_path" VARCHAR(500)
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_15429e" ON "auto_back_media_file" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_b5e6db" ON "auto_back_media_file" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_a51087" ON "auto_back_media_file" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_c9623d" ON "auto_back_media_file" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_ca7016" ON "auto_back_media_file" ("is_deleted");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_file_id_eb079e" ON "auto_back_media_file" ("file_id");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_upload__b7373d" ON "auto_back_media_file" ("upload_user_id");
COMMENT ON COLUMN "auto_back_media_file"."description" IS '描述';
COMMENT ON COLUMN "auto_back_media_file"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_file"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_file"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_file"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_file"."file_id" IS '文件ID';
COMMENT ON COLUMN "auto_back_media_file"."original_filename" IS '原始文件名';
COMMENT ON COLUMN "auto_back_media_file"."file_type" IS '文件类型';
COMMENT ON COLUMN "auto_back_media_file"."file_size" IS '文件大小(字节)';
COMMENT ON COLUMN "auto_back_media_file"."upload_user_id" IS '上传用户ID';
COMMENT ON COLUMN "auto_back_media_file"."file_path" IS '本地文件路径';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "auto_back_media_file";"""


MODELS_STATE = (
    "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"
    "cJaweK9Km7DfuqDV+xFegFrvpeXr7+H3oCPj0="
)
