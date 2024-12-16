import csv

def tab_to_csv(input_file, output_file):
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        	reader = csv.reader(infile, delimiter='\t')
        	writer = csv.writer(outfile)
        	for row in reader:
            		writer.writerow(row) 

if __name__ == "__main__":
    input_file = 'manuf'  # Replace with the path to your input file
    output_file = 'macDict.csv'  # Replace with the desired path for the output file
    tab_to_csv(input_file, output_file)
    print(f"Conversion from {input_file} to {output_file} completed.")