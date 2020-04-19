import psycopg2
from flask_login import UserMixin
from config import config


class Schema:

    def __init__(self):
        self.conn = psycopg2.connect(config['prod'].DATABASE_URI)
        self.curr = self.conn.cursor()
        self.create_users_table()
        self.create_items_table()

    def create_items_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS items (
        id SERIAL NOT NULL PRIMARY KEY,
        item TEXT,
        quantity INTEGER,
        is_bought BOOLEAN DEFAULT '0',
        is_deleted BOOLEAN DEFAULT '0',
        created_on DATE DEFAULT CURRENT_DATE,
        user_id VARCHAR(50),
        FOREIGN KEY (user_id) REFERENCES Users (id)
        );        
        """
        self.curr.execute(query)

    def create_users_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(50) NOT NULL PRIMARY KEY,
        name TEXT,
        email TEXT,
        avatar TEXT,
        is_inactive BOOLEAN DEFAULT '0',
        created_on DATE DEFAULT CURRENT_DATE
        );
        """
        self.curr.execute(query)

    def __del__(self):
        self.conn.commit()
        self.curr.close()
        self.conn.close()


class ShoppingModel:

    def __init__(self):
        self.conn = psycopg2.connect(config['prod'].DATABASE_URI)
        self.curr = self.conn.cursor()
        #self.conn.row_factory = psycopg2.Row

    def get_by_id(self,_id, uid):
        where_clause = f'AND id={_id}'
        return self.list_items(uid,where_clause)

    def create(self,item, quantity,user_id):
        print(item, quantity, user_id)
        self.curr.execute("INSERT INTO items (item, quantity, user_id) VALUES(%s,%s,%s) RETURNING id", (item,quantity,user_id))
        self.conn.commit()
        lastrowid = self.curr.fetchone()[0]
        return self.get_by_id(lastrowid,user_id)

    def delete(self, item_id,uid):
        self.curr.execute("UPDATE items SET is_deleted= %s WHERE user_id = %s AND id = %s", ('1', uid,item_id))
        self.conn.commit()
        return self.list_items(uid)

    def update(self, item_ids, uid):
        for item_id in item_ids:
            self.curr.execute("UPDATE items SET is_bought= %s WHERE id = %s AND user_id = %s",('1', item_id, uid))
        self.conn.commit()
        return self.list_items(uid)

    def list_items(self, uid, where_clause=""):
        self.curr.execute("SELECT id, quantity, item FROM items WHERE user_id= %s"
                                       " AND is_deleted != %s AND is_bought != %s "+ where_clause,
                                       (uid, '1', '1'))
        result_set = self.curr.fetchall()
        result = [{'id': row[0], 'quantity': row[1], 'item':row[2]}
                  for row in result_set]
        return result

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.curr.close()
        self.conn.close()

class UserModel:


    def __init__(self):
        self.conn = psycopg2.connect(config['prod'].DATABASE_URI)
        self.curr = self.conn.cursor()

    def create(self, id, name, email, avatar):
        self.curr.execute("INSERT INTO users(id, name, email, avatar) values (%s,%s,%s,%s)", (id, name, email, avatar))
        self.conn.commit()

    def select_by_id(self, uid):
        self.curr.execute("SELECT id, name, email, avatar FROM  users WHERE id = %s AND is_inactive = %s", (uid, '0'))
        result = self.curr.fetchall()
        if not result:
            return None
        else:
            return result[0]

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.curr.close()
        self.conn.close()


class User(UserMixin):

    def __init__(self,  _id, email, name, avatar):
        self.id = _id
        self.email = email
        self.name = name
        self.avatar = avatar

    @staticmethod
    def get(user_id):
        result = UserModel().select_by_id(user_id)
        if not result:
            return None
        else:
            user = User(
                _id=result[0],
                name=result[1],
                email=result[2],
                avatar=result[3])
        return user

    @staticmethod
    def create(_id, name, email, avatar):
        user = UserModel()
        user.create(_id, name, email, avatar)











