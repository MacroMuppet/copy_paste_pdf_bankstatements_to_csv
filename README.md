# Bank Statement to CSV Converter

This Python script converts copy-pasted bank statement transactions into a structured CSV file for easier analysis and tax preparation.

## Prerequisites

- Python 3.x
- pandas library (`pip install pandas`)

## Usage

1. Open your bank statement PDF and click and select your Post Date, Transaction Date, Amount, Balance, and Description Transactions from the PDF and copy them month-by-month into a 'paste.txt' file.
2. Make sure the `paste.txt` file is in the same directory as `script_csv.py`
3. Paste the transactions into `paste.txt` to the point where you want to end.
4. Run the script:
   ```bash
   python script_csv.py
   ```
5. The script will generate CSV file(s) in the same directory, with transactions grouped by month

## Input Format

The script expects transactions in the following format from your bank statement: 
   Post Date,Transaction Date,Amount,Balance,Description
