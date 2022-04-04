#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sends email to new and terminated ABC Organization members and updates 
member database.
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import pandas as pd
import sqlite3
from credentials import abc_membership_email as email_credentials


class ABC_Member_Email():
    ''' Sends email to all new members and a different email to members that
    terminated/ dropped off.  Members are tracked in a SQLite database, which is
    updated as part of the monthly process of emailing members. '''
    
    input_path = ('/Users/JohnDoe/Documents/python_code/abc_organization/' +
                  'member_email/input/')
    db_path = input_path + 'members.db'
    cnxn = sqlite3.connect(db_path)
    cur = cnxn.cursor()
    cnxn_port = 465
    server = smtplib.SMTP_SSL('smtpout.secureserver.net', cnxn_port)
    
    def __init__(self):
        self.server.connect('smtpout.secureserver.net', self.cnxn_port)
        self.server.ehlo()
        self.server.login(email_credentials.username, email_credentials.password)
    
    def send_abc_member_emails(self):
        self._update_members_db()
        self._email_new_members()
        self._email_terminated_members()
    
    def _update_members_db(self):
        current_members_path = self.input_path + 'current_month_members.xlsx'
        current_members = pd.read_excel(current_members_path)
        current_members.to_sql('stage_current_members', self.cnxn, 
                               if_exists='replace')
        
        # SQLite does not have merge command, can do insert and replace 
        # or upsert, with so many cols to update just use find and replace
        # to keep shorter and replace the 3 cols to maintain with existing data.
        # NOTE: If I was using a standard database like SQL Server instead of SQLite,
        # I would instead call a stored procedure.
        sql_find_or_replace = '''
        INSERT OR REPLACE INTO members(
            member_number
            ,first_name
            ,last_name
            ,designations
            ,membership_type
            ,join_date
            ,end_date
            ,terminated_date
            ,membership_years
            ,email
            ,phone
            ,organization
            ,job_title
            ,job_code
            ,industry
            ,address1
            ,address2
            ,city
            ,state
            ,email_opt_out_yes
            
            ,deleted_yes
            ,welcome_email_sent_yes
            ,terminated_email_sent_yes)
        SELECT 
            cm.[GAN]
            ,cm.[First Name]
            ,cm.[Last Name]
            ,cm.[Designations]
            ,cm.[Membership Type]
            ,cm.[Join Date]
            ,cm.[End Date]
            ,cm.[Terminate Date]
            ,cm.[Membership Years]
            ,cm.[Email]
            ,cm.[Phone]
            ,cm.[Organization]
            ,cm.[Job Title]
            ,cm.[Job Code]
            ,cm.[Industry]
            ,cm.[Address 1]
            ,cm.[Address 2]
            ,cm.[City]
            ,cm.[State]
            ,cm.[Email Opt Out]
            
            ,m.deleted_yes
            ,m.welcome_email_sent_yes
            ,m.terminated_email_sent_yes
        FROM stage_current_members cm
            LEFT JOIN members m;
        '''
        self.cur.execute(sql_find_or_replace)
        self.cnxn.commit()
        
        # Mark any deleted members (not in current month file).
        sql_mark_deleted = '''
        UPDATE members
            SET deleted_yes = 1
            WHERE member_number NOT IN
                (SELECT [GAN] AS member_number FROM stage_current_members);
        '''
        self.cur.execute(sql_mark_deleted)
        self.cnxn.commit()

    def _email_new_members(self):
        ''' Sends email to new members who have a start date after 10/31/21
        (when this process started) who are not marked as welcome_email_sent_yes. 
        NOTE: ABC files are a month behind, e.g. 12/31 has join dates to 11/30 '''
        sql_new_members = '''
        SELECT 
            member_number
            ,first_name
            ,email
        FROM members
        WHERE
            DATE(join_date) > DATE('2021-10-31')
            AND IFNULL(welcome_email_sent_yes, 0) = 0
            AND IFNULL(email_opt_out_yes, 0) = 0
            AND IFNULL(deleted_yes, 0) = 0;
        '''
        new_members = pd.read_sql(sql_new_members, self.cnxn)
        
        for index, row in new_members.iterrows():
            msg_to_address = row['email']
            # Some first names have middle initial also.
            first_name = row['first_name'].split()[0]
            msg_subject = 'Welcome to the ABC Organization'
            msg_html_content = f'<p>Dear {first_name},</p>' + '''
            <p>On behalf of the ABC Leadership Team, we would like to 
            welcome you to the Organization and thank you for your support. Helpful 
            information, including trainings and leadership team contact information, 
            can be found on the ABC Organization website 
            (<a href="https://abc_organization.org">https://abc_organization.org</a>). 
            Please feel free to reach out to me if you have any questions about the 
            Organization.</p>
            <p>Regards,<br>
            John Doe<br>
            ABC Organization Membership Officer<br>
            <a href="membership@abc_organization.org">Membership@abc_organization.org</a></p>
            '''
            self._send_email(msg_to_address, msg_subject, msg_html_content)
        
        # Mark email as sent so only send welcome email once (not next month).
        new_members.to_sql('stage_new_members', self.cnxn, if_exists='replace')
        sql_sent = '''
        UPDATE members
            SET welcome_email_sent_yes = 1
            WHERE member_number IN
                (SELECT member_number FROM stage_new_members);
        '''
        self.cur.execute(sql_sent)
        self.cnxn.commit()
        
    def _email_terminated_members(self):
        ''' Sends email to terminated members who are either marked as deleted_yes (not
        in current listing of members) or who have a terminated date after 11/30/21
        (when this process started, a month after new members process) and are 
        not marked as terminated_email_sent_yes. '''
        pass
    
    def _send_email(self, to_address, subject, html_content):
        ''' Sends email from membership@abc_organization.org (Go Daddy email). '''
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = str(Header('ABC Organization Membership Officer <membership@abc_organization.org>'))
        msg['To'] = to_address
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        self.server.send_message(msg)

if __name__ == "__main__":
    abc = ABC_Member_Email()
    abc.send_abc_member_emails()
    abc.cnxn.close()
    abc.server.close()
