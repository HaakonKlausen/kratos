# Kratos

Kratos is a Home Automation application for the Raspberry Pi. 

Knowledge is power, so the ancient Greek God of Strength comes to our rescue when it comes to knowledge about our home and the environment around it.

The application consists of two parts: The data collection and automation control jobs, and the Kratosdisplay application.  The two parts can run on the same computer, or be set up to run on two separate ones.  In the latter case, an rsync script is used to transfer values for display.  Each display value is stored in a separate file in the ~/.config/kratos/displaydata folder.  


