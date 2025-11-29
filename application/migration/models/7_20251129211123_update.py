from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "auto_back_media_settings" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "description" VARCHAR(500),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "key" VARCHAR(100) NOT NULL UNIQUE,
    "value" VARCHAR(100) NOT NULL UNIQUE,
    "is_public" BOOL NOT NULL DEFAULT True,
    "category" VARCHAR(50) NOT NULL DEFAULT 'general'
);
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_uuid_11c171" ON "auto_back_media_settings" ("uuid");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_created_042421" ON "auto_back_media_settings" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_updated_ba701b" ON "auto_back_media_settings" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_acti_8db8a7" ON "auto_back_media_settings" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_auto_back_m_is_dele_724521" ON "auto_back_media_settings" ("is_deleted");
COMMENT ON COLUMN "auto_back_media_settings"."description" IS '设置描述';
COMMENT ON COLUMN "auto_back_media_settings"."created_at" IS '创建时间';
COMMENT ON COLUMN "auto_back_media_settings"."updated_at" IS '更新时间';
COMMENT ON COLUMN "auto_back_media_settings"."is_active" IS '是否启用';
COMMENT ON COLUMN "auto_back_media_settings"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "auto_back_media_settings"."key" IS '设置键';
COMMENT ON COLUMN "auto_back_media_settings"."value" IS '设置值';
COMMENT ON COLUMN "auto_back_media_settings"."is_public" IS '是否公开设置';
COMMENT ON COLUMN "auto_back_media_settings"."category" IS '设置分类';
COMMENT ON TABLE "auto_back_media_settings" IS '系统设置表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "auto_back_media_settings";"""


MODELS_STATE = (
    "eJztXW1v2zgS/itBPrVAdiHrXYfDAW6b282hSRatc7vY7cKgJMrRRZa8emkbLPrfj6Ssd1"
    "GhbNmSa35xU5Kjl2cocuaZ0ejvy3VgQy/6cb5xb/Ffl/+4+PvSB2uI/mj0XV1cgs2m6MEN"
    "MTA9MhgkcbA0gfW0XEPbBUuwcYmAGcUhsGI0xAFeBFGTDSMrdDexG/hYcP7LzadEBeLsU6"
    "JouomF7MBCUq6/ovQnvvtXApdxsILxIwzRqD/+RM2ub8OvMMr+u3laOi707Mo9uTY+AGlf"
    "xs8b0vbGXd348b/JWHx2c2kFXrL2i/Gb5/gx8HMB149x6wr6MAQxxGeIwwTfm5943haR7H"
    "bTiy2GpFdZkrGhAxIPI4SlGwBljSVMtk1W4GNw0dVE5B5X+Cw/GKIoSZooSKquyJqm6IKO"
    "xpJLanZp39IbLgBJD0Vgufnp5m6BbzRAGky1jBu+ERkQg1SK4F0AnCRtED883LxrBzgbX4"
    "MYN/+IpepAZ7Duh/TlP53EtzDCF+RM+Ef+1+Xu4Hfg+Pbn+YdXkvqa3GUQxauQdBJMCJgF"
    "eOWTNzB8+wjCdgxrYjUo0WXuAmLWUKBYPMA5jE3ELtHDKlnOp0R3HKH+MFMm7hp8XXrQX8"
    "WP6L+SIHSA+d/5hxRPQXhdnZp32y4x7asCa4UQ3/oSxE1c36Ge2F3DdmyrkjVo7a3oj9kf"
    "wwDNtjAgpBVxZqJfNA6hrjjqp8RQHJkRdXRj9r3vPW9P2AH64ub2+uNifvsLPvI6iv7yCG"
    "7zxTXuEUnrc631lVrTT36Qi19vFj9f4P9e/H5/d11/LPJxi98v8TWRjcUPviyBXcIma83w"
    "q2g72dg7arsqOTFtq6ojYz2bwhlre3vxpR09WiL7wv0MWzb2IPAg8Ck7e1mupmkTCR5IuX"
    "lDQ7kiWjQVWVTJL/pbU0SdTbldm/j9/fuKHt/c1Lb0u4fbN9cfXs2IAtEgN67s9BWgkdUH"
    "MRq9kS4JHg9qisFZw1oU0eNkqCrjg3QcrDcA7YU9LIBs/PG2/vZFihjrOhqFgHV01rWpsv"
    "/PmPb/Wcf+P2vu/2vkKAQt8xYjeu0na4LqDboq4FuwgW4hPTa+CFzT0dAMtmSRbAUG/ttW"
    "dgFaZYC5vqwXIKt1iKNkvQbhc59ZWxKZFrCaqaNFQYZWwx1lAVZhmsFKxwxWmjM4BquoD7"
    "bZ+LGBTd135GliVDU46oqAWQHnqeS24gbMWXwBob1s9ARiQBvb7FqL61Z/OEQbIyZDWpR3"
    "C/znRYB/G8tPTWtbJuYDOlZOxQzvFO9HP3zLZmDWWpyCXP6yRitVbiaEHrG7szE5YEFI8H"
    "6Cz5ctJBMBN+UPctVkQzduetq0O34Mg2T1SD0Ihb5COkhNF/KwzT++nb8jJuyyzv2QubUG"
    "PliRJgzRt6v8Xm+hn1D5taLzqg/BtkZibAwbWtsk20I7sqQonVRb10DOuXHOjXNunHOj7L"
    "CcczsrFoZzbuekbc659dp8OOd2kpwb+beHBZCNH9vDrlrtiizYaB4buxkCIosdINLNALFh"
    "BYRwDcKnJq7/+Xh/145rIVFD9sFHd/yH7Vrx1YXnRvGfDDhvJ+ggMMuOjaFVFAPBbCqYLT"
    "JNRuqtA1aMRGUKZ3C+up3/Vkf67fv7N/X1HB/gTYPw9JMUuNYZzcJ5lg6w0xQfEvryDNcs"
    "zWx3YFlmeJf3leGuUee3Vp/ertXPbcjGTwpRRXVgStJNhrA/1QBIFdgJRkKC0IZhE1kqGZ"
    "OPf5mPGQpZodV+kAwRu126wwhlysyIM1mTdUmVc0Imb+laCdoiciH042Ub0ULFriIzMn6a"
    "KKnlyZmyPMfHERmmj65tw5ZV8yWDtpA7mD3bBJPJoDVUAxm0umIxTs7jGLRWsN4EPvRbPH"
    "L6QloRGn811aAl40ico05mBX2CcAO8/s5vRe6IM5jm/SITVkfT2JYY7ajjTNoQ2m4IrV5z"
    "tiwzumFlzCwbg2sAvDrMZqPO29Einth94CHPPiHPArGdY574EPsEPbOQ4kBRz+J2W6KeFS"
    "zYo574uokEQ9RT1WQJ782K8ELUkz6QRz151JNHPXnUk7LL8qjnWcXBeNTznLTNo569Nh8e"
    "9eRRz2N5aJhmN2wR/YqaOL2YJ77YvlbVJLiLMqj72VaD5cCPwWAMRV5UMntPnbyo3EydvK"
    "hxPlUGo05LNFK16QzHQRmMpjk3UJ5+uWLCqau9fC+tWqel6lfz7w+o8z6p+i0WfARDctwh"
    "FP+ADvbdaL5yM22qZ2ErCbztUwAfgpGtJEehUYEDsZXzxHbj98GKXgelMuCqVzEULLr0gh"
    "UTdUnXKKcjOR3J6UhOR1JMZk5HnhVBxenIc9I2pyN7bT6cjjxJOrLkLzAmWZYkjpdiSU1X"
    "Q1MXwSxK2lj5lRiOvpxuWWZsG6pAcF9eV5VZCpzI9AoncqOKTGAnXi9kC4mxcVVEA9umgm"
    "MXOS7KTvn+w+N6KqVj2pGtVOTZywOYiTpL2p+o09P+cB976SPKpB2h3BEDtHsVO5qxJVR2"
    "5FOe3hsqL2O63/spoqKwRM4UhR46w321tSAGcVvwhbr/FwLH2/5/mLVuXaKJ7CpVENDiqu"
    "kCa+bvwAYA8i826AxwmTlqjDg25EZ+YUWRSR41NOSy0/cqe7VKdmR7Hb0eC2N0c1G8BGFb"
    "Ua6uV1urchN7wbW8NCiSRRZdjXEnO/YLrvl0NQO7xXLo0kFNcGpKcGwZv5JpwxR+bFSojH"
    "XTjqGE4wXkO8M1H2EcIygiarimOuCqT7gm2ooyRWvwwm85Jn5Vyca2n2kixWmOin51XW0Q"
    "GQzDeZSHR3l4lGfYKM+w22TxzE4kS4qHfM4jCMBDPuekbR7y6bUT8ZDPSYZ8cDpYD2tgO3"
    "z0/POSEWAo4riFrctwfgZe0itGkQtMCVJFkKzJQIoe6k1iem5LUv9Li0EhN4GKD5W1YKbi"
    "SjCOIJSBn9K6YCFUVkG/sFBZ5ohEe3pQj8K3l2a1KKhpAbPdvAUmZ6HDVzjuCxWd/E2RXd"
    "zC3VRSj9l5GxzHZuZsSnFmGk/TMoRzM5yb4dwMz8ClLLE8A/esHHROx5yTtk+MjtnNL1Ad"
    "S5heVbip8zFNrKmGp+6oTpmKyb6OhfyE/UPtA2fijp9IujubMFwi6fAFAoDngl5fc8sFRg"
    "9+KYYtpYDuZmExGVgd9lUdSrgGrtcHylxg7AlqCAATA6a5U4nIgyTfbRAgvR74XGD0eakp"
    "Ei64bdo7zcvhH/ENiKIvQdgr8bYsMzqgimmpvfIYD5/KjDbzKNnAMON5+tkBFdEpWAJls0"
    "uGEsD5uDr+wAEE5GuZAOeRygIJkimTCo95ICKvs7stXEG3l1OVHMDLGXLKqxpmw9Hehtdl"
    "lXxlwiFfQuzp8ZyIh5MB03Box6i5M1QJjvMpGFyrXFKtw1EvrvFS/ZXSW3QHrcNRTLCOj6"
    "Wio3aGB2ojrvp9NrVXpIDX4uCRAB4J4JEAHgngkQAeCeCRgJOMBPDETJ6YuQPWmzD4H7Ti"
    "Zd8oQF1ufCoLapizlhxh71DAIVjX1CUh8PRAuSo1PsYAf59PdhRp3y90HhDjXWJaTclJYa"
    "3bZAGRnJ1qeRwQa0Jm96w7UZWbFM770eEHwfkMWFjZ0Zw8lHtmLGxZ1XHw1PbFTPqzlAuM"
    "/hAVcfhFdk2TeHpOotDIrP1brqXUhqLoCCOyA5TCmEgK+QJET7ekk8oU14dc9aeKY3QItk"
    "oAnCvmXDHnijlXzLlizhVzrphzxZwr5lwx54q7LQHOFXOumHPF58sVY+8a+cWbttoKHexW"
    "RWp0jGWIC/opIk7YxRnoaHnWDcat8AgYW2Hgx8CkFIR9yZuoynKuePJcMSH3d9F1RZArev"
    "KKPmEGu7xinjGD/Ss0qdR13nfVh7P+Ak32srWOguEHtpG+fZq97kArh/LCcE5yc5L7/Eju"
    "BfxKmaRTK1tr6JqB32uCO5St7do2r39bVHbMRmHxfNd8f3/3Uza8Xm2c09/nQohy+vuctH"
    "1i9HdzOeVFUybwqvSpFE3J6Oy+BG1d7lARcfadqkSD70fRDlO1sg3kJOxV+KMmNro9VkD8"
    "8OH9LsgOVut2It7wHIau9XjZ4gtve646PeFizGQStb4jB3bPb2fRXdPPMIx6pg+VRI6XOr"
    "Qnioen+fGj0QPE7fDTBPAgZb7RGWPot/gg9I+JlUQG+IzYCLB2oPh9fDHs2/8BL9914Q=="
)
