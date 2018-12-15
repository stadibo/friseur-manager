## Experiences

### Planning

The plan that I initially set out to fulfil was a bit too ambitious for the timeframe of this course, and was forced to limit the application to only handle reservations and appointment management. It would have been nice to have some statistics about services and rates for friseurs, and I is possible to expand the application in the future. The functionality that exists is fairly robust in its logic and easy enough to use.

### Implementation

- I was aiming to have a sort of continuous deployment, where Heroku always deploys the last commit pushed to github. I tried to only push working features to github, but the differences in the execution environments of the local machine and Heroku often caused issues.

- A recurring issue during the development of this application was accommodating the different ways Sqlite3 and PostgreSQL handle dates. I had handled dates in a previous project but now when I wanted to use the database's built in functions to operate on the dates it got a more involved. This is a part of the project I should have planned better: how should dates be stored and handled. 

- The reservation interface was a bit tricky to get right using the Flask templates, but it was quite a simple solution I ended up with. I think it isn't necessearily optimal to pass along variables like 'id' in the url, when showing the 'id' of other users to non logged in users is not needed for the functionality. A dynamically loaded interface could have been better.

### Issues

- The original plan had to be limited in order to finish the project on time. There was also some useful functionality like search and filtering of data that was left out beacause of time constraints.

- When counting upcoming appointments only appointments on dates in the future are considered. It should also consider the appointments left for the current date based on the time. I created a query (now removed) that would do this, but only locally, since PostgreSQL needs the timezone for time data to compare against the current time. This could have been done by manually assigning a timezone for the time data in the query.

### What I've learned

- To comfortably use python (no previous experince of the language)
- Using Flask and accompanying libraries to create a web app
- Got more familiar with Bootstrap 
- Reading the docs and error messages when things broke
- Suspect everything when debugging. A simple typo could ruin everything.