"""
Initial
"""

from yoyo import step

steps = [
    step("CREATE TABLE if not exists User (user_id INTEGER primary key AUTOINCREMENT not null, email TEXT, hashed_password text, is_active boolean)"),
    
]
