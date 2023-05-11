import os
import psycopg2

from dotenv import load_dotenv
from logger import logger


load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')


class DataBase:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                database=DATABASE
            )
        except psycopg2.Error as e:
            logger.error(f'Can`t establish connection to database: {e}')

        try:
            cursor = self.conn.cursor()
            with cursor as curs:
                curs.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        ID SERIAL PRIMARY KEY,
                        user_id INTEGER,
                        chat_id INTEGER,
                        rom TEXT,
                        version TEXT,
                        link TEXT
                    )
                ''')
                self.conn.commit()
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')


    def check_user(self, user_id):
        try:
            logger.info(f'[DB] Checking USER [{user_id}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT *
                    FROM users
                    WHERE user_id=%s
                ''', (user_id,))
                row = curs.fetchone()

            if row:
                logger.info(f'[DB] USER [{user_id}] exist')
                return True
            else:
                logger.info(f'[DB] USER [{user_id}] is new')
                return False
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def check_rom_exist(self, user_id, rom):
        try:
            logger.info(f'[DB] Checking existing ROM [{rom}] to USER [{user_id}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT *
                    FROM users
                    WHERE user_id=%s AND rom=%s
                ''', (user_id, rom))
                row = curs.fetchone()

            if row:
                return True
            else:
                return False
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def add_rom(self, user_id, chat_id, rom, version, link):
        try:
            logger.info(f'[DB] Adding ROM [{rom}] & VERSION [{version}] to USER [{user_id}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    INSERT INTO users (user_id, chat_id, rom, version, link)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (user_id, chat_id, rom, version, link))
                self.conn.commit()
            return True
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def update_version(self, user_id, rom, version, link):
        try:
            logger.info(f'[DB] Updating VERSION [{version}] to USER [{user_id}] for ROM [{rom}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    UPDATE users
                    SET version=%s, link=%s
                    WHERE user_id=%s AND rom=%s
                    VALUES (%s, %s, %s)
                ''', (version, link, user_id, rom))
                self.conn.commit()
            return True
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def delete_rom(self, user_id, rom):
        try:
            logger.info(f'[DB] Deleting ROM [{rom}] for USER [{user_id}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    DELETE FROM users
                    WHERE user_id = %s AND rom = %s
                ''', (user_id, rom))
                self.conn.commit()
            logger.info(f'[DB] ROM [{rom}] for USER [{user_id}] was deleted')
            return True
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def get_user_data(self, user_id):
        try:
            logger.info(f'[DB] Getting all ROMs for USER [{user_id}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT rom, version, link
                    FROM users
                    WHERE user_id = %s
                ''', (user_id,))
                result = curs.fetchall()
            return result
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def get_my_roms(self, user_id):
        try:
            logger.info(f'[DB] Getting unique ROMs for USER [{user_id}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT DISTINCT rom
                    FROM users
                    WHERE user_id = %s
                ''', (user_id,))
                result = curs.fetchall()
            return result
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def delete_user_data(self, user_id):
        try:
            logger.info(f'[DB] Deleting data for USER [{user_id}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    DELETE FROM users
                    WHERE user_id = %s
                ''', (user_id,))
                self.conn.commit()
            return True
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def get_users(self):
        try:
            logger.info(f'[DB] Getting all users')
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT DISTINCT user_id
                    FROM users
                ''')
                result = curs.fetchall()
            return result
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def get_user_chat_id(self, user_id):
        try:
            logger.info(f'[DB] Getting all users')
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT chat_id
                    FROM users
                    WHERE user_id=%s
                ''', (user_id,))
                result = curs.fetchone()
            return result
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False


    def get_user_rom_version(self, user_id, rom):
        try:
            logger.info(f'[DB] Getting VERSION for USER [{user_id}] & ROM [{rom}]')
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT version
                    FROM users
                    WHERE user_id=%s AND rom=%s
                ''', (user_id, rom))
                result = curs.fetchone()
            return result
        except psycopg2.Error as e:
            logger.error(f'[DB] {e}')
            return False
