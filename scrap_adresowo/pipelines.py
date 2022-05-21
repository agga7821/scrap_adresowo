# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .models import session_maker, Apartment


class ScrapAdresowoPipeline:

    def __init__(self):
        self.session = session_maker()

    def __del__(self):
        self.session.close()

    def process_item(self, item, spider):
        item = ItemAdapter(item)
        self.process_apartment_item(item, spider)
        return item

    def process_apartment_item(self, item, spider):
        link = item.get("link")
        apartment = self.session.query(Apartment).filter(Apartment.link == link).one_or_none()
        if apartment:
            for key, value in item.asdict().items():
                setattr(apartment, key, value)
            self.session.commit()
        else:
            apartment = Apartment(**item.asdict())
            self.session.add(apartment)
            self.session.commit()
