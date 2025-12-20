from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "path" DROP NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "is_hidden" DROP NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "component" DROP NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "parent_id" DROP NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "order" DROP NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "keepalive" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "path" SET NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "is_hidden" SET NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "component" SET NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "parent_id" SET NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "order" SET NOT NULL;
        ALTER TABLE "auto_back_media_menu" ALTER COLUMN "keepalive" SET NOT NULL;"""


MODELS_STATE = (
    "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"
)
