import datetime 
message = 'Hello world'
severity = 'INFO'
print(datetime.datetime.now().strftime("%a %d %b %H:%M:%S %Y") + ' App ' + severity + ': ' + message + '\n')