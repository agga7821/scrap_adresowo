# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose
from w3lib.html import replace_escape_chars


def first_split_space(value):
    return value.split(' ')[0]


def from_second_split_space(value):
    try:
         return ' '.join(value.split(' ')[1:])
    except IndexError:  # missing value
        return ''


def is_direct(value):
    if value == 'Bez pośrednika':
        return True
    else:
        return False


def remove_spaces(value):
    return value.replace(' ', '')


def float_or_none(value):
    try:
        return float(value)
    except ValueError:
        return None


class ApartmentItem(scrapy.Item):
    city = scrapy.Field(input_processor=MapCompose(first_split_space))
    district = scrapy.Field(input_processor=MapCompose(from_second_split_space))
    property_type = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(remove_spaces, float_or_none))
    rooms = scrapy.Field(input_processor=MapCompose(int))
    floor = scrapy.Field(input_processor=MapCompose(int))
    squares = scrapy.Field(input_processor=MapCompose(int))
    directly = scrapy.Field(input_processor=MapCompose(is_direct))
    description = scrapy.Field(input_processor=MapCompose(str.strip, replace_escape_chars))
    price_per_square = scrapy.Field(input_processor=MapCompose(remove_spaces, float_or_none))
    address = scrapy.Field()
    link = scrapy.Field()




