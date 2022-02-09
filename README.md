# Kratos

Kratos is a Home Automation application for the Raspberry Pi. 

Knowledge is power, so the ancient Greek God of Strength comes to our rescue when it comes to knowledge about our home and the environment around it.

The application consists of two parts: The data collection and automation control jobs, and the Kratosdisplay application.  The two parts can run on the same computer, or be set up to run on two separate ones.  In the latter case, an rsync script is used to transfer values for display.  Each display value is stored in a separate file in the ~/.config/kratos/display folder.  

## Copyright and Licenses
Copyright (c) 2021 Håkon Klausen

Kratos is licensed under the MIT License.  

Yr Weather Symbols Copyright (c) 2015-2017 Yr

Collect Sensor Data Based upon code copied from rewrite of ldtool
Copyright (c) 2020 Jim Augustsson