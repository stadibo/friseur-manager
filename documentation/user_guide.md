# Friseur manager 

The application can be used locally at http://localhost:5000, or on a web hosting service of ones choosing. At the moment the application is running at https://friseur-app.herokuapp.com/

## Logging in

The application has additional features when a user is logged in. Currentl test user accounts for the application running on https://friseur-app.herokuapp.com/ are:

|     USERNAME     |  PASSWORD  | ROLE          |
| ---------------- | ---------- | ------------- |
| admin            | password   | ADMIN         |

It is possible to create FRISEUR users with the admin credentials, and customer user accounts can be created by following the register link. To log in follow the __Log in__-link in the top right corner.

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

5. If all goes well a page Saying reservation successful is displayed. It will also display the reservation number, which should be written down if user does not have an account. This number can be found from account appointments page when logged in __(TODO)__. Pressing __Back to front page__ directs user to front page...

## System administrator (admin) tools

### Accounts - lists all existing user accounts

Clicking the link in the navbar will display a view showing all existing user account with corresponding data. For more actions press the __Info__-button on the row of the user.

A page showing a card with user information and two buttons is show. If the user displayed is a friseur their appointments are also shown underneath.

- Pressing the __Change password__-button will bring up a page for doing just that for the user displayed. Admin can directly create new password without knowing the current password __(TODO)__. Press __Confirm__ when input is according to requirements of the fields.

- Pressing delete will permanently delete that user. Admins cannot delete themselves.

### Appointments - listing all appointments in the system

Clicking the link in the navbar will display a view showing all appointments with corresponding data. Statistics show above the table. 

The button __Set as fulfilled__ will mark the appointment as such, which would mean that the service has been provided and the transaction completed.

The button __Delete__ will permanently delete the record of the appointment.

### New friseur - add new friseur

Clicking the link in the navbar will display a view for creating an account for a new friseur. It is the same as registering a new user, but the type and priviledges of the account are different.

### Work days - show work days in the system

Clicking the link in the navbar will display a view showing all the work days in the system. These are used for tracking work of friseurs and assigning the date for the reservation.

A new work day can be added by typing a date in the format of the field or by chosing a date using the datepicker, which can be accessed by clicking the right side of the input field.

Pressing __Delete__ on a work day will permanently delete it from the system as well as all the appointments for that day.

## Logging out

Click the __Logout__-link in the top right corner in any view.