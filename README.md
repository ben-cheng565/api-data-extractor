# Unleashed API Data Extractor

This project is a tool for fetching and processing data from the Unleashed Software API. It handles communication with the API, parses and flattens the returned JSON data, and writes the results to CSV files.

## Setup

1. **Environment Variables**

   Create a `.env` file in the root directory of the project and include your API details:

   ```bash
   API_URL=your-api-url
   API_ID=your-api-id
   SECRET_KEY=your-secret-key
   ```

Replace `your-api-url`, `your-api-id`, and `your-secret-key` with your actual API details.

2. **Install Dependencies**

   This project requires the `requests`, `python-dotenv` and `datetime` libraries. You can install these with pip:

```bash
pip3 install requests python-dotenv datetime
```

## Usage

To run the project, execute `main.py`:

```bash
python main.py
```

## Structure

- `src/api/api_data.py`: Defines the ApiData class for handling API communication and data preparation.
- `src/utils/json_utils.py`: Provides utility functions for handling JSON data.
- `src/utils/file_utils.py`: Provides utility functions for handling files, including writing to CSV.
- `main.py`: Main script that uses the above modules to fetch, process, and write data.
