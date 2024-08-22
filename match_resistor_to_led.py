import sys

def main():
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = input("Enter the input file name: ")
        output_file = input("Enter the output file name: ")

    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
            total_lines = len(lines)
            with open(output_file, 'w') as outfile:
                last_percent = 0
                for i, line in enumerate(lines):
                    outfile.write(line)
                    # Calculate the percentage of completion
                    percent_complete = ((i + 1) / total_lines) * 100
                    current_percent = int(percent_complete)
                    if current_percent > last_percent:
                        print(f"Processed {current_percent}% of lines")
                        last_percent = current_percent
        print(f"Contents of {input_file} have been written to {output_file}.")
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
