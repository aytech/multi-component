CREATE TABLE IF NOT EXISTS public.user (
    city VARCHAR(100),
    created TIMESTAMP,
    id serial PRIMARY KEY,
    liked BOOLEAN DEFAULT FALSE,
    name VARCHAR(100),
    s_number BIGINT,
    user_id VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.photo (
    created TIMESTAMP,
    id serial PRIMARY KEY,
    photo_id VARCHAR(100),
    url TEXT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES public.user(id)
);

CREATE TABLE IF NOT EXISTS public.settings (
    created TIMESTAMP,
    id serial PRIMARY KEY,
    name VARCHAR(100),
    value VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS public.log (
    created TIMESTAMP,
    id serial PRIMARY KEY,
    text TEXT
);