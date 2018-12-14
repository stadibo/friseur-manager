# SQL create table statements

```sql
CREATE TABLE role (
        id INTEGER NOT NULL,
        name VARCHAR(8) NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE work_day (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        date DATETIME NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (date)
);
CREATE TABLE account (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        username VARCHAR(144) NOT NULL,
        password BLOB NOT NULL,
        role_id INTEGER,
        PRIMARY KEY (id),
        UNIQUE (username),
        FOREIGN KEY(role_id) REFERENCES role (id)
);
CREATE TABLE appointment (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        time_reserved TIME NOT NULL,
        duration INTEGER NOT NULL,
        customer VARCHAR(144) NOT NULL,
        friseur VARCHAR(144) NOT NULL,
        reservation_number VARCHAR(8) NOT NULL,
        fulfilled BOOLEAN NOT NULL,
        work_day_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        CHECK (fulfilled IN (0, 1)),
        FOREIGN KEY(work_day_id) REFERENCES work_day (id)
);
CREATE TABLE friseur_work_day (
        account_id INTEGER NOT NULL,
        work_day_id INTEGER NOT NULL,
        start INTEGER,
        finish INTEGER,
        PRIMARY KEY (account_id, work_day_id),
        FOREIGN KEY(account_id) REFERENCES account (id),
        FOREIGN KEY(work_day_id) REFERENCES work_day (id)
);
CREATE TABLE account_appointment (
        account_id INTEGER NOT NULL,
        appointment_id INTEGER NOT NULL,
        PRIMARY KEY (account_id, appointment_id),
        FOREIGN KEY(account_id) REFERENCES account (id),
        FOREIGN KEY(appointment_id) REFERENCES appointment (id)
);
```
