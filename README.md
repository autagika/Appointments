# Appointments
A simple web application which adds appointments to a database and search them

The following files are used in this application
1) form.html - This is the html file which displays the appointment form, front end and the search button and text field
2) add.cgi - This Perl script contains the functionality to add appointments to the MySQL database
3) search.cgi - This Perl script contains the functionality to search appointments in the database
4) js/appointments.js - This javascript file contains the frontend code to add new appointments, cancel them and AJAX
                     functionality to search the appointments
5) css/style1.css - This file add styling to the application
6) css/style2.css - This file adds styling to the application
7) sql/appointments.sql - This file contains the sql code of the database

Steps to be taken before the application can be run
===================================================

1) Install MySQL database and Apache HTTP server
2) Create a MySQL database called webapp with the following components

Tables
======
1) appointments

Columns
==========
1) id - int  autoincrement primary key not null
2) appointmenttime - date format unique index not null
3) Description - text format not null

Once that is done, you can add and search the appointments using the following url

http://localhost/form
