"""
Functionality added
"""

from yoyo import step

__depends__ = {'20221204_01_LUvn9', '20221205_01_5oCmi-initial'}

steps = [
    step("CREATE TABLE  Url (id INTEGER Primary key AUTOINCREMENT not null, long_url TEXT, short_url text, user_id INT, FOREIGN KEY (user_id)  REFERENCES User (user_id))")
]
