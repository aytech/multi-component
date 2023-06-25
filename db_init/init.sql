CREATE TABLE IF NOT EXISTS public.user (
    age INTEGER,
    bio TEXT,
    birth_date VARCHAR(100),
    city VARCHAR(100),
    created TIMESTAMP,
    distance INTEGER,
    id serial PRIMARY KEY,
    liked BOOLEAN DEFAULT FALSE,
    name VARCHAR(100),
    s_number BIGINT,
    scheduled BOOLEAN DEFAULT FALSE,
    user_id VARCHAR(100) NOT NULL,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS public.scheduled_like (
    id serial PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES public.user(id)
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
    context VARCHAR(20),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id serial PRIMARY KEY,
    level VARCHAR(10),
    text TEXT
);