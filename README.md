CMPUT 410 Project - Group 4
================

How to Deploy on VM
========
How to Deploy DJango on VM:
>ssh btrinh1@ohaton.cs.ualberta.ca

>ssh user@cs410.cs.ualberta.ca -p 41040

>Password is ubersomething -- its not actually 'something' but you guys should know it, if not ask Benson.

>cd ~/cmput410-project/BenHoboCo

>git pull

>sudo supervisorctl "restart django"

How to Setup SSH tunnel to VM
========
Then if you want to access the webserver from your machine at home, running the following SSH tunnel command (OSX syntax)
>ssh -L 8080:cs410.cs.ualberta.ca:41048 -p 22 -l btrinh1 -N ohaton.cs.ualberta.ca  

Group Members
=========
ciwong

btrinh1

remco

tpolasek

teschnei


Web Service API & Documentation 
================
https://github.com/tpolasek/cmput410-project/wiki/API


AJAX Documentation
================
Github Activity on a User Profile uses Jquery/AJAX



Setup Documentation
================

How to rebuild the schema
>create database helix;
>GRANT ALL ON helix.* TO 'myuser'@'%';

If you flush the mysql database then you must run the following mysql command:
>INSERT INTO social_siteconfiguration() VALUES(1,1,0);
