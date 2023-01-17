# member_email

## Overall Purpose:
This code is used to track the members of an organization in a database, including changes to the membership over time, based on monthly membership files as of a point in time. It also sends welcome emails to new members and termination emails to terminated members.

## Useful Code Aspects:
<ul>
   <li>Connect to and update a SQLite database (MERGE is not a command in SQLite, so used INSERT OR REPLACE)</li>
   <li>Send automated emails to multiple people based on criteria using GoDaddy email</li>
   <li>Track sent emails in database so only send each type once to each person</li>
   <li>User credentials that are not stored in the code itself, but instead are in a separate file/ library that is not part of the local Git repository and thus not pushed to GitHub</li>
</ul>

## Personal Note:
I created this during an object-oriented time of my life.  If I was to create this again, I probably would just put functions in a module and skip making it into a class.
