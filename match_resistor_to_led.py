import sys
import pprint

def main():
 
  #  Diode value is of format:
  #  {
  #    "reference": "D1",
  #    "positionX": 1,
  #    "positionY": 1,
  #  }
  diode_values = []
  if len(sys.argv) == 3:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
  else:
    input_file = input("Enter the input file name: ")
    output_file = input("Enter the output file name: ")
  
  try:
    lines = []
    with open(input_file, 'r') as infile:
      lines = infile.readlines()
      total_lines = len(lines)

      iterator = 0
      while iterator < total_lines:
        line = lines[iterator]
        # if line starts with "(footprint \"lifeclocc_keebs:LED" then it is a diode
        if line.strip().startswith("(footprint \"lifeclocc_keebs:LED"):
          reference = ""
          positionX = 0
          positionY = 0

          while iterator < total_lines:
            line = lines[iterator].strip()
            if line.startswith("(at "):
              # Extract position
              parts = line.split()
              positionX = float(parts[1])
              positionY = float(parts[2].strip(')'))
            elif line.startswith("(fp_text reference "):
              # Extract reference
              reference = line.split()[2].strip('"')
            elif line.startswith(")"):
              # End of the diode block
              break
            iterator += 1
          # Add the extracted values to the list
          diode_values.append({
            "reference": reference,
            "positionX": positionX,
            "positionY": positionY,
          })
        iterator += 1
        
      pprint.pprint(diode_values)

    with open(output_file, 'w') as outfile:
      iterator = 0
      while iterator < total_lines:
        line = lines[iterator]
        if line.strip().startswith("(footprint \"lifeclocc_keebs:R"):
          resistor_block = []
          while iterator < total_lines:
            resistor_block.append(lines[iterator])
            if lines[iterator].startswith("  )"):
                break
            iterator += 1

          # Extract reference and position for the resistor
          reference = ""
          positionX = 0
          positionY = 0
          for res_line in resistor_block:
            if res_line.strip().startswith("(at "):
              parts = res_line.split()
              positionX = float(parts[1])
              positionY = float(parts[2].strip(')'))
            elif res_line.strip().startswith("(fp_text reference "):
              reference = res_line.split()[2].strip('"')

          # Check for corresponding diode
          diode_reference = "D" + reference[1:]
          for diode in diode_values:
            if diode["reference"] == diode_reference:
              positionX = diode["positionX"]
              positionY = diode["positionY"] + 1.7  # Adjust the offset as needed
              break

          # Update the resistor block with new coordinates
          for i, res_line in enumerate(resistor_block):
            if res_line.strip().startswith("(at "):
              resistor_block[i] = f"    (at {positionX} {positionY})\n"

          # Write the updated resistor block to the output file
          outfile.writelines(resistor_block)
        else:
          outfile.write(line)
        iterator += 1

      print(f"Output written to {output_file}")
  except FileNotFoundError:
    print(f"Error: The file {input_file} does not exist.")
  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == "__main__":
  main()
