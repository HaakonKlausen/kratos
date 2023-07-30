import teslapy
with teslapy.Tesla('hakon.klausen@icloud.com') as tesla:
    vehicles = tesla.vehicle_list()
    #vehicles[0].sync_wake_up()
    #vehicles[0].command('ACTUATE_TRUNK', which_trunk='front')
    vehicles[0].get_vehicle_data()
    #print(vehicles[0]['vehicle_state']['car_version'])
    #print(vehicles[0]['charge_state'])
    print(vehicles[0]['charge_state']['battery_level'])
    print(vehicles[0]['charge_state']['charger_power'])
    print(vehicles[0]['charge_state']['charging_state'])
    print(vehicles[0]['charge_state']['conn_charge_cable'])