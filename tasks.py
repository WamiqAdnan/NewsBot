from robocorp.tasks import task
import extract_data_from_news_site.util as util
import os
from extract_data_from_news_site.ExtractNews import ExtractNews
from extract_data_from_news_site.ImageDownloader import ImageDownloader
from extract_data_from_news_site.CSVWriter import CSVWriter
from RPA.Robocorp.WorkItems import WorkItems

@task
def extract_data_from_news_site():

    # Retrieve the work item data
    workitems =  WorkItems()
    input_data = workitems.get_work_item_payload()

    # define news site URL
    url = "https://www.latimes.com/"

    output_dir = "output"

    search_query = input_data["search_query"]

    category = input_data["category"]

    number_of_months = input_data["number_of_months"]

    number_of_months = 0 if number_of_months in [0, 1] else number_of_months - 1
    
    timestamp_to_stop = util.get_start_of_previous_month_timestamp(util.get_current_timestamp(), number_of_months) * 1000

    csv_path = f"{output_dir}/{search_query}_after_{util.get_formatted_date_from_timestamp_path(timestamp_to_stop / 1000)}.csv"

    image_output_dir = f"{output_dir}"
    
    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    header = ["title", "date", "description", "picture filename", "count of search phrase", "contains amount"]

    csv_writer = CSVWriter(csv_path, header)

    image_downloader = ImageDownloader(image_output_dir)

    automation = ExtractNews(url, image_downloader, csv_writer, timestamp_to_stop, category)

    automation.run(search_query)
