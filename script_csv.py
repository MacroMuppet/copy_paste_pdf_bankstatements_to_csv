import pandas as pd
import re
import os

def parse_bank_statement(file_path, output_dir='.'):
    """
    Parse a bank statement text file and convert it to a CSV file.
    
    Args:
    file_path (str): Path to the input text file
    output_dir (str): Directory to save the output CSV file
    """
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into lines and remove empty lines
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Initialize lists to store transaction data
    transactions = []
    
    # Regular expression to match transaction lines
    # This will help parse lines with varying formats
    transaction_pattern = re.compile(r'^(\d{2}-\d{2})\s*(?:(\d{2}-\d{2}))?\s*([-]?\d+(?:,\d{3})*\.\d{2})?\s*([-]?\d+(?:,\d{3})*\.\d{2})?\s*(.+)$')
    
    # Extract month and year from the transactions
    month_year_match = re.search(r'(\w+ \d{1,2}, \d{4}) to (\w+ \d{1,2}, \d{4})', content)
    
    # Default to using the first transaction's date if no statement date found
    if not month_year_match:
        # Look for the first transaction date
        first_date_match = re.search(r'^(\d{2})-(\d{2})', content)
        if first_date_match:
            month_num = first_date_match.group(1)
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            month_name = month_names[int(month_num) - 1]
            # Assume current year if not specified
            year = pd.Timestamp.now().year
            output_filename = f"{month_name}_{year}_transactions.csv"
        else:
            output_filename = "2020_2021_June_transactions.csv"
    else:
        # Parse the date range from the statement
        try:
            start_date = pd.to_datetime(month_year_match.group(1))
            output_filename = f"{start_date.strftime('%B')}_{start_date.year}_transactions.csv"
        except:
            output_filename = f"2020_2021_June_transactions.csv"
    
    # Process each line
    for line in lines:
        match = transaction_pattern.match(line)
        if match:
            # Unpack the matched groups
            post_date, trans_date, amount, balance, description = match.groups()
            
            # Clean up amount and balance (remove commas)
            amount = amount.replace(',', '') if amount else ''
            balance = balance.replace(',', '') if balance else ''
            
            # Create a transaction dictionary
            transaction = {
                'Post Date': post_date,
                'Transaction Date': trans_date or post_date,
                'Amount': amount,
                'Balance': balance,
                'Description': description
            }
            
            # Only add if it looks like a valid transaction
            if any([amount, balance]):
                transactions.append(transaction)
    
    # Create DataFrame
    df = pd.DataFrame(transactions)
    
    # Reorder columns
    df = df[['Post Date', 'Transaction Date', 'Amount', 'Balance', 'Description']]
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create full output path
    output_path = os.path.join(output_dir, output_filename)
    
    # Save to CSV using pandas
    df.to_csv(output_path, index=False)
    print(f"Transactions saved to {output_path}")
    
    return output_path

# Example usage
if __name__ == "__main__":
    input_file = 'paste.txt'  # Replace with your input file path
    parse_bank_statement(input_file)