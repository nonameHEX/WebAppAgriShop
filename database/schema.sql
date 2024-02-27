DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS employees;

DROP TABLE IF EXISTS machine_types;
DROP TABLE IF EXISTS machines;
DROP TABLE IF EXISTS cart_items;

DROP TABLE IF EXISTS order_state;
DROP TABLE IF EXISTS main_orders;
DROP TABLE IF EXISTS order_machine;

CREATE TABLE roles
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT,
    description TEXT
);

CREATE TABLE users
(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT UNIQUE NOT NULL,
    password        TEXT        NOT NULL,
    name            TEXT,
    last_name       TEXT,
    email           TEXT UNIQUE,
    phone_number    TEXT,
    salary_per_hour INTEGER,
    role_id         INTEGER,
    created_date    TEXT DEFAULT (DATETIME('now')),
    FOREIGN KEY (role_id) REFERENCES roles (id)
);

CREATE TABLE machine_types
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT,
    description TEXT
);

CREATE TABLE machines
(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT,
    price_per_day INT,
    type          INTEGER,
    description   TEXT,
    image         BLOB,
    FOREIGN KEY (type) REFERENCES machine_types (id)
);

CREATE TABLE cart_items
(
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id          INTEGER,
    user_id          INTEGER,
    date_to_delivery TEXT,
    date_to_pickup   TEXT,
    with_service     BOOLEAN,
    created_date     TIMESTAMP DATETIME DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))
);

CREATE TABLE order_state
(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE main_orders
(
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    date_to_delivery TEXT,
    date_to_pickup   TEXT,
    address          TEXT,
    state            INTEGER,
    creator          INTEGER,
    given_employee   INTEGER,
    FOREIGN KEY (state) REFERENCES order_state (id),
    FOREIGN KEY (creator) REFERENCES users (id),
    FOREIGN KEY (given_employee) REFERENCES users (id)
);

CREATE TABLE order_machine
(
    order_id     INTEGER,
    machine_id   INTEGER,
    with_service BOOLEAN,
    FOREIGN KEY (order_id) REFERENCES main_orders (id),
    FOREIGN KEY (machine_id) REFERENCES machines (id)
);

-- SEED DATA
INSERT INTO roles(name, description)
VALUES ('Správce', 'Může přidat/odebrat stroje, přidat/odebrat zaměstnance + funkce ostatních rolí'),
       ('Dispečer', 'Přijímá a přiděluje zakázky'),
       ('Technik', 'Ovládá přidělené stroje na zakázkách'),
       ('Uživatel', 'Nemá žádné administrativní funkce');

INSERT INTO users(username, password, name, last_name, email, phone_number, salary_per_hour, role_id)
VALUES ('PPP1', 'af388d3bf5e1a252da1ad453ec3d6dbf7106499b8a1e5e8a98d6bdbff19b0458', 'Prtest1', 'PT1', 'test1@prtesting.com', '000000000', 1500, 1),
       ('PPP2', '35330ae647edee57fea3b04da7665d29d931029564c9067ff9f5556aafa3dc00', 'Prtest2', 'PT2', 'test2@prtesting.com', '000000001', 700, 2),
       ('PPP3', 'ebc6833c9bc2c07b7f7e9d3882faf3c986214d9af991b21fefc07539482884d4', 'Prtest3', 'PT3', 'test3@prtesting.com', '000000002', 500, 3),
       ('PPP4', '24c10ea1b4ca632d2b24f83751cd7392a2ebbe7759999631132162056813f393', 'Prtest4', 'PT4', 'test4@prtesting.com', '000000003', 400, 3),
       ('TTT1', 'af388d3bf5e1a252da1ad453ec3d6dbf7106499b8a1e5e8a98d6bdbff19b0458', 'Test1', 'T1', 'test1@testing.com', null, null, 4),
       ('TTT2', '35330ae647edee57fea3b04da7665d29d931029564c9067ff9f5556aafa3dc00', 'Test1', 'T2', 'test2@testing.com', null, null, 4),
       ('TTT3', 'ebc6833c9bc2c07b7f7e9d3882faf3c986214d9af991b21fefc07539482884d4', 'Test1', 'T3', 'test3@testing.com', null, null, 4);

INSERT INTO machine_types(name, description)
VALUES ('Kombajn', 'Sbírá a separuje zrno z plodin během sklizně.'),
       ('Pluh', 'Používá se k obracení a přípravě půdy pro setí.'),
       ('Lisy', 'Stlačuje materiál do kompaktních bloků nebo balíků.'),
       ('Sekačky', 'Slouží k sekání a úpravě trávy nebo rostlin.');

INSERT INTO machines(name, price_per_day, type, description)
VALUES ('Komtest1', 3000, 1, 'Kompaktní a velmi snadno ovladatelný Komtest1 je vhodný pro sklízení různých druhů obilovin. Velice vhodné pro menší zemědělské podniky a farmy.'),
       ('Komtest2', 3000, 1, 'Kompaktní a velmi snadno ovladatelný Komtest2 je vhodný pro sklízení různých druhů obilovin. Velice vhodné pro menší zemědělské podniky a farmy.'),
       ('Pluhtest1', 4000, 2, 'Mimořádně účinný Pluhtest1 výborně zaorává rostlinné zbytky a plevele. V porovnání s konvenčním zpracováním půdy šetří zemědělec čas a energii.'),
       ('Pluhtest2', 4000, 2, 'Mimořádně účinný Pluhtest2 výborně zaorává rostlinné zbytky a plevele. V porovnání s konvenčním zpracováním půdy šetří zemědělec čas a energii.'),
       ('Listest1', 2000, 3, 'Listest1 je vybaven přítlačnými válci a je určen pro intenzivní profesionální použití po dlouhé pracovní dny s požadovanou vysokou účinností.'),
       ('Listest2', 2000, 3, 'Listest1 je vybaven přítlačnými válci a je určen pro intenzivní profesionální použití po dlouhé pracovní dny s požadovanou vysokou účinností.'),
       ('Sektest1', 5000, 4, 'Robustnost a promyšlené konstrukční řešení Sektest1 zajišťují vysokou provozní spolehlivost a životnost i v nejnáročnějších terénních podmínkách.');

INSERT INTO order_state(name)
VALUES ('Nevyřízeno'),
       ('Přijato'),
       ('Zamítnuto');

INSERT INTO main_orders(date_to_delivery, date_to_pickup, address, state, creator, given_employee)
VALUES ('2023-03-02', '2023-03-05', 'Testová 14, 642 66 Testo', 1, 5, 3),
       ('2023-03-03', '2023-03-05', 'Testová 15, 652 66 Testo', 2, 6, 4),
       ('2023-03-02', '2023-03-03', 'Testová 16, 662 66 Testo', 3, 7, null),
       ('2023-03-06', '2023-03-08', 'Testová 17, 672 66 Testo', 2, 5, 3),
       ('2024-01-26', '2024-01-27', 'Testová 18, 666 66 Testo', 1, 5, null);

INSERT INTO order_machine(order_id, machine_id, with_service)
VALUES (1, 1, true),
       (2, 3, true),
       (3, 5, false),
       (4, 4, true),
       (5, 1, false),
       (5, 2, true),
       (5, 3, false);