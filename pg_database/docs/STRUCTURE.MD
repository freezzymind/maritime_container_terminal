# Sea terminal database structure

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
- **Password:** Set during initialization. Stored securely.

### term_user
- **Role:** Standard user with restricted privileges.
- **Privileges:**
  - Can perform `SELECT`, `INSERT`, `UPDATE` on tables in the `public` schema.
  - Can connect to the `sea_terminal` database.
- **Password:** Set during initialization. Managed securely in environment variables or secrets.






## Настройки базы
- **Encoding**: UTF8
- **Collation**: en_US.UTF-8
- **Ctype**: en_US.UTF-8
- **Tablespace**: pg_default

## Триггеры
- **auto_update_timestamp**:
  - Таблица: `port_calls`.
  - Описание: автоматически обновляет поле `updated_at` при изменении записи.

## Стандарты данных
- **IMO номер**:
  - Формат: 7 цифр (`^\d{7}$`).
  - Пример: `1234567`.


## tables

### port_calls
- 'id SERIAL PRIMARY KEY': - unigue identificator 
-
-