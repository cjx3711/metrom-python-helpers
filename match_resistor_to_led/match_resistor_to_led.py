import sys
import pprint


DIODE_FOOTPRINT_PREFIX = "(footprint \"lifeclocc_keebs:LED"
RESISTOR_FOOTPRINT_PREFIX = "(footprint \"lifeclocc_keebs:R"
OFFSET = [0, 1.7]  # Offset for the resistor position

"""
Format of a footprint block:
  (footprint "lifeclocc_keebs:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder_Side" (layer "F.Cu")
    (tstamp 03b8e690-3fc0-47c7-9107-d89fcfb30565)
    (at 135.31 123.175) # Position of the footprint
    (descr "Resistor SMD 0603 (1608 Metric), square (rectangular) end terminal, IPC_7351 nominal with elongated pad for handsoldering. (Body size source: http://www.tortai-tech.com/upload/download/2011102023233369053.pdf), generated with kicad-footprint-generator")
    .......
    (fp_text reference "R1" (at 4.1656 0) (layer "F.SilkS") # Reference of the footprint
        (effects (font (size 1 1) (thickness 0.15)))
      (tstamp 8f13f99e-5e3c-48b5-888c-f99ce6ee5c27)
    )
    ........
    (model "${KISYS3DMOD}/Resistor_SMD.3dshapes/R_0603_1608Metric.wrl"
      (offset (xyz 0 0 0))
      (scale (xyz 1 1 1))
      (rotate (xyz 0 0 0))
    )
  ) # End of the footprint block
"""

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
        # if line starts with the diode footprint prefix, extract the reference and position
        if line.strip().startswith(DIODE_FOOTPRINT_PREFIX):
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
        # if line starts with the resistor footprint prefix, extract the block and update the position
        if line.strip().startswith(RESISTOR_FOOTPRINT_PREFIX):
          resistor_block = []

          # Extract the resistor block and store it in a temporary variable
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
              positionX = diode["positionX"] + OFFSET[0]
              positionY = diode["positionY"] + OFFSET[1]
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
