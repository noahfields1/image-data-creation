import csv

def find_avg_col1(file1, file2):
    """
    Reads in two separate CSV files and finds the average of column 1 for each file.

    Parameters:
    file1 (str): File path to CSV file 1.
    file2 (str): File path to CSV file 2.

    Returns:
    Tuple containing the average of column 1 for file1 and file2, respectively.
    """

    # Initialize variables to keep track of sum and count of values in column 1 for each file
    sum_col1_file1 = 0
    count_col1_file1 = 0
    sum_col1_file2 = 0
    count_col1_file2 = 0

    # Read in CSV file 1
    with open(file1, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip header row
        for row in csv_reader:
            sum_col1_file1 += float(row[1])
            count_col1_file1 += 1

    # Calculate average of column 1 for file 1
    avg_col1_file1 = sum_col1_file1 / count_col1_file1

    # Read in CSV file 2
    with open(file2, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip header row
        for row in csv_reader:
            sum_col1_file2 += float(row[1])
            count_col1_file2 += 1

    # Calculate average of column 1 for file 2
    avg_col1_file2 = sum_col1_file2 / count_col1_file2

    # Return tuple of averages
    #return (avg_col1_file1, avg_col1_file2)
    #print(count_col1_file1,sum_col1_file1)
    print(avg_col1_file1)
    print(avg_col1_file2)

find_avg_col1("/Users/noah/Desktop/TEST.csv", "/Users/noah/Desktop/TESTall015.csv")
