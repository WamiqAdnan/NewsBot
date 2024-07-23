import time

from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from extract_data_from_news_site.Logging import Logging as logging
import re
import extract_data_from_news_site.util as util

class ExtractNews:
    def __init__(self, url, image_downloader, csv_writer, timestamp_to_stop, category):
        self.browser = Selenium()
        self.url = url
        self.image_downloader = image_downloader
        self.csv_writer = csv_writer
        self.timestamp_to_stop = timestamp_to_stop
        self.category = category

    def open_browser(self):
        """Open the browser and navigate to the specified URL.

        This method opens the browser and navigates to the URL stored in 
        the instance variable `self.url`.
        """
        logging.info(f"Opening browser and navigating to {self.url}")
        self.browser.open_available_browser(self.url)

    def close_browser(self):
        self.browser.close_browser()

    def wait_and_click_button(self, button_locator):
        # Wait until button is visible and click
        self.browser.click_button_when_visible(button_locator)
    
    def wait_until_element_is_visible(self, element, timeout=10):
        """Wrapper to wait for element for custom timeout"""
        self.browser.wait_until_element_is_visible(element, timeout=timeout)

    def enter_text_in_field(self, field_locator, text):
        """Enter text into a field located by the given locator.

        Args:
            field_locator (str): The locator for the text field.
            text (str): The text to enter into the field.

        Returns:
            bool: True if the text was entered successfully, False otherwise.
        """
        try:
            # Enter text into the field
            logging.info(
                f"Waiting for the text field with locator '{field_locator}' to be visible"
            )
            self.wait_until_element_is_visible(field_locator)

            # Enter text into the field
            logging.info(
                f"Entering text '{text}' into the field with locator '{field_locator}'"
            )
            self.browser.input_text(field_locator, text)

        except Exception as e:
            logging.error(f"Error entering text in the field: {e}")
        
    def find_and_click_checkbox_by_text(self, ul_locator, text):
        """Find the checkbox next to a span element with the given text and click it."""
        try:
            # Wait until ul is visible
            self.wait_until_element_is_visible(ul_locator)

            # Locate the <ul> element with the ul_locator attribute
            ul_element = self.browser.find_element(ul_locator)
        
            # Find all <li> elements within the located <ul>
            list_items = ul_element.find_elements(By.CSS_SELECTOR, "li")
            
            for li in list_items:
                # Check for the <span> with the desired text within each <li>
                span = li.find_element(By.CSS_SELECTOR, "span")
                if span.text.strip() == text:
                    # Locate the checkbox input within the same <li>
                    checkbox = li.find_element(By.CSS_SELECTOR, "input.checkbox-input-element")
                    
                    # Click the checkbox if it is not already selected
                    if not checkbox.is_selected():
                        checkbox.click()
                        logging.info(f"Clicked checkbox for '{text}'")
                    else:
                        logging.info(f"Checkbox for '{text}' is already selected")
                    return
            
            
            logging.info(f"Span with text '{text}' not found within <ul> with '{ul_locator}'")
        except Exception as e:
            logging.info(f"Error interacting with the checkbox: {e}")

    def wait_until_page_contains_text(self, text):
        """Wait until the page contains the specified text."""
        self.browser.wait_until_page_contains(text)


    def find_and_click_select_by_text(self, select_locator, text):
        """Find the select accoriding to select_locator click it."""
        try:
            # Wait until select is visible
            self.wait_until_element_is_visible(select_locator)

            # Locate the <ul> element with the select_locator attribute
            ul_element = self.browser.find_element(select_locator)
        
            # Find all <li> elements within the located <ul>
            options = ul_element.find_elements(By.CSS_SELECTOR, "option")
            
            for option in options:
                if option.text.strip() == text:
                    
                    # Click the option if it is not already selected
                    if not option.is_selected():
                        option.click()
                        logging.info(f"Clicked option for '{text}'")
                    else:
                        logging.info(f"Option for '{text}' is already selected")
                    return
            
            
            logging.info(f"Option with text '{text}' not found within <select> with '{select_locator}'")
        except Exception as e:
            logging.info(f"Error interacting with the select: {e}")

    def check_selected_options(self, select_locator):
        """Check which options are selected in the select element."""
        try:
            # Wait until select is visible
            self.wait_until_element_is_visible(select_locator)

            select_element = self.browser.find_element(select_locator)
            select = Select(select_element)
            selected_options = select.all_selected_options
            selected_values = [option.get_attribute('value') for option in selected_options]
            selected_texts = [option.text for option in selected_options]

            if selected_values and selected_texts[0] == "Newest":
                return True
            logging.info(f"'Newest' sorting option selected")
        except Exception as e:
            logging.error(f"No select element found with locator '{e}'")
            return False
        
    def text_contains_currency(self, text):
        """
        Check if the string contains currency in the formats: $11.1, $111,111.11, 11 dollars, 11 USD
        """
        # Define a regex pattern to match the different currency formats
        currency_pattern = re.compile(r"""
            \$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?    # Matches $ followed by digits with optional commas and decimals
            |                                     # OR
            \b\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?\s*dollars\b  # Matches digits followed by 'dollars'
            |                                     # OR
            \b\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?\s*USD\b  # Matches digits followed by 'USD'
            """, re.VERBOSE | re.IGNORECASE)  # Verbose mode for readability, ignore case for 'dollars' and 'USD'
        
        # Search for the pattern in the text
        match = currency_pattern.search(text)
        
        # Return True if a match is found, otherwise False
        return bool(match)
    
    def click_next_button_if_possible(self, locator):
        """Find the element according to locator click it."""
        # Wait until element is visible
        self.wait_until_element_is_visible(locator)

        element = self.browser.find_element(locator)
        element_svg = element.find_element(By.CSS_SELECTOR, "svg")
        is_active = element_svg.get_attribute("data-inactive")

        if is_active is None:
            # Find element and click it 
            self.browser.click_element_when_clickable(locator)
            return True
        return False
        

    def fetch_all_news_on_current_page(self, ul_locator, page, search_query):
        """Find the select according to select_locator click it."""
        try:

            # Wait until select is visible
            self.wait_until_element_is_visible(ul_locator)

            # Locate the <ul> element with the ul_locator attribute
            ul_element = self.browser.find_element(ul_locator)
        
            # Find all <li> elements within the located <ul>
            list_items = ul_element.find_elements(By.CSS_SELECTOR, "li")
        
            image_src_paths = []
            rows = []
            completed = False

            for i, news in enumerate(list_items):

                # Getting timestamp of news
                timestamp_p = news.find_element(By.CLASS_NAME, "promo-timestamp")
                timestamp = int(timestamp_p.get_attribute("data-timestamp"))

                if timestamp < self.timestamp_to_stop:
                    completed = True
                    break

                # Getting title of news
                title_heading = news.find_element(By.CLASS_NAME, "promo-title")
                title_a =  title_heading.find_element(By.CSS_SELECTOR, "a")
                title = title_a.text.strip()

                # Getting description of news
                description_p = news.find_element(By.CLASS_NAME, "promo-description")
                description = description_p.text.strip()

                # Getting image of news
                image_img = news.find_element(By.CLASS_NAME, "image")
                image_src = image_img.get_attribute("src")

                # Calculate count of search phrase in description and sentence
                count = title.lower().count(search_query.lower()) + description.lower().count(search_query.lower())

                file_name = f"{search_query}_after_{util.get_formatted_date_from_timestamp_path(self.timestamp_to_stop / 1000)}_{page}_{i+1}.{image_src.split('.')[-1]}"

                image_src_paths.append((image_src, file_name))

                contains_amount = self.text_contains_currency(title + description)

                ["title", "date", "description", "picture filename", "count of search phrase", "contains amount"]
                rows.append([title, util.get_formatted_date_from_timestamp(timestamp/1000), description, file_name, count, contains_amount])

            if list_items:
                # Locate next page button using CSS class
                next_button_locator = "css:.search-results-module-next-page"

                # Find next_button_locator and click it
                if not self.click_next_button_if_possible(next_button_locator):
                    return True
                

            self.image_downloader.download_images_in_parallel(image_src_paths)
            self.csv_writer.write_rows(rows)

            return completed

        except Exception as e:
            logging.error(f"Error fetching news: {e}")


    def run(self, search_query):
        try:

            # Open the browser and navigate to the web page
            self.open_browser()

            # Locate search button using CSS selector
            search_button_locator = "css:button[data-element='search-button']"

            # Wait until search button is visible and click
            self.wait_and_click_button(search_button_locator)

            # Locate search field using CSS selector
            search_field_locator = "css:input[data-element='search-form-input']"

            # Locate and enter text in search field
            self.enter_text_in_field(search_field_locator, search_query)

            # Locate search submit button using CSS selector
            search__submit_button_locator = "css:button[data-element='search-submit-button']"

            # Wait until search submit button is visible and click
            self.wait_and_click_button(search__submit_button_locator)

            # Locate news category ul using CSS selector
            category_ul_locator = "css:ul[data-name='Type']"

            # Find and click checkbox with text Newsletter
            self.find_and_click_checkbox_by_text(category_ul_locator, self.category)

            # Wait until the filter is selected and page is loaded
            self.wait_until_page_contains_text("Selected Filters")

            time.sleep(5)

            # Sort option can be oldest as well
            sort_option = "Newest"

            # Locate sort select using CSS selector
            sort_select_locator = "css:select[name='s']"

            # Find and click option with text Newest
            self.find_and_click_select_by_text(sort_select_locator, sort_option)

            
            # if self.check_selected_options(sort_select_locator):

            # Locate news ul using CSS class
            news_ul_locator = "css:.search-results-module-results-menu"

            # Refresh to be safe
            # self.browser.driver.refresh()

            time.sleep(5)
            
            page = 1

            # Fetch all news on current page
            while not self.fetch_all_news_on_current_page(news_ul_locator, page, search_query):
                page += 1

            
        except Exception as e:
            logging.error(e)
        finally:
            self.close_browser()

