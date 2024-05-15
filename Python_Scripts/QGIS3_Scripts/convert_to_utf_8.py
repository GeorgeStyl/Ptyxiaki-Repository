import csv
import os 



def convert_encoding(input_file, output_file, input_encoding='utf-8', output_encoding='utf-8'):
    """
    Convert the encoding of a CSV file from its original encoding to UTF-8.

    Parameters:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file with UTF-8 encoding.
        input_encoding (str, optional): The encoding of the input CSV file. Defaults to 'utf-8'.
        output_encoding (str, optional): The encoding for the output CSV file. Defaults to 'utf-8'.

    Returns:
        None

    Raises:
        FileNotFoundError: If the input file is not found.
    """
    with open(input_file, mode='r', encoding=input_encoding, newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    with open(output_file, mode='w', encoding=output_encoding, newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the script
    input_file = os.path.join(script_dir, "test_data.csv")     # Construct the full path to input file
    output_file = os.path.join(script_dir, "output_test_data.csv")

    convert_encoding(input_file, output_file)
    print("CSV file encoded to UTF-8 successfully.")
