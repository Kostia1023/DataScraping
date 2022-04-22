import scrapy


class InstituteItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class DepartmentItem(scrapy.Item):
    name = scrapy.Field()
    institute = scrapy.Field()
    link = scrapy.Field()


class ScientistItem(scrapy.Item):
    name = scrapy.Field()
    department = scrapy.Field()


class StaffItem(scrapy.Item):
    name = scrapy.Field()
    institute = scrapy.Field()