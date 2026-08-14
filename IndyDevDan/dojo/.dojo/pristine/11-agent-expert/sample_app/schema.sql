-- sample_app/schema.sql — the schema, applied by db.connect(). DO NOT EDIT.
CREATE TABLE IF NOT EXISTS tasks (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done  INTEGER NOT NULL DEFAULT 0
);
