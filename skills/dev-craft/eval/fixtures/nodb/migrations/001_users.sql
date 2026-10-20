CREATE TABLE users (id bigserial PRIMARY KEY, email text NOT NULL UNIQUE, updated_at timestamptz NOT NULL DEFAULT now());
