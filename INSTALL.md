# Installing Kratos

1. Clone the repo
2. Install the Python packages in requirements.txt and mariadb (ev mariadb-client on the display computer)
3. Install Mariadb, create a database with the tables in the database/ddl folder. 
4. <TODO: Config database in .config>
5. Create crontab entries using the example jobserver crontab in the install folder as templates
6. If the Kratosdisplay is being run on a different computer:
	- Clone the repo there
	- Copy the file install/kratosdisplay.sync_cratosdata to a suitable place on the display computer
	- Create a crontab entry using the example kratosdisplay crontab in the install folder as template
7. Run kratos/kratosdisplay.py on the display computer.  
