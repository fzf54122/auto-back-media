from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "deptclosure" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(300) NOT NULL DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "ancestor" INT NOT NULL,
    "descendant" INT NOT NULL,
    "level" INT NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS "idx_deptclosure_uuid_a7dbae" ON "deptclosure" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_created_96f6ef" ON "deptclosure" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_updated_41fc08" ON "deptclosure" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_is_acti_6bb82c" ON "deptclosure" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_is_dele_84e3fc" ON "deptclosure" ("is_deleted");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_ancesto_fbc4ce" ON "deptclosure" ("ancestor");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_descend_2ae8b1" ON "deptclosure" ("descendant");
CREATE INDEX IF NOT EXISTS "idx_deptclosure_level_ae16b2" ON "deptclosure" ("level");
COMMENT ON COLUMN "deptclosure"."description" IS '描述';
COMMENT ON COLUMN "deptclosure"."created_at" IS '创建时间';
COMMENT ON COLUMN "deptclosure"."updated_at" IS '更新时间';
COMMENT ON COLUMN "deptclosure"."is_active" IS '是否启用';
COMMENT ON COLUMN "deptclosure"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "deptclosure"."ancestor" IS '父代';
COMMENT ON COLUMN "deptclosure"."descendant" IS '子代';
COMMENT ON COLUMN "deptclosure"."level" IS '深度';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "deptclosure";"""


MODELS_STATE = (
    "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"
    "kR62ERsA1hYUv48dw779H/Kjyv0="
)
