

disconnecting_means_id = None
power_sources = []
pcs_devices = []
service_conductor_amperage = None

# checks if a circuit element's output is connected directly or indirectly to the disconnecting means
# with no PCS in between.
def is_connected_with_no_pcs(item):
    current_item = item
    while current_item is not None:
        output_id = current_item['output']
        if output_id == None:
            return False
        if output_id == disconnecting_means_id:
            return True
        if pcs_devices.find(x['id'] == output_id):
            return False
        current_item = power_sources.find(x['id'] == output_id)
        if current_item == None:
            return False

def is_compliant(data):
    # identify different elements 
    for item in data.elements:
        if item.type == 'disconnecting-means':
            disconnecting_means_id = item['id']
        elif item.type == 'service-conductor':
            service_conductor_amperage = item['current-rating-amps']
        elif item.type == 'solar-photovoltaic-system' or item.type == 'battery-system':
            power_sources.append(item)
        elif item.type == 'pcs':
            pcs_devices.append(item)

    # I'm assuming that disconnecting_means_id and service_conductor_amperage both have values
    # at this point. Production code would have checks to ensure this.

    # process power sources
    total_current = 0.0
    for power_source in power_sources:
        if is_connected_with_no_pcs(power_source):
            total_current += power_source['current-output-amps']

    return total_current < service_conductor_amperage