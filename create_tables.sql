-- Creating tables
CREATE TABLE ships (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
imo CHAR(7) NOT NULL UNIQUE CHECK (imo ~ '^\d{7}$'),
flag VARCHAR(50) NOT NULL,
gross_tonnage NUMERIC(10, 2) NOT NULL,
length NUMERIC(10, 2) NOT NULL,
width NUMERIC(10, 2) NOT NULL,
draft NUMERIC(10, 2) NOT NULL,
location VARCHAR(100));

CREATE TABLE port_calls (
id SERIAL PRIMARY KEY,
imo CHAR(7) NOT NULL REFERENCES ships(imo) CHECK (imo ~ '^\d{7}$'),
arrival_time TIMESTAMP NOT NULL);

CREATE TABLE port_departs (
id SERIAL PRIMARY KEY,
imo CHAR(7) NOT NULL REFERENCES ships(imo) CHECK (imo ~ '^\d{7}$'),
departure_time TIMESTAMP NOT NULL);

CREATE TABLE berths (
id SERIAL PRIMARY KEY,
status VARCHAR(10) NOT NULL CHECK (status IN ('free', 'busy', 'reserved')),
max_draft NUMERIC(10, 2) NOT NULL,
max_length NUMERIC(10, 2) NOT NULL,
ship_name VARCHAR(100),
ship_imo CHAR(7) REFERENCES ships(imo) CHECK (ship_imo ~ '^\d{7}$'));

-- Creating indexes for ships
CREATE UNIQUE INDEX idx_ships_imo ON ships(imo);                 -- Unique index for searching by `imo` field.
CREATE INDEX idx_ships_location ON ships(location);              -- Index for searching ships at the roadstead, by the "location" field.

-- Creating indexes for berths
CREATE INDEX idx_berths_ship_imo ON berths(ship_imo);                           -- Index for searching a berth by `ship_imo` field.
CREATE INDEX idx_berths_conditions ON berths(status, max_draft, max_length);    -- Composite index for filtering available berths.


                                                                 