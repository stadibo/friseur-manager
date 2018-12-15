# Friseur manager 

The application can be used locally at http://localhost:5000, or on a web hosting service of ones choosing. At the moment the application is running at https://friseur-app.herokuapp.com/

## Logging in

The application has additional features when a user is logged in. Currently test user accounts for the application running on https://friseur-app.herokuapp.com/ are:

|     USERNAME     |  PASSWORD  | ROLE          |
| ---------------- | ---------- | ------------- |
| admin            | password   | ADMIN         |

It is possible to create FRISEUR users with the admin credentials, and customer user accounts can be created by following the register link. To log in follow the __Log in__-link in the top right corner. (The first user to register is assigned as admin)

It is possible to log out at any time using the __Logout__-link in the top right corner.

## Registering

Click the __Register__-link in top right corner.

Input the required information in the corresponding fields, taking into consideration restriction on the length of the input and uniqueness of the username. Fix the input if necessary when prompted with messages. The registered user is automatically logged in and redirected to the front page.

## Front page

When first logged in the user is directed to this page. The navigation bar is specific to the type of user that is logged in.

There is a short presentation of the business and simple instructions for reserving an appointment.

*The page can also be reached by clicking the brand text __DIMMA__ in the top left corner.*

## Making a reservation

To start the reservation of an appointment press the __Reserve an appointment__-button on the front page.

1. Choose the friseur who shall provide the service. Press the __Choose__-button on the row of the desired friseur to continue.

2. Chose the date from those available. If the dates do not work it is possible to go back using the browsers previous page navigation. Press the __Choose__-button on the row of the date to continue.

3. Chose the time from those available. If the times do not work it is possible to go back using the browsers previous page navigation. Press the __Choose__-button on the row of the time to continue.

*If logged in as customer the following step does not apply (Customer name will be assigned based on the name assossiated with the account).*

4. Enter the name by which the customer will be identified. Press the __Confirm__-button to continue.

5. If all goes well a page Saying reservation successful is displayed. It will also display the reservation number, which should be written down if user does not have an account. This number can be found from account page when logged in. Pressing __Back to front page__ directs user to front page...

## Customer tools

- When logged in clicking __Account__ in the navbar will show the account page of the current user

- Pressing the __Change password__-button will bring up a page for doing just that. Press __Confirm__ when fields have been filled according to requirements of the validation.

- On the account page the customer can view their upcoming appointments and cancel them by clicking __Cancel__ on the appointment that should be cancelled. This will remove the appointment and open up the time slot for the friseur.

## Friseur tools

- All of the above regarding customer

- The same kind of view exists for a logged in friseur but on their page all of their appointments are shown instead of just the upcoming appointments. Also their appointments have a __View__ button to display more info about appointment. Single appointment view is the same as for the _admin_ but the __Show all__ button leads back to the account page.

## System administrator (admin) tools

### Accounts - lists all existing user accounts

Clicking the link in the navbar will display a view showing all existing user level accounts with corresponding data. For more actions press the __View__-button on the row of the user.

- A page showing a card with user information and delete button is displayed. Their appointments are also shown underneath.

- Pressing delete will permanently delete that user.

### Friseurs - list all friseur accounts

Clicking the link in the navbar will display a view showing all existing user level accounts with corresponding data. For more actions press the __View__-button on the row of the user.

- A page showing a card with user information and delete button is displayed. Their appointments are also shown underneath.

Clicking the button above the table  will display a view for creating an account for a new friseur. It is the same as registering a new user, but the type and priviledges of the account are different.

### Appointments - listing all appointments in the system

Clicking the link in the navbar will display a view showing all appointments with corresponding data. Statistics show above the table. 

Clicking the button __View__ will show the full information of the appointment.

When in the single appointment view:

- The button __Set as fulfilled__ will mark the appointment as such, which would mean that the service has been provided and the transaction completed.

- The button __Delete__ will permanently delete the record of the appointment.

- __Show all__ button will direct the admin to the list showing all the appointments
 
### Work days - show work days in the system

Clicking the link in the navbar will display a view showing all the work days in the system. These are used for tracking work of friseurs and assigning the date for the reservation.

A new work day can be added by typing a date in the format of the field or by chosing a date using the datepicker, which can be accessed by clicking the right side of the input field.

Clicking __View__ on a work day will show the appointments for that work day and some statistics on how busy that day is for the friseurs.

Pressing __Delete__ on a work day will permanently delete it from the system as well as all the appointments for that day.

## Logging out

Click the __Logout__-link in the top right corner in any view.