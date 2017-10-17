DROP TABLE IF EXISTS "ticket";
DROP TYPE IF EXISTS ticket_status;
CREATE TYPE ticket_status AS ENUM (
    'open',
    'answer_ready',
    'answer_wait',
    'close'
);
CREATE TABLE "ticket" (
  "id" SERIAL PRIMARY KEY,
  "date_create" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "date_change" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "subject" varchar NOT NULL,
  "text" text NOT NULL,
  "email" varchar NOT NULL,
  "status" ticket_status DEFAULT 'open'
);

DROP TABLE IF EXISTS "comment";
CREATE TABLE "comment" (
  "id" SERIAL PRIMARY KEY,
  "ticket_id" int NOT NULL ,
  "date_create" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "text" text NOT NULL,
  "email" varchar NOT NULL
);
