from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "status" DROP DEFAULT;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "status" DROP NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "username" DROP DEFAULT;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "username" DROP NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "path" DROP DEFAULT;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "path" DROP NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "module" DROP DEFAULT;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "module" DROP NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "response_time" DROP DEFAULT;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "response_time" DROP NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "summary" DROP DEFAULT;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "summary" DROP NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "method" DROP DEFAULT;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "method" DROP NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "user_id" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "status" SET NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "status" SET DEFAULT -1;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "username" SET NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "username" SET DEFAULT '';
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "path" SET NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "path" SET DEFAULT '';
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "module" SET NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "module" SET DEFAULT '';
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "response_time" SET NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "response_time" SET DEFAULT 0;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "summary" SET NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "summary" SET DEFAULT '';
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "method" SET NOT NULL;
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "method" SET DEFAULT '';
        ALTER TABLE "auto_back_media_audit_log" ALTER COLUMN "user_id" SET NOT NULL;"""


MODELS_STATE = (
    "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"
)
