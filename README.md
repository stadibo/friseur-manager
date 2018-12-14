# friseurManager
This is a project made for a database application project course at the University of Helsinki.

## Description
The goal is to crate a friseur salon management application that enables the manager(s) to keep track of friseurs and reservations for their services.

Services are presented on a website and it is possible to make reservations from the web. The assortment of services of the friseurs vary and, as such, every friseur is not offering all the services. Prices are based on the service. A customer can reserve an appointment via the web, where they will choose the service, date, time and friseur, as well as, special arrangements if needed. A customer can register to become a loyaty customer, through which they get a loyaty discount. Even if not registered the reservation is accepted, and the customer will recieve a reservation number by which they can cancel the appointment by calling the salon.

## Functionality

**Appointments (CRUD)**

- Reserve and appointment (even if not logged in)
- Keeping track of appointments
  - Set them  as fulfilled

**Work_day (CRD)**

- Create work days for friseurs
- Show statistics for a work day

**Account (CRUD)**

- Hiring a new friseur (admin only)
- Firing a friseur (admin only)
- List accounts (admin only)
- Making and canceling reservations
- Registering and logging in for customers
- Changing password (logged in user)
- Passwords are encrypted


## Not yet implemented functionality

- Defining a service
- Defining and changing the assortment services
- Work sheets for employees
- Summary for management
- Tracking and changing work hours of friseurs

## Test user credentials 

|	__USERNAME__ | __PASSWORD__  |   __ROLE__    | 
|--------------|---------------|---------------|
| admin        |   password    |    ADMIN      |

## Documentation and link to application
[Live application](https://friseur-app.herokuapp.com/)

[User stories](https://github.com/stadibo/friseurManager/blob/master/documentation/user_stories.md)

[Database diagram](https://github.com/stadibo/friseurManager/blob/master/documentation/database_diagram.png)

[Setup guide](https://github.com/stadibo/friseurManager/blob/master/documentation/installation_guide.md)

[User guide](https://github.com/stadibo/friseurManager/blob/master/documentation/user_guide.md)

[SQL-create-table](https://github.com/stadibo/friseurManager/blob/master/documentation/SQL_create_table_statements.md)


## Issues and improvements

- A couple of methods are still a bit long
- The routes leading to appointment data should also be able to traverse back the same direction, and not only lead to all appointments
- The handling of dates could probably be made more simple, instead of manually checking and modifying the date value if needed
- Make the authorization check take more than one role for making routes more reusable for users with different roles
- Add search and filtering by various criteria
