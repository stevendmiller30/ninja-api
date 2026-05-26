from elasticsearch.dsl import Document, InnerDoc, Object, Text


class Person(InnerDoc):
    first_name = Text()
    last_name = Text()
    birth_date = Text()


class USSenator(Document):
    description = Text()
    term_end_date = Text()
    website = Text()
    state = Text()
    person = Object(Person)
    political_party = Text()
    phone_number = Text()

    class Index:
        name = "us_senator_alias"
