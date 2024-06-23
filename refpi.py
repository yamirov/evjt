import csv
import re

ccc_partitions = []
for ch in range(8): ccc_partitions.append(f'ch{ch}ccc')
for c in range(2): 
    for b in range(8): 
        ccc_partitions.append(f'data{b}ch{c}')

def find_pattern_lines(file_path,pattern = r"refpi"):
    result = []
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if re.search(pattern, line):
                    result.append(line.strip())
        return result
    except:
        print("somethign went wrong")
        return result

def process_csv_and_add_capicode(input_csv_file_path, output_csv_file_path):
    with open(input_csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        fieldnames = csvreader.fieldnames + ccc_partitions

        with open(output_csv_file_path, mode='w', newline='') as outputfile:
            csvwriter = csv.DictWriter(outputfile, fieldnames=fieldnames)
            csvwriter.writeheader()
            row_ctr= 0
            for row in csvreader:
                print(f'proccessing row number {row_ctr}')
                new_row = row.copy() # result row 
                ddrphy_top_path = row['ddrphy_top']
                capicode_lines = find_pattern_lines(ddrphy_top_path,pattern = r"refpi=")

                if capicode_lines:# by end of iteration all CCC in row should have values
                    for line in capicode_lines:
                        for partition in ccc_partitions:
                            if partition in line : # by end of iteration all CCC should have values
                                new_row[partition] = line.split('=')[1] # parse value from the regdump
                    csvwriter.writerow(new_row) # write output
                else :
                    print("somethign went wrong")
                row_ctr += 1
                
# Example usage
input_csv_file_path = r'C:\Users\yamirov\OneDrive - Intel Corporation\Desktop\scripts\margin_hist_expand\data.csv'
output_csv_file_path = r'C:\Users\yamirov\OneDrive - Intel Corporation\Desktop\scripts\margin_hist_expand\pizdata_refpi.csv'
try:
    process_csv_and_add_capicode(input_csv_file_path, output_csv_file_path)
    print(f"Processed CSV file saved to {output_csv_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")