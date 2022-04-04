# member_email

## Overall Purpose:
This code is used to track the members of an organization in a database, including changes to the membership over time, based on monthly membership files as of a point in time. It also sends welcome emails to new members and termination emails to terminated members.

I created this for a small non-profit I volunteer for, so it is not proprietary.  Feel free to use for your own purposes.

## Useful code aspects
<ul>
   <li>Connect to and update a SQLite database (merge is not a command in SQLite, so use INSERT OR REPLACE)</li>
   <li>Send automated emails to multiple people based on criteria using GoDaddy email</li>
   <li>Track sent emails in database</li>
   <li>User credentials that are not stored in the code itself, but instead are in a separate file/ library that is not part of the local Git repository and thus not pushed to GitHub
</ul>
