from elasticsearch.dsl import Document, Text


class COBusinesses(Document):
    entity_id = Text()
    business_name = Text()
    status = Text()
    address_line1 = Text()
    address_line2 = Text()
    city = Text()
    state = Text()
    zip_code = Text()
    business_established_date = Text()

    class Index:
        name = "co_business_alias"
