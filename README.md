# member_email

## Overall Purpose:
This code is used to track the members of an organization in a database, including changes to the membership over time.  Only a list of members at a given time is available from the organization headquarters (with recent terminations in past month or two only), so this is the only way to track and analyze membership changes over time.  It also sends welcome emails to new members and termination emails to terminated members.

## Useful code aspects
<ul>
   <li>Connect to and update a SQLite database (merge is not a command in SQLite, so use INSERT OR REPLACE)</li>
   <li>Send automated emails to multiple people based on criteria using GoDaddy email</li>
   <li>Track sent emails in database</li>
</ul>
