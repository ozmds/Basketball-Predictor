BASE_URL = 'https://condos.ca'
HOMEPAGE_URL = 'https://condos.ca/toronto/condos-for-sale?sale_price_range=100000%2C500000'
# PROPERTY_PAGE_URL = HOMEPAGE_URL + '?page={}'
PROPERTY_PAGE_URL = HOMEPAGE_URL + '&page={}'
LIST_SELECTOR = '#listRow > div'
COUNT_SELECTOR = '[for="listings"] h6 > div'

URL_SELECTOR = 'a'
SUMMARY_SELECTOR = 'a > div:nth-child(2)'
UNLISTED_ADDRESS_SELECTOR = 'img'

'''
&size_range=500%2C1500&parking_spots_min=1&maintenance_fee=0%2C500&beds=1-1%2C1.1-1.9%2C2-2
'''
