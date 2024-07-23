import datetime

def get_formatted_date_from_timestamp(timestamp):
    """
    Convert a timestamp to a formatted date string.
    
    Args:
        timestamp (int): Unix timestamp in seconds.
        
    Returns:
        str: Formatted date string in "Month Day, Year" format.
    """
    # Convert the timestamp to a datetime object
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    
    # Format the datetime object to the desired string format
    formatted_date = dt_object.strftime("%B %d, %Y")
    
    return formatted_date

def get_formatted_date_from_timestamp_path(timestamp):
    """
    Convert a timestamp to a formatted date string.
    
    Args:
        timestamp (int): Unix timestamp in seconds.
        
    Returns:
        str: Formatted date string in "Month Day, Year" format.
    """
    # Convert the timestamp to a datetime object
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    
    # Format the datetime object to the desired string format
    formatted_date = dt_object.strftime("%B_%d_%Y")
    
    return formatted_date

def subtract_months(dt, months):
    """
    Subtract a specified number of months from a datetime object.
    
    Args:
        dt (datetime.datetime): Original datetime object.
        months (int): Number of months to subtract.
        
    Returns:
        datetime.datetime: New datetime object for the first day of the new month.
    """
    # Calculate the new month and year
    new_month = dt.month - months
    new_year = dt.year
    
    while new_month <= 0:
        new_month += 12
        new_year -= 1
    
    # Return a new datetime object for the first day of the new month
    return datetime.datetime(new_year, new_month, 1)

def get_start_of_previous_month_timestamp(timestamp, months=1):
    """
    Get the Unix timestamp for the start of the previous month.
    
    Args:
        timestamp (int): Unix timestamp in seconds.
        months (int): Number of months to subtract (default is 1).
        
    Returns:
        int: Unix timestamp for the start of the previous month.
    """
    # Convert the timestamp to a datetime object
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    
    # Subtract the given number of months from the current date
    start_of_previous_month = subtract_months(dt_object, months)
    
    # Convert the start of the previous month datetime object back to a timestamp
    start_of_previous_month_timestamp = start_of_previous_month.timestamp()
    return int(start_of_previous_month_timestamp)

def get_current_timestamp():
    """
    Get the current Unix timestamp in seconds.
    
    Returns:
        int: Current Unix timestamp in seconds.
    """
    # Get the current datetime
    now = datetime.datetime.now()
    
    # Convert the current datetime to a Unix timestamp (in seconds)
    current_timestamp_seconds = now.timestamp()
    
    return current_timestamp_seconds
