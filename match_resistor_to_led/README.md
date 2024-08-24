# match_resistor_to_led.py

## Purpose

This is a helper script to automatically match all the SMD resistors to the corresponding LED in a PCB design.

In order for this to work, the LED references need to be D1, D2, D3, etc. and the resistor references need to be R1, R2, R3, etc. The numbers must also match.

**Before Matching**
![Before](images/before.png)

**After Matching**
![After](images/after.png)

## Usage

This runs on python 3.12.0.

To use this script, run the following command:

```bash
python match_resistor_to_led.py <input_file> <output_file>
```
