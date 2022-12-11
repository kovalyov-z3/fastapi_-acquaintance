-- 
-- depends: 

CREATE TABLE User (user_id INT, email TEXT, hashed_password text, is_active boolean, PRIMARY KEY (id));
DROP TABLE USER;
CREATE TABLE  Url (id INT, long_url TEXT, short_url text, user_id INT, PRIMARY KEY (id), FOREIGN KEY(user_id)  REFERENCES User (user_id));
