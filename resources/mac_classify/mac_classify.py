#00:00:6B         ,SiliconGraph,Silicon Graphics
#00:1B:C5:01:E0/36,Private     ,Private
#00:69:67:10/28   ,miliwave    ,miliwave

import csv

def group_mac_addresses(input_file, output_files):
    """
    Groups MAC addresses from an input CSV file into three output CSV files based on their format.

    Args:
        input_file (str): Path to the input CSV file.
        output_files (list): List of paths to the four output CSV files.
    """

    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        output_writers = [csv.writer(open(f, 'w', newline='')) for f in output_files]

        for row in reader:
            mac_address = row[0].strip()

            if ':' in mac_address and '/' not in mac_address:
                output_writers[0].writerow(row)
            elif '/28' in mac_address:
                output_writers[1].writerow(row)
            elif '/36' in mac_address:
                output_writers[2].writerow(row)
            else:
                output_writers[3].writerow(row)

# Example usage:
input_file = 'full_macDict.csv'
output_files = ['standard_macs.csv', 'prefix_28_macs.csv', 'prefix_36_macs.csv', 'unknown_format_macs.csv']

group_mac_addresses(input_file, output_files)