import yaml
import csv
import os

# Global variables to store data
group_lists = []
radio_ids = []
channels_dict = {}
contacts_dict = {}
zones = []

def preprocess_yaml_content(yaml_content):
    # Replace the !<!default> tags with an empty string or another placeholder
    return yaml_content.replace('!<!default>', '')

def get_rx_tone(tone):
    if isinstance(tone, dict):
        if 'ctcss' in tone:
            return f"{tone['ctcss']:.1f}"
        elif 'dcs' in tone:
            return tone['dcs']
    return "None"

def get_tx_tone(tone):
    if isinstance(tone, dict):
        if 'ctcss' in tone:
            return f"{tone['ctcss']:.1f}"
        elif 'dcs' in tone:
            return tone['dcs']
    return "None"

def get_squelch(squelch):
    return 'Disabled'

def get_power(power):
    return 'Master'

def get_vox(vox):
    return "Off" if vox == 0 else vox

def get_tg_list(group_id):
    global group_lists
    for group in group_lists:
        if group.get('id') == group_id:
            return group.get('name', '')
    return 'None'

def get_timeslot(timeslot):
    if timeslot == "TS1":
        return 1
    elif timeslot == "TS2":
        return 2
    else:
        return ""

def get_dmr_id(radio_id):
    global radio_ids
    for item in radio_ids:
        if item.get('dmr', {}).get('id') == radio_id:
            return item.get('dmr', {}).get('number', '')
    return "None"

def get_channel_name(channel):
    if isinstance(channel, dict):
        return channel.get('name', '')
    elif isinstance(channel, str):
        return channel
    return ""

def get_ts_override(ts):
    if ts.startswith('TS'):
        return ts[2:]
    elif ts == "None":
        return "Disabled"
    else:
        return ts

def write_channels_csv(data, csv_file_path):
    global group_lists, radio_ids, channels_dict
    
    try:
        # Extract groupLists and radioIDs from data
        group_lists = data.get('groupLists', [])
        radio_ids = data.get('radioIDs', [])

        print("Processing channels data.")

        # Define the CSV headers
        headers = [
            "Channel Number", "Channel Name", "Channel Type", "Rx Frequency", "Tx Frequency",
            "Bandwidth (kHz)", "Colour Code", "Timeslot", "Contact", "TG List", "DMR ID",
            "TS1_TA_Tx", "TS2_TA_Tx ID", "RX Tone", "TX Tone", "Squelch", "Power", "Rx Only",
            "Zone Skip", "All Skip", "TOT", "VOX", "No Beep", "No Eco", "APRS", "Latitude", "Longitude"
        ]

        # Open the Channels CSV file for writing
        with open(csv_file_path, 'w', newline='') as cf:
            writer = csv.writer(cf, delimiter=';')
            
            # Write the header
            writer.writerow(headers)
            
            # Iterate through the channels and write each channel's data to the CSV file
            for index, channel in enumerate(data.get('channels', [])):
                if 'analog' in channel:
                    analog = channel['analog']
                    row = [
                        index + 1,  # Channel Number
                        get_channel_name(analog),  # Channel Name
                        "Analogue",  # Channel Type
                        f"{analog.get('rxFrequency', 0):.5f}",  # Rx Frequency
                        f"{analog.get('txFrequency', 0):.5f}",  # Tx Frequency
                        # "12.5",  # Bandwidth (kHz)
                        25 if analog.get('bandwidth', 12.5) == "Wide" else 12.5,
                        "",  # Color Code
                        "",  # Timeslot
                        "",  # Contact
                        "",  # TG List
                        "",  # DMR ID
                        "",  # TS1_TA_Tx
                        "",  # TS2_TA_Tx ID
                        get_rx_tone(analog.get('rxTone', {})),  # RX Tone
                        get_tx_tone(analog.get('txTone', {})),  # TX Tone
                        get_squelch(analog.get('squelch', '')), # Squelch
                        get_power(analog.get('power', '')),  # Power
                        "Yes" if analog.get('rxOnly', False) else "No",  # Rx Only
                        "Yes" if analog.get('openGD77', {}).get('scanZoneSkip', False) else "No",  # Zone Skip
                        "Yes" if analog.get('openGD77', {}).get('scanAllSkip', False) else "No",  # All Skip
                        analog.get('timeout', 0),  # TOT
                        get_vox(analog.get('vox', 0)),  # VOX
                        "No",  # No Beep
                        "No",  # No Eco
                        "None",  # APRS
                        "0",  # Latitude
                        "0"  # Longitude
                    ]
                elif 'digital' in channel:
                    digital = channel['digital']
                    row = [
                        index + 1,  # Channel Number
                        get_channel_name(digital),  # Channel Name
                        "Digital",  # Channel Type
                        f"{digital.get('rxFrequency', 0):.5f}",  # Rx Frequency
                        f"{digital.get('txFrequency', 0):.5f}",  # Tx Frequency
                        "",  # Bandwidth (kHz)
                        digital.get('colorCode', ''),  # Colour Code
                        get_timeslot(digital.get('timeSlot', '')),  # Timeslot
                        # get_contact(digital.get('contact', '')),  # Contact
                        "None", # Contact
                        get_tg_list(digital.get('groupList', '')),  # TG List
                        get_dmr_id(digital.get('radioId', '')),  # DMR ID
                        "Off",  # TS1_TA_Tx
                        "Off",  # TS2_TA_Tx ID
                        "",  # RX Tone
                        "",  # TX Tone
                        "",  # Squelch
                        get_power(analog.get('power', '')),  # Power
                        "Yes" if digital.get('rxOnly', False) else "No",  # Rx Only
                        "Yes" if digital.get('openGD77', {}).get('scanZoneSkip', False) else "No",  # Zone Skip
                        "Yes" if digital.get('openGD77', {}).get('scanAllSkip', False) else "No",  # All Skip
                        digital.get('timeout', 0),  # TOT
                        get_vox(analog.get('vox', 0)),  # VOX
                        "No",  # No Beep
                        "No",  # No Eco
                        "None",  # APRS
                        "0",  # Latitude
                        "0"  # Longitude
                    ]
                channels_dict[f"ch{index + 1}"] = get_channel_name(analog if 'analog' in channel else digital)
                writer.writerow(row)
        
        print("Channels CSV file created successfully.\n")

    except Exception as e:
        print(f"An error occurred: {e}")

def write_contacts_csv(data, csv_file_path):
    global contacts_dict
    
    try:
        contacts = data.get('contacts', [])
        
        print("Processing contacts data.")

        # Define the CSV headers
        headers = ["Contact Name", "ID", "ID Type", "TS Override"]
        
        with open(csv_file_path, 'w', newline='') as zf:
            writer = csv.writer(zf, delimiter=';')
            
            # Write the header row
            writer.writerow(headers)
            
            for contact in contacts:
                contact = contact.get('dmr', {})
                row = [
                    contact.get('name'),
                    contact.get('number'),
                    "Group" if contact.get('type') == "GroupCall" else contact.get('type'),
                    get_ts_override(contact.get('openGD77').get('timeSlotOverride'))
                ]
                contacts_dict[contact.get('id')] = contact.get('name')
                writer.writerow(row)
        
        print("Contacts CSV file created successfully.\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def write_tg_lists_csv(data,csv_file_path):
    global contacts_dict
    
    try:
        tg_lists = data.get('groupLists', [])
        
        print("Processing TG lists data.")

        # Define the CSV headers
        headers = ["TG List Name"]
        for i in range(1, 33):
            headers.append(f"Contact{i}")
        
        with open(csv_file_path, 'w', newline='') as zf:
            writer = csv.writer(zf, delimiter=';')
            
            # Write the header row
            writer.writerow(headers)
            
            for tg_list in tg_lists:
                row = [tg_list.get('name')]
                
                tg_contacts = tg_list.get('contacts')
                
                for contact_index in range(1, 33):
                    if contact_index <= len(tg_contacts):
                        contact_id = tg_contacts[contact_index - 1]
                        contact_name = contacts_dict[contact_id]
                        row.append(contact_name)
                    else:
                        row.append("")  # Fill empty if fewer channels
                
                writer.writerow(row)
        
        print("TG Lists CSV file created successfully.\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def write_zones_csv(data, csv_file_path):
    global channels_dict
    global zones
    
    try:
        # Extract zones from data
        zones = data.get('zones', [])

        print("Processing zones data.")

        # Define the CSV headers
        headers = ["Zone Name"]
        for i in range(1, 81):
            headers.append(f"Channel{i}")
        
        # Open the Zones CSV file for writing
        with open(csv_file_path, 'w', newline='') as zf:
            writer = csv.writer(zf, delimiter=';')
            
            # Write the header row
            writer.writerow(headers)
            
            # Iterate through zones and write each zone's channels to the CSV file
            for zone in zones:
                row = [zone.get('name', '')]

                # Extract channels A and B
                channels_A = zone.get('A', [])
                channels_B = zone.get('B', [])

                # Combine channels A and B
                combined_channels = channels_A + channels_B

                # Write up to 80 channels for each zone
                for channel_index in range(1, 81):
                    if channel_index <= len(combined_channels):
                        channel_id = combined_channels[channel_index - 1]
                        channel_name = channels_dict[channel_id]
                        row.append(channel_name)
                    else:
                        row.append("")  # Fill empty if fewer channels

                # Write the row to CSV file
                writer.writerow(row)
        
        print("Zones CSV file created successfully.\n")

    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to load YAML and generate all CSV files
def generate_csv_files(yaml_file_path, channels_csv_file_path, contacts_csv_file_path, zones_csv_file_path):
    try:
        # Read the YAML file and preprocess its content
        with open(yaml_file_path, 'r') as yf:
            raw_content = yf.read()
            preprocessed_content = preprocess_yaml_content(raw_content)
            data = yaml.safe_load(preprocessed_content)
        
        print("YAML file loaded and preprocessed successfully.\n")
        
        # Generate each CSV file using the loaded data
        write_channels_csv(data, channels_csv_file_path)
        write_contacts_csv(data, contacts_csv_file_path)
        write_tg_lists_csv(data, tg_lists_csv_file_path)
        write_zones_csv(data, zones_csv_file_path)
        
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Paths
current_dir = os.path.dirname(__file__) if os.path.dirname(__file__) else '.'
yaml_file_path = os.path.join(current_dir, '..', 'GD-77.yaml')
channels_csv_file_path = os.path.join(current_dir, 'Channels.csv')
contacts_csv_file_path = os.path.join(current_dir, 'Contacts.csv')
tg_lists_csv_file_path = os.path.join(current_dir, 'TG_Lists.csv')
zones_csv_file_path = os.path.join(current_dir, 'Zones.csv')

# Generate CSV files
generate_csv_files(yaml_file_path, channels_csv_file_path, contacts_csv_file_path, zones_csv_file_path)
