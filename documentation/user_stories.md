### As a manager, I want be be able to:
- add a new hire to employee list so that I can keep track of their work. (COMPLETE)
- remove a friseur. (COMPLETE)
- view work hours of employees. (TODO)
- change employees’ work hours. (TODO)
- create work days. (COMPLETE)
- delete work days. (COMPLETE)
- update account passwords of existing accounts (Not implementing)
- remove users so that I can enforce our policy. (COMPLETE)
- view earnings for an interval of time so that I can analyse viability of business. (TODO)
- view earnings of friseurs. (TODO)
- show statistics about appointments, employees and customers. (WORK IN PROGRESS)

all appointments and data related to it paginated (offset and count added as parameters)
```sql
SELECT DISTINCT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, appointment.friseur, appointment.fulfilled, appointment.id, work_day.date 
FROM appointment
INNER JOIN work_day 
ON appointment.work_day_id = work_day.id 
LEFT JOIN account_appointment 
ON account_appointment.appointment_id = appointment.id 
LEFT JOIN account 
ON account.role_id = 2 
AND account.id = account_appointment.account_id 
ORDER BY work_day.date DESC, appointment.time_reserved ASC 
LIMIT offset, count;
```

add new friseur (role_id = 2 for friseur)
```sql
INSERT INTO account (name, username, password, role_id) VALUES ('name', 'username', passwordHash, role_id);
```

create work day 
```sql
INSERT INTO work_day (date) VALUES ('datetime');
```

delete user from database (id added as a parameter)
```sql
DELETE FROM account WHERE account.id = id;
```

delete work day from database (id added as a parameter)
```sql
DELETE FROM work_day WHERE work_day.id = id;
```

**Statistics**
```sql
average amount of appointments for a work day (id added as a parameter)
SELECT AVG(appointments) 
FROM (
  SELECT COUNT(appointment.id) AS appointments, account.id 
  FROM account 
  LEFT JOIN account_appointment 
  ON account.id = account_appointment.account_id 
  LEFT JOIN appointment 
  ON account_appointment.appointment_id = appointment.id 
  AND appointment.work_day_id = :id 
  WHERE account.role_id = 2 
  GROUP BY account.id
) AS appointment_per_account_for_day;
```

upcoming work_days that are not fully booked for friseur (user_id added as a parameter)
```sql
SELECT work_day.id, work_day.date 
FROM friseur_work_day 
LEFT JOIN work_day 
ON friseur_work_day.work_day_id = work_day.id 
WHERE friseur_work_day.account_id = :user_id
AND CURRENT_TIMESTAMP < work_day.date 
AND (
  SELECT COUNT(*) 
  FROM account_appointment, appointment 
  WHERE account_appointment.account_id = :user_id
  AND account_appointment.appointment_id = appointment.id 
  AND appointment.work_day_id = friseur_work_day.work_day_id
) < 8 
ORDER BY work_day.date ASC;
```

how many upcoming appointments for user 
```sql
SELECT COUNT(DISTINCT appointment.id) 
FROM appointment 
INNER JOIN account_appointment 
ON appointment.id = account_appointment.appointment_id 
INNER JOIN account 
ON account_appointment.account_id = :user 
INNER JOIN work_day 
ON appointment.work_day_id = work_day.id 
WHERE CURRENT_TIMESTAMP < work_day.date;
```

### As a user I want to be able to:
- reserve an appointment so that I can get a haircut. (COMPLETE)
- change my reservation so that it fits my schedule better. (COMPLETE)
- cancel my appointment so that a friseur does not expect me in vain. (COMPLETE)
- choose who will cut my hair so that I am comfortable with their decisions. (COMPLETE)
- sign up for loyalty account so that I get a discount for supporting the business in question. (COMPLETE)
- update the information of my account. (COMPLETE)
- delete my account when I no longer want my information used by this business. (WORK IN PROGRESS: Not yet GDPR compliant, send email to management or call salon to delete account)

create appointment
```sql
INSERT INTO appointment (time_reserved, duration, customer, friseur, reservation_number, fulfilled, work_day_id) VALUES ('time', 1, 'customer name', 'friseur name', '12345678', work_day_id);
```

delete appointment
```sql
DELETE FROM appointment WHERE appointment.id = id;
```

create a loyalty account (role_id = 1 for user)
```sql
INSERT INTO account (name, username, password, role_id) VALUES ('name', 'username', passwordHash, role_id);
```

update the password of my account (id for user added as a parameter)
```sql
UPDATE account SET passwordHash = newPasswordHash WHERE account.id = id;
```


### As a friseur I want to be able to:
- change my working hours so that I can adjust for changes in life. (TODO)
- cancel appointments with me so that I can adjust for emergencies. (COMPLETE)
- create an appointment so that appointments of customers’ who call by phone can be added to the system. (COMPLETE)
- view a summary of my earnings for a set time period. (TODO)
- view my appointments. (COMPLETE)

view my appointments (id for friseur added as a parameter)
```sql
SELECT DISTINCT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, account.name, appointment.fulfilled, appointment.id, work_day.date 
FROM appointment 
INNER JOIN work_day 
ON appointment.work_day_id = work_day.id 
INNER JOIN account_appointment 
ON account_appointment.appointment_id = appointment.id 
INNER JOIN account 
ON account.id = :user_id
WHERE account.role_id = 2 
AND account_appointment.account_id = :user_id
ORDER BY work_day.date DESC, appointment.time_reserved ASC;
```