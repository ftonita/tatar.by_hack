DROP TABLE IF EXISTS "users";
CREATE TABLE "public"."users" (
    "user_id" text NOT NULL,
    "nickname" text DEFAULT 'None' NOT NULL,
    "city" text DEFAULT 'None' NOT NULL,
    "level" real DEFAULT '0' NOT NULL,
    "person_id" integer DEFAULT '0' NOT NULL
) WITH (oids = false);

INSERT INTO "users" ("user_id", "nickname", "city", "level", "person_id") VALUES
('766274883',	'ftonita',	'KZN',	0,	0),
('1935966096',	'ftonita',	'KZN',	0,	0);

DROP TABLE IF EXISTS "tasks";
CREATE TABLE "public"."tasks" (
    "task_id" text NOT NULL,
    "task_info" text DEFAULT 'None' NOT NULL,
    "answers" text DEFAULT 'None' NOT NULL,
    "cost" int DEFAULT '0' NOT NULL,
    "k" real DEFAULT '0' NOT NULL
) WITH (oids = false);

DROP TABLE IF EXISTS "shop";
CREATE TABLE "public"."shop" (
    "item_id" text NOT NULL,
    "item_name" text DEFAULT 'None' NOT NULL,
    "item_info" text DEFAULT 'None' NOT NULL,
    "price" int DEFAULT '0' NOT NULL,
    "level" int DEFAULT '0' NOT NULL
) WITH (oids = false);

DROP TABLE IF EXISTS "person";
CREATE TABLE "public"."person" (
    "id" integer DEFAULT '0' NOT NULL,
    "name" integer DEFAULT '0' NOT NULL,
    "age" integer DEFAULT '0' NOT NULL,
    "sex" integer DEFAULT '0' NOT NULL,
    "status" int DEFAULT '0' NOT NULL
) WITH (oids = false);
