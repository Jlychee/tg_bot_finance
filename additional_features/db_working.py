import psycopg2
from additional_features.db_config import host, user, password, db_name


class DBConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            self.connection.autocommit = True
        except Exception as ex:
            print("[INFO]", ex)

    def __del__(self):
        self.connection.close()

    def check_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT * FROM users
                WHERE user_id = '{user_id}'
            """)
            user_data = cursor.fetchone()
            if user_data is None:
                return 0
            else:
                return [user_data[2], user_data[3]]

    def create_user(self, user_id, notion_token, page_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO users (user_id, notion_token, page_id)
                VALUES ('{user_id}', '{notion_token}', '{page_id}');
            """)

    def update_user(self, user_id, new_token, new_page_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT * FROM users
                WHERE user_id = '{user_id}'
            """)
            if cursor.fetchone() is not None:
                cursor.execute(f"""
                    UPDATE users
                    SET notion_token = '{new_token}', page_id = '{new_page_id}'
                    WHERE user_id = '{user_id}'
                """)
                return 1
            else:
                return 0
