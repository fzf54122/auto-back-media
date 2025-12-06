from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "auto_back_media_role_auto_back_media_menu";
        DROP TABLE IF EXISTS "auto_back_media_role_auto_back_media_api";
        ALTER TABLE "auto_back_media_role" ADD "users" JSONB NOT NULL;
        ALTER TABLE "auto_back_media_role" ADD "menus" JSONB NOT NULL;
        ALTER TABLE "auto_back_media_role" ADD "apis" JSONB NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "auto_back_media_role" DROP COLUMN "users";
        ALTER TABLE "auto_back_media_role" DROP COLUMN "menus";
        ALTER TABLE "auto_back_media_role" DROP COLUMN "apis";
        CREATE TABLE "auto_back_media_role_auto_back_media_api" (
    "apimodel_id" BIGINT NOT NULL REFERENCES "auto_back_media_api" ("id") ON DELETE CASCADE,
    "auto_back_media_role_id" BIGINT NOT NULL REFERENCES "auto_back_media_role" ("id") ON DELETE CASCADE
);
        CREATE TABLE "auto_back_media_role_auto_back_media_menu" (
    "menumodel_id" BIGINT NOT NULL REFERENCES "auto_back_media_menu" ("id") ON DELETE CASCADE,
    "auto_back_media_role_id" BIGINT NOT NULL REFERENCES "auto_back_media_role" ("id") ON DELETE CASCADE
);"""


MODELS_STATE = (
    "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"
    "0Gaw+KJ/iduJbl5ev/AVOw+GA="
)
