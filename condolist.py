import math
import locators
from datetime import date, timedelta
from common import create_driver, get_beautiful_soup, write_csv, write_csv_with_headers


def get_list_of_pages(driver):
    driver.get(locators.HOMEPAGE_URL)
    property_cards = len(driver.find_elements_by_css_selector(locators.LIST_SELECTOR))
    property_count = int(driver.find_element_by_css_selector(locators.COUNT_SELECTOR).text)
    return math.ceil(property_count / property_cards)


def get_home_summary(home):
    url = home.select(locators.URL_SELECTOR)[0]['href']
    summary_section = home.select(locators.SUMMARY_SELECTOR)
    if len(summary_section) == 0:
        print('Could Not Find Summary Selector')
        return {}
    else:
        summary_section = home.select(locators.SUMMARY_SELECTOR)[0]
        summary = sanitize_row(get_summary_contents(summary_section))
        summary['URL'] = locators.BASE_URL + url
        return summary


def get_summary_contents(summary):
    contents = []
    for element in summary.contents:
        if not element.string:
            contents += get_summary_contents(element)
        else:
            contents.append(element.string)
    return contents


def sanitize_row(row):
    summary = {}
    for value in row:
        if is_maintenance(value):
            summary['Maintenance'] = int(sanitize_value(value))
        elif is_price(value):
            summary['Price'] = int(sanitize_value(value))
        elif is_posted_date(value):
            if 'day' in value:
                value = int(value.split(' ')[0])
            else:
                value = 0
            value = date.today() - timedelta(days=value)
            value = value.strftime("%b-%d-%Y")
            summary['Posted Date'] = value
        elif is_bedroom(value):
            value = sanitize_value(value)
            if '+' in value:
                room_count = value.split('+')[0]
                den_count = value.split('+')[1]
                value = int(room_count) + int(den_count) / 2
            elif value == 'Studio':
                value = 0
            summary['Bedrooms'] = value
        elif is_bathroom(value):
            summary['Bathrooms'] = int(sanitize_value(value))
        elif is_parking(value):
            summary['Parking'] = int(sanitize_value(value))
        elif is_size(value):
            value = sanitize_value(value)
            if '-' in value:
                if int(value.split('-')[0]) == 0:
                    value = int(value.split('-')[1])
                else:
                    value = int(value.split('-')[0])
            summary['Size'] = value
        elif is_address(value):
            if ' - ' in value:
                summary['Unit No.'] = value.split(' - ')[0]
                summary['Address'] = value.split(' - ')[1]
            else:
                summary['Address'] = value
    return summary


def sanitize_value(value):
    remove_values = ['$', ',', 'BD', 'BA', ' Parking', ' sqft', 'Maint. Fee ']
    for remove_value in remove_values:
        value = value.replace(remove_value, '')
    return value


def is_posted_date(value):
    for metric in ['minute', 'day', 'hour']:
        if metric in value:
            return True
    return False


def is_bedroom(value):
    for room_type in ['Studio', 'BD']:
        if room_type in value:
            return True
    return False


def is_address(value):
    street_types = ['Rd', 'St', 'Lane', 'Dr', 'Way', 'Ave', 'Quay', 'Gdns', 'Blvd', 'Pl', 'Cres', 'Sq', 'on', 'Crt', 'The', 'Terr']
    for street_type in street_types:
        if ' ' + street_type in value:
            return True
    return False


def is_bathroom(value):
    return 'BA' in value


def is_parking(value):
    return 'Parking' in value


def is_size(value):
    return 'sqft' in value


def is_maintenance(value):
    return 'Maint. Fee' in value


def is_price(value):
    return '$' in value


if __name__ == '__main__':
    header = ['Price', 'Posted Date', 'Unit No.', 'Address', 'Bedrooms', 'Bathrooms', 'Parking', 'Size', 'Maintenance', 'URL']
    driver = create_driver()
    page_count = get_list_of_pages(driver)
    unlisted_addresses = []
    property_urls = []
    for i in range(1, page_count + 1):
    # for i in range(1, 2):
        print('Page {} of {}'.format(i, page_count))
        page = locators.PROPERTY_PAGE_URL.format(i)
        soup = get_beautiful_soup(driver, page)
        homes = soup.select(locators.LIST_SELECTOR)
        for index, home in enumerate(homes):
            if len(home.select(locators.URL_SELECTOR)) > 0:
                property_urls.append(get_home_summary(home))
            else:
                home_address = home.select(locators.UNLISTED_ADDRESS_SELECTOR)[0]['alt']
                unlisted_addresses.append([home_address])
    write_csv('./unlisted.csv', unlisted_addresses)
    # write_csv('./urls.csv', property_urls)
    write_csv_with_headers('./urls.csv', property_urls, header)
    driver.quit()
