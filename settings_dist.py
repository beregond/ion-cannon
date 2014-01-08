"""Config file."""

TEST = False

config = {
    # Port to listen, while recording requests.
    'port': '80',
    # Target to send recorded requests.
    'target': 'localhost',
    # Mongo db credentials, to store recorded requests.
    'mongo': {
        'host': 'localhost',
        'port': '27017',
        'dbname': '',
        'collection': '',
    },
    # Mongo db credentials for test purposes.
    'test_mongo': {
        'host': 'localhost',
        'port': '27017',
        'dbname': '',
        'collection': '',
    },
}
