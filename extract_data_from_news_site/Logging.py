import logging as Logging

# Configure logging
Logging.basicConfig(
    level=Logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        # logging.StreamHandler(),  # Output logs to the console
        Logging.FileHandler('output/ExtractNews.log')  # Output logs to a file
    ]
)