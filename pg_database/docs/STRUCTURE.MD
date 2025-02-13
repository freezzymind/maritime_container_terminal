# Maritime terminal database structure

## Schemas
- `public`: - Default schema


## Indexes
- **berths**:
  - `idx_berths_ship_imo`: index for searching a berth by `ship_imo` field.
  - `idx_berths_conditions`: composite index for filtering available berths, 
  considering the fields `status`, `max_draft` and `max_length`. 

- **ships**:
  - `idx_ships_imo`: unique index for searching by `imo` field.
  - `idx_ships_location`: index for searching ships at the roadstead, by the "location" field.


## Relationships between tables
- **port_calls → ships**:
  - The `imo` field in `port_calls` is a foreign key related to the `imo` field in `ships`.
- **port_departs → ships**:
  - The `imo` field in `port_departs` is a foreign key related to the `imo` field in `ships`.
- **berths → ships**:
  - The `ship_imo` field in `berths` is a foreign key related to the `imo` field in `ships`.


## Users and Privileges
### postgres
- **Role:** Superuser.
- **Privileges:** Full control over the database cluster.
- **Password:** Set during initialization.

### term_user
- **Role:** Standard user with restricted privileges.
- **Privileges:**
  - Can perform `SELECT`, `INSERT`, `UPDATE` on tables in the `public` schema.
  - Can connect to the `maritime_terminal` database.
- **Password:** Set during initialization. Managed securely in environment variables or secrets.


## Tables

### `ships`
Stores information about ships.

| Column          | Type              | Constraints                                        | Description                       |
|-----------------|-------------------|----------------------------------------------------|-----------------------------------|
| `id`            | `SERIAL`          | `PRIMARY KEY`                                      | Unique identifier.                |
| `name`          | `VARCHAR(100)`    | `NOT NULL`                                         | Ship name.                        |
| `imo`           | `CHAR(7)`         | `NOT NULL`, `UNIQUE`, `CHECK (imo ~ '^\d{7}$')`    | Ship IMO number (7-digit format). |
| `flag`          | `VARCHAR(50)`     | `NOT NULL`                                         | Ship's country of registration.   |
| `gross_tonnage` | `INTEGER`         | `NOT NULL`, `CHECK (gross_tonnage > 1000 AND       |                                   |
|                 |                   | gross_tonnage < 999999)`                           | Ship's weight (in GT).            |
| `length`        | `NUMERIC(10,2)`   | `NOT NULL`                                         | Ship length in meters.            |
| `width`         | `NUMERIC(10,2)`   | `NOT NULL`                                         | Ship width in meters.             |
| `draft`         | `NUMERIC(10,2)`   | `NOT NULL`                                         | Maximum draft in meters.          |
| `location`      | `VARCHAR(100)`    | `NOT NULL`,                                        |                                   |
|                 |                   | `CHECK (location IN                                |                                   |
|                 |                   | ('arrived', 'departed', 'anchored', 'docked'))`    | Current location of the ship.     |

---

### `berths`
Stores information about berths in the port.

| Column      | Type             | Constraints                                       | Description                        |
|-------------|------------------|---------------------------------------------------|------------------------------------|
| `id`        | `SERIAL`         | `PRIMARY KEY`                                     | Unique berth ID.                   |
| `status`    | `VARCHAR(10)`    | `NOT NULL`,                                       |                                    |
|             |                  | `CHECK (status IN ('free', 'busy', 'reserved'))`  | Berth availability status.         |
| `max_draft` | `NUMERIC(10,2)`  | `NOT NULL`                                        | Maximum draft allowed.             |
| `max_length`| `NUMERIC(10,2)`  | `NOT NULL`                                        | Maximum ship length allowed.       |
| `ship_name` | `VARCHAR(100)`   |                                                   | Name of the ship currently docked. |
| `ship_imo`  | `CHAR(7)`        | `REFERENCES ships(imo)`,                          |                                    |
|             |                  | `CHECK (ship_imo ~ '^\d{7}$')`                    | IMO number of the docked ship.     |

---

### `port_calls`
Stores information about ship arrivals at the port.

| Column         | Type        | Constraints                           | Description                         |
|----------------|-------------|---------------------------------------|-------------------------------------|
| `id`           | `SERIAL`    | `PRIMARY KEY`                         | Unique identifier.                  |
| `imo`          | `CHAR(7)`   | `NOT NULL`, `REFERENCES ships(imo)`,  |                                     | 
|                |             | `CHECK (imo ~ '^\d{7}$')`             | Ship IMO number.                    |
| `arrival_time` | `TIMESTAMP` | `NOT NULL`                            | Time of arrival at port.            |

---

### `port_departs`
Stores information about ship departures from the port.

| Column           | Type        | Constraints                           | Description                         |
|------------------|-------------|---------------------------------------|-------------------------------------|
| `id`             | `SERIAL`    | `PRIMARY KEY`                         | Unique identifier.                  |
| `imo`            | `CHAR(7)`   | `NOT NULL`, `REFERENCES ships(imo)`,  |                                     |
|                  |             | `CHECK (imo ~ '^\d{7}$')`             | Ship IMO number.                    |
| `departure_time` | `TIMESTAMP` | `NOT NULL`                            | Time of departure.                  |

## Data Standards

### **IMO Number (`imo`)**
- **Format:** Exactly **7 digits** (`^\d{7}$`).
- **Example:** `1234567`.
- **Description:** Unique identifier for a ship, assigned by the International Maritime Organization (IMO).
- **Validation:** Ensured by `CHECK (imo ~ '^\d{7}$')` constraint.

---

### **Ship Location (`location` in `ships`)**
- **Allowed Values:**  
  - `'arrived'` – The ship has entered the port.  
  - `'departed'` – The ship has left the port.  
  - `'anchored'` – The ship is at the anchorage, waiting.  
  - `'docked'` – The ship is moored at a berth.  
- **Description:** Represents the ship’s current status in the port or surrounding area.

---

### **Berth Status (`status` in `berths`)**
- **Allowed Values:**  
  - `'free'` – The berth is available for docking.  
  - `'busy'` – The berth is occupied by a ship.  
  - `'reserved'` – The berth is booked for an upcoming arrival.  
- **Description:** Indicates the availability of the berth.

