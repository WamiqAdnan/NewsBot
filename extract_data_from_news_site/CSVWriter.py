from RPA.FileSystem import FileSystem
import csv
from extract_data_from_news_site.Logging import Logging as logging

class CSVWriter:
    def __init__(self, file_path, header):
        self.file_path = file_path
        self.file_system = FileSystem()
        self.write_header(header)

    def write_header(self, header):
        """Write the header to the CSV file if it does not exist."""
        try:
            # Check if file exists
            file_exists = self.file_system.does_file_exist(self.file_path)
            if not file_exists:
                with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
        except Exception as e:
            logging.error(f"Error writing header to CSV file: {e}")

    def write_row(self, row):
        """Write a single row to the CSV file."""
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row)
        except Exception as e:
            logging.error(f"Error writing to CSV file: {e}")

    def write_rows(self, rows):
        """Write multiple rows to the CSV file."""
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for row in rows:
                    writer.writerow(row)
        except Exception as e:
            logging.error(f"Error writing to CSV file: {e}")
