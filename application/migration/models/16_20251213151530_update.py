from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_deptclosure_ancesto_b09b41";
        DROP INDEX IF EXISTS "idx_deptclosure_descend_3e42d7";
        ALTER TABLE "deptclosure" ADD "descendant_id" BIGINT NOT NULL;
        ALTER TABLE "deptclosure" ADD "ancestor_id" BIGINT NOT NULL;
        ALTER TABLE "deptclosure" DROP COLUMN "descendant";
        ALTER TABLE "deptclosure" DROP COLUMN "ancestor";
        ALTER TABLE "deptclosure" ADD CONSTRAINT "fk_deptclos_auto_bac_dacfd77b" FOREIGN KEY ("descendant_id") REFERENCES "auto_back_media_depts" ("id") ON DELETE CASCADE;
        ALTER TABLE "deptclosure" ADD CONSTRAINT "fk_deptclos_auto_bac_361f756d" FOREIGN KEY ("ancestor_id") REFERENCES "auto_back_media_depts" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "deptclosure" DROP CONSTRAINT IF EXISTS "fk_deptclos_auto_bac_361f756d";
        ALTER TABLE "deptclosure" DROP CONSTRAINT IF EXISTS "fk_deptclos_auto_bac_dacfd77b";
        ALTER TABLE "deptclosure" ADD "descendant" INT NOT NULL;
        ALTER TABLE "deptclosure" ADD "ancestor" INT NOT NULL;
        ALTER TABLE "deptclosure" DROP COLUMN "descendant_id";
        ALTER TABLE "deptclosure" DROP COLUMN "ancestor_id";
        COMMENT ON COLUMN "deptclosure"."descendant" IS '子代';
COMMENT ON COLUMN "deptclosure"."ancestor" IS '父代';
        CREATE INDEX IF NOT EXISTS "idx_deptclosure_descend_3e42d7" ON "deptclosure" ("descendant_id");
        CREATE INDEX IF NOT EXISTS "idx_deptclosure_ancesto_b09b41" ON "deptclosure" ("ancestor_id");"""


MODELS_STATE = (
    "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"
    "=="
)
