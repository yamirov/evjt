import csv

def get_ddrphy_top_column_content(csv_file_path):
    ddrphy_top_content = []

    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        # Check if 'ddrphy_top' column exists
        if 'ddrphy_top' not in csvreader.fieldnames:
            raise ValueError("The column 'ddrphy_top' does not exist in the CSV file.")

        # Iterate over each row and collect the 'ddrphy_top' column content
        for row_number, row in enumerate(csvreader, start=1):
            ddrphy_top_content.append((row_number, row['ddrphy_top']))

    return ddrphy_top_content

# Example usage
csv_file_path = r'C:\Users\yamirov\OneDrive - Intel Corporation\Desktop\scripts\margin_hist_expand\shmata.csv'
try:
    content = get_ddrphy_top_column_content(csv_file_path)
    for row_number, item in content:
        print(f"Row {row_number}: {item}")
except Exception as e:
    print(f"An error occurred: {e}")