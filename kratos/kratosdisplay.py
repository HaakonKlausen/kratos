#!/usr/bin/python3

import datetime
from os import stat_result
import pytz
import tkinter as tk
import tkinter.font as tkFont
import time
import datetime 
import sys

import mysql.connector

import kratoslib 


###############################################################################
# Parameters and global variables

# Default font size
font_size = -12

# Declare global variables
root = None
dfont = None
frame = None
dtime = None

# Global variable to remember if we are fullscreen or windowed
fullscreen = False

###############################################################################
# Functions

# Toggle fullscreen
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize()

# Return to windowed mode
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize()

# Automatically resize font size based on window size
def resize(event=None):

    global time_dfont
    global temp_dfont
    global button_dfont
    global date_dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 6)))
    time_dfont.configure(size=new_size)
    new_size = -max(12, int((frame.winfo_height() / 11)))
    date_dfont.configure(size=new_size)
    new_size = -max(12, int((frame.winfo_height() / 4.5)))
    temp_dfont.configure(size=new_size)
    new_size = -max(12, int((frame.winfo_height() / 22)))
    button_dfont.configure(size=new_size)


def readKratosData(filename):
	value = ''
	try:
		value = kratoslib.readKratosDataFromSql(filename)
	except:
		# If we don't get the value from the database, try the file instead
		kratoslib.writeKratosLog('ERROR', 'Unable to read kratosdata for ' + filename + ' from the database, trying the file instead')
		value = ''
	if value == '':
		value = kratoslib.readKratosData(filename)
		
	return value

    #filepath="/home/haakon/kratosdata/" + filename
    #file = open(filepath, "r")
    #value = file.read()
    #file.close()
    #return value.strip()


def getWeatherIcon(p_symbol_code):
    symbol_codes = {'clearsky': '01', 
                    'cloudy': '04','fair': '02','fog': '15','heavyrain': '10','heavyrainandthunder':'11','heavyrainshowers':'41',
                    'heavyrainshowersandthunder': '11', 'heavysleet': '48', 'heavysleetandthunder': '32', 'heavysleetshowers': '43',
                    'heavysleetshowersandthunder': '27', 'heavysnow': '50', 'heavysnowandthunder': '27', 'heavysnowshowers': '45',
                    'heavysnowshowersandthunder': '29', 'lightrain': '46', 'lightrainandthunder': '30', 'lightrainshowers': '40',
                    'lightrainshowersandthunder': '24', 'lightsleet': '47', 'lightsleetandthunder': '31', 'lightsleetshowers': '42', 
                    'lightsnow': '49', 'lightsnowandthunder': '33', 'lightsnowshowers': '44', 'lightssleetshowersandthunder': '26',
                    'lightssnowshowersandthunder': '28', 'partlycloudy': '03', 'rain': '09', 'rainandthunder': '22', 'rainshowers': '05',
                    'rainshowersandthunder': '06', 'sleet': '12', 'sleetandthunder': '22', 'sleetshowers': '07', 'sleetshowersandthunder': '20',
                    'snow': '13', 'snowandthunder': '14', 'snowshowers': '08', 'snowshowersandthunder': '21'}

    symbol_codes_day = {'clearsky': '01d', 
                    'cloudy': '04','fair': '02d','fog': '15','heavyrain': '10','heavyrainandthunder':'11','heavyrainshowers':'41d',
                    'heavyrainshowersandthunder': '11', 'heavysleet': '48', 'heavysleetandthunder': '32', 'heavysleetshowers': '43',
                    'heavysleetshowersandthunder': '27d', 'heavysnow': '50', 'heavysnowandthunder': '27d', 'heavysnowshowers': '45',
                    'heavysnowshowersandthunder': '29d', 'lightrain': '46', 'lightrainandthunder': '30', 'lightrainshowers': '40d',
                    'lightrainshowersandthunder': '24d', 'lightsleet': '47', 'lightsleetandthunder': '31', 'lightsleetshowers': '42d', 
                    'lightsnow': '49', 'lightsnowandthunder': '33', 'lightsnowshowers': '44d', 'lightssleetshowersandthunder': '26d',
                    'lightssnowshowersandthunder': '28d', 'partlycloudy': '3d', 'rain': '09', 'rainandthunder': '22', 'rainshowers': '05d',
                    'rainshowersandthunder': '06d', 'sleet': '12', 'sleetandthunder': '22', 'sleetshowers': '07d', 'sleetshowersandthunder': '20d',
                    'snow': '13', 'snowandthunder': '14', 'snowshowers': '08d', 'snowshowersandthunder': '21d', 'lightsnowshowers_day': '44d'}
    
    symbol_code = p_symbol_code.strip()
    filename = ''
    description = ''
    icon = ''

    if symbol_code in symbol_codes:
        icon_str = str(symbol_codes.get(symbol_code))
    else:
        if symbol_code.find('_day') >=0 or symbol_code.find('_night') >=0: 
            if symbol_code.split('_')[0] in symbol_codes:
                icon_str = str(symbol_codes.get(symbol_code.split('_')[0]))
                if symbol_code.find('_day') >=0:
                    icon_str = icon_str + "d"
                else:
                    icon_str = icon_str + "n"
            else:
                print('ERROR: Symbol not found: ' + symbol_code)
    
    filename = kratoslib.getYrSymbolFilePath(icon_str + '.png')
    #filename = 'yr-weather-symbols/png/'+ icon_str + '.png'
    return filename, description


def timestamp2display(timestamp):
    hour=timestamp[11:13]
    minute=timestamp[14:16]
    return hour + ':' + minute

def utc2osl(timestamp): 
    utc_timezone=pytz.timezone('UTC')
    timestamp_date = utc_timezone.localize(datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ'))
    osl_timezone=pytz.timezone('Europe/Oslo')
    expires_date_osl = timestamp_date.astimezone(osl_timezone)
    return str(expires_date_osl)



# Read values from the sensors at regular intervals
def update():
	kratoslib.writeKratosLog('DEBUG', 'Updating display')
	global root
	global dtime
	global ddate
	global dtemp
	global label_temp
	global label_temp_inside
	global dcottagetemp
	global dcottagetempinside
	global dcottageactivepower
	global label_cottage_temp
	global label_cottage_temp_inside
	global dsymbolcode
	global dpowerprice
	global dmaxpowerprice
	global dactivepower

	global label_weather_icon
	global label_weather_icon2
	global weathericon
	global label_powerprice
	global label_date
	global label_active_power
	global dactarget 
	global dchargertarget
	global label_charger_icon
	global chargericon
	global label_ac_icon
	global acicon

	mndnames=['Januar', 'Februar', 'Mars', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Desember']
	# Get local time
	local_time = time.localtime()

	# Convert time to 12 hour clock
	hours = local_time.tm_hour
	#if hours > 12:
	#    hours -= 12

	local_date = time.localtime()
	local_date_str = time.strftime('%d', local_date)
	if local_date_str[0:1] == '0':
		local_date_str = local_date_str[1:]
	local_month = int(time.strftime('%m', local_date))
	local_month_str = mndnames[local_month - 1]
	local_date_str = local_date_str + '. ' + local_month_str
	# Add leading 0s
	shours = str(hours)
	smin = str(local_time.tm_min)
	if hours < 10:
		shours = '0' + shours
	if local_time.tm_min < 10:
		smin = '0' + smin

	# Construct string out of tAime
	dtime.set(shours + ':' + smin)
	ddate.set(local_date_str)
	if local_date_str == '24.. Desember':
		label_date.config(fg='red')
	else:
		label_date.config(fg='gray50')



	in_temp = str(readKratosData("in.temp"))
	dtempinside.set(" " + in_temp + u"\u00b0")        # u2103 with C, \u00b0 without

	powerstate = readKratosData('panasonic.power')
	if powerstate == 'Power.Off':
		dactarget.set(' ')
		aciconfile = 'black_icon_59.png'
	else:
		aciconfile = 'heatpump_icon_grey_75.png'
		ac_target = str(readKratosData("panasonic.temperature"))
		dactarget.set(" " + ac_target + u"\u00b0")

	aciconpath = kratoslib.getImageFilePath(aciconfile)
	acicon = tk.PhotoImage(file=aciconpath)
	label_ac_icon.config(image=acicon)

	try:
		chargePower = float(readKratosData('tesla.chargePower'))
		plug = str(readKratosData('tesla.plug'))
		soc = str(readKratosData('tesla.soc'))
		target_soc = str(readKratosData('tesla.targetSoc'))
		#state = str(readKratosData('tesla.state'))

		cariconfile='car_icon_grey_59.png'
		charging = False

		if readKratosData('tesla.online') == 'False':
			cariconfile='black_icon_59.png'
			dchargertarget.set(' ')
		elif readKratosData('tesla.driving') == 'True':
			cariconfile='car_driving_icon_grey_59.png'
			dchargertarget.set(str(readKratosData("tesla.currentDistance")) + ' km')
		else:
			if plug == 'Disconnected':
				if int(round(float(soc))) == int(round(float(target_soc))):
					cariconfile='car_charged_icon_grey_59.png'
				else:
					cariconfile='car_icon_grey_59.png'
			else:
				cariconfile = 'charger_icon_grey_59.png'
				if int(round(float(soc))) == int(round(float(target_soc))):
					cariconfile='charger_charged_icon_grey_59.png'
				elif chargePower > 0: #state != 'readyForCharging':
					cariconfile='charger_charging_icon_grey_59.png'
					charging = True

			if charging == True:
				remainingMinutes = 0
				try:
					remainingMinutes = int(round(float(readKratosData("tesla.remainingChargeTime"))))
				except:
					pass
				h=remainingMinutes//60
				m=remainingMinutes-(h*60)
				dchargertarget.set(str(h) + ':' + str(m).zfill(2))
			else:
				dchargertarget.set(str(readKratosData("tesla.soc"))[:-2] + '% ')


		cariconpath=kratoslib.getImageFilePath(cariconfile)
		chargericon = tk.PhotoImage(file=cariconpath)
		label_charger_icon.config(image=chargericon)
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Unable to read Tesla data: ' + str(e))
		
	
	out_temp = readKratosData("out.temp")
	out_temp_str = str(out_temp)
	if float(out_temp) > 0:
		label_temp.config(fg='red')
	else:
		label_temp.config(fg='blue')
	dtemp.set(out_temp_str + u"\u00b0")


	powerprice_eur = float(readKratosData('powerprice.eur'))
	powerprice_nok = round(((powerprice_eur * 10.12 / 1000) + 0.05) * 1.25, 2)
	powerprice_nok_str = "{:.2f}".format(powerprice_nok)
	dpowerprice.set(str(powerprice_nok_str) + " kr/kWh")
	#dpowerprice.set(u"\u20AC" + str(readKratosData('powerprice.eur')) + " MW/h")

	powerprice_max_eur = float(readKratosData('powerprice_max.eur'))
	powerprice_max_nok = round(((powerprice_max_eur * 10.12 / 1000) + 0.05) * 1.25, 2)
	powerprice_max_nok_str = "{:.2f}".format(powerprice_max_nok)
	powerprice_max_period = readKratosData('powerprice_max.period')
	dmaxpowerprice.set('Max: ' + powerprice_max_nok_str + ' (' + powerprice_max_period + ':00)')

	# Check if powerprice is in the highest 3 hours
	powerprice_3max_eur = float(readKratosData('powerprice_3max.eur'))
	if powerprice_eur >= powerprice_3max_eur and powerprice_nok > 2:
		label_powerprice.config(fg='red')
	else:
		label_powerprice.config(fg='gray50')
	
	if powerprice_max_nok > 2 and int(powerprice_max_period) >= int(hours):
		label_max_powerprice.config(fg='red')
	else:
		label_max_powerprice.config(fg='gray50')

	try:
		filename, description=getWeatherIcon(str(readKratosData('yr.symbol_code')))
		weathericon = tk.PhotoImage(file=filename)
		label_weather_icon.config(image=weathericon)
		label_weather_icon2.config(image=weathericon)
		period_start = str(readKratosData('yr.period_start'))

		precipitation_amount = str(readKratosData('yr.precipitation_amount'))
		wind_speed = str(readKratosData('yr.wind_speed'))
		#print('Period start: ' + period_start)
		period_start = utc2osl (period_start)
		if float(precipitation_amount) > 0:
			dsymbolcode.set(precipitation_amount + ' mm')
		else:
			dsymbolcode.set('')
		#timestamp2display(period_start) + ' -> ' + 
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Unable to read weather data: ' + str(e))
		dsymbolcode.set('')
	
	try:
		activepower=int(readKratosData('oss.active_power').split('.')[0])
		activepower_kw = activepower / 1000
		if activepower > 9999:
			activepower_kw_str="{:.0f}".format(activepower_kw)
		else:
			activepower_kw_str="{:.1f}".format(activepower_kw)
		dactivepower.set(str(activepower_kw_str) + ' kW')
		if activepower > 10000:
				label_active_power.config(fg='red')
		else:
			label_active_power.config(fg='gray50')
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Unable to read OSS data: ' + str(e))
		dactivepower.set('')

	cottage_ovner = readKratosData("bjonntjonn.ovner")
	cottage_temp = str(readKratosData("hytten.out.temp"))

	if float(cottage_temp) > 0:
		label_cottage_temp.config(fg='red')
	else:
		label_cottage_temp.config(fg='blue')

	cottage_inside_temp = str(readKratosData("hytten.in.temp"))
	if float(cottage_inside_temp) < 3.3:
		label_cottage_temp_inside.config(fg='red')
	else:
		if float(cottage_ovner) > 0:
			label_cottage_temp_inside.config(fg='green')
		else:
			label_cottage_temp_inside.config(fg='gray50')

	dcottagetemp.set(cottage_temp + u"\u00b0")
	cottage_inside_temp_str = cottage_inside_temp + u"\u00b0"
	#if float(cottage_ovner) > 0:
#		cottage_inside_temp_str = cottage_inside_temp_str + " ovn"
	dcottagetempinside.set(cottage_inside_temp_str)

	cottage_active_power = str(readKratosData("hytten_oss.active_power"))
	if float(cottage_active_power) > 1000:
		cottage_active_power_kw = float(cottage_active_power) / 1000
		cottage_active_power_kw_str="{:.1f}".format(cottage_active_power_kw)
		dcottageactivepower.set(cottage_active_power_kw_str + ' kW')
	else:
		cottage_active_power_w = float(cottage_active_power)
		cottage_active_power_kw_str="{:.0f}".format(cottage_active_power_w)
		dcottageactivepower.set(cottage_active_power_kw_str + ' W')	

	# Schedule the poll() function for another 1000 ms from now
	root.after(5000, update)

###############################################################################
# Main script

#print(os.getcwd())
#print(__file__)
kratoslib.checkAndInitKratos()

# Create the main window
root = tk.Tk()
root.title("Kratosdisplay")

# Create the main container
frame = tk.Frame(root, bg='black')

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# Variables for holding temperature and light data
dtime = tk.StringVar()
ddate = tk.StringVar()

# Variable for holding temperature data
dtemp = tk.StringVar()

dcottagetemp = tk.StringVar()
dcottagetempinside = tk.StringVar()
dcottageactivepower = tk.StringVar()

dtempinside = tk.StringVar()
dsymbolcode = tk.StringVar()

dpowerprice = tk.StringVar()
dmaxpowerprice = tk.StringVar()

dactivepower = tk.StringVar()
dactarget = tk.StringVar()
dchargertarget = tk.StringVar()

# Create dynamic font for text
temp_dfont = tkFont.Font(family='Helvetica', size=-36)
time_dfont = tkFont.Font(family='Helvetica', size=-8)
date_dfont = tkFont.Font(family='Helvetica', size=-8)
button_dfont = tkFont.Font(size=font_size)

# Read

thermometerlogo = tk.PhotoImage(file=kratoslib.getImageFilePath('thermometerlogo_45.png'))
insidetemplogo = tk.PhotoImage(file=kratoslib.getImageFilePath('inside_temp_logo_dark_grey_35.png'))

filename, description=getWeatherIcon(str(readKratosData('yr.symbol_code')))
weathericon = tk.PhotoImage(file=filename)


acicon = tk.PhotoImage(file='images/heatpump_icon_grey_75.png')
chargericon = tk.PhotoImage(file='images/charger_icon_grey_59.png')

# Create widgets


label_ac_icon = tk.Label(frame, 
                        image=acicon,
                        compound=tk.TOP,
                        textvariable=dactarget,
                        font=date_dfont, 
                        fg='gray50', 
                        bg='black')
label_charger_icon = tk.Label(frame, 
                        image=chargericon,
                        compound=tk.TOP,
                        textvariable=dchargertarget,
                        font=date_dfont, 
                        fg='gray50', 
                        bg='black')
label_active_power = tk.Label(frame, 
#                        image=powerlogo,
#                        compound=tk.LEFT,
                        textvariable=dactivepower, 
                        font=time_dfont, 
                        fg='gray50', 
                        bg='black')
label_weather_icon = tk.Label(frame, 
                        image=weathericon,
                        compound=tk.TOP,
                        textvariable=dsymbolcode,
                        font=date_dfont, 
                        fg='gray50', 
                        bg='black'
)
label_weather_icon2 = tk.Label(frame, 
                        image=weathericon,
                        compound=tk.TOP,
                        textvariable=dsymbolcode,
                        font=button_dfont, 
                        fg='gray50', 
                        bg='black'
)
label_powerprice = tk.Label(frame, 
                        textvariable=dpowerprice, 
                        font=button_dfont, 
                        fg='gray50', 
                        bg='black')
label_max_powerprice = tk.Label(frame, 
                        textvariable=dmaxpowerprice, 
                        font=button_dfont, 
                        fg='gray50', 
                        bg='black')                    
label_temp = tk.Label(  frame, 
                        #image=thermometerlogo,
                        #compound=tk.LEFT,
                        textvariable=dtemp, 
                        font=temp_dfont, 
                        fg='gray50', 
                        bg='black')
label_time = tk.Label(  frame, 
                        textvariable=dtime, 
                        font=time_dfont, 
                        fg='gray50', 
                        bg='black')
label_date = tk.Label(  frame, 
                        textvariable=ddate, 
                        font=date_dfont, 
                        fg='gray50', 
                        bg='black')
label_temp_inside = tk.Label(  frame, 
                        image=insidetemplogo,
                        compound=tk.LEFT,
                        textvariable=dtempinside, 
                        font=date_dfont, 
                        fg='red', 
                        bg='black')
button_quit = tk.Button(frame, 
                        text="Quit", 
                        font=button_dfont, 
                        command=root.destroy,
                        borderwidth=0,
                        highlightthickness=0, 
                        fg='gray10',
                        bg='black')

label_cottage_temp = tk.Label(  frame, 
                        compound=tk.LEFT,
                        textvariable=dcottagetemp, 
                        font=date_dfont, 
                        fg='gray50', 
                        bg='black')
label_cottage_temp_inside = tk.Label(  frame, 
                        compound=tk.LEFT,
                        textvariable=dcottagetempinside, 
                        font=date_dfont, 
                        fg='gray50', 
                        bg='black')
label_cottage_active_power = tk.Label(  frame, 
                        compound=tk.LEFT,
                        textvariable=dcottageactivepower, 
                        font=date_dfont, 
                        fg='gray50', 
                        bg='black')

# Lay out widgets in a grid in the frame
label_ac_icon.grid(row=0, column=0, rowspan=1, columnspan=1, padx=0, pady=0, sticky=tk.W)
label_charger_icon.grid(row=0, column=1, rowspan=1, columnspan=1, padx=0, pady=0, sticky=tk.E)
label_weather_icon.grid(row=0, column=2, rowspan=2, columnspan=2, padx=0, pady=0)
#label_weather_icon2.grid(row=0, column=3, rowspan=2, columnspan=2, padx=0, pady=0, sticky=tk.E)
label_temp.grid(row=0, column=5, columnspan=2, padx=0, pady=0, sticky=tk.E)
label_active_power.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky=tk.W)

label_cottage_temp.grid(row=2, column=0, padx=0, pady=0, sticky=tk.S)
label_cottage_temp_inside.grid(row=2, column=1, padx=0, pady=0, sticky=tk.S)

label_time.grid(row=2, column=2, columnspan=2, padx=0, pady=0, sticky=tk.S)
label_date.grid(row=2, column=6, padx=0, pady=0, sticky=tk.S)

label_temp_inside.grid(row=1, column=6, padx=0, pady=0)

label_cottage_active_power.grid(row=4, column=0, columnspan=2, padx=0, pady=0, sticky=tk.SW)
label_powerprice.grid(row=4, column=5, columnspan=2, padx=0, pady=0, sticky=tk.SW)
label_max_powerprice.grid(row=4, column=2, columnspan=1, padx=0, pady=0, sticky=tk.SW)


button_quit.grid(row=4, column=6, padx=0, pady=0, sticky=tk.E)

# Make it so that the grid cells expand out to fill window
frame.rowconfigure(0, weight=6) # Weather and outside temp
frame.rowconfigure(1, weight=1) 
frame.rowconfigure(2, weight=1) #Power, timer and date
frame.rowconfigure(3, weight=1) #Empty line
frame.rowconfigure(4, weight=1) #Bottom line
frame.columnconfigure(0, weight=3)
frame.columnconfigure(1, weight=3)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)
frame.columnconfigure(4, weight=1)
frame.columnconfigure(5, weight=1)
frame.columnconfigure(6, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Schedule the poll() function to be called periodically
root.after(20, update)

args = sys.argv[1:]
start_in_fullscreen=True
if len(args) == 1:
	if args[0] == "window":
		start_in_fullscreen = False

# Start in fullscreen mode and run
if start_in_fullscreen:
	toggle_fullscreen()
root.mainloop()


