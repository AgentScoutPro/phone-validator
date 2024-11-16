# Phone Number Validator App

A Streamlit application that validates phone numbers and provides detailed information about them.

## Features

- Upload Excel files containing phone numbers for batch validation
- Manual entry and validation of individual phone numbers
- Validates international phone numbers
- Provides information about:
  - Number validity
  - Mobile/Landline detection
  - Carrier information
  - Geographic location
  - Timezone
- Export results to CSV

## Installation

1. Clone this repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run phone_validator_app.py
   ```

## Usage

### File Upload
1. Prepare an Excel file (.xlsx or .xls) containing phone numbers
2. Upload the file using the file uploader
3. Select the column containing phone numbers
4. Click "Validate Numbers"
5. Download results as CSV

### Manual Entry
1. Enter a phone number with country code (e.g., +1234567890)
2. Click "Validate"
3. View detailed results

## Requirements
- Python 3.9 or higher
- See requirements.txt for package dependencies
