CREATE TABLE IF NOT EXISTS public.user (
    city VARCHAR(20),
    created TIMESTAMP,
    id serial PRIMARY KEY,
    name VARCHAR(20),
    s_number BIGINT,
    user_id VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.photo (
    created TIMESTAMP,
    id serial PRIMARY KEY,
    photo_id VARCHAR(20),
    url TEXT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES public.user(id)
);

CREATE TABLE IF NOT EXISTS public.log (
    created TIMESTAMP,
    id serial PRIMARY KEY,
    text TEXT
);