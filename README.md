# member_email

## Overall Purpose:
This code is used to track the members of an organization in a database, including changes to the membership over time, based on monthly membership files as of a point in time. It also sends welcome emails to new members and termination emails to terminated members.

I created this for a small non-profit I volunteer for, so it is not proprietary.  Feel free to use for your own purposes.

## Useful code aspects
<ul>
   <li>Connect to and update a SQLite database (merge is not a command in SQLite, so use INSERT OR REPLACE)</li>
   <li>Send automated emails to multiple people based on criteria using GoDaddy email</li>
   <li>Track sent emails in database</li>
   <li>Example of using user credentials in code with storing them in the code itself (it is stored in a separate secret file on my computer that is imported as a library and not pushed to GitHub)
</ul>
