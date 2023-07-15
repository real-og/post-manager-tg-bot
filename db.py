import psycopg2
import psycopg2.extras
from typing import List, Literal
import os
import json 
import datetime

class Database(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            database=str(os.environ.get('database')),
            user=str(os.environ.get('user')),
            password=str(os.environ.get('password')),
            host=str(os.environ.get('host')),
            port=str(os.environ.get('port'))
        )
        self.curs = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def __enter__(self):
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def get_channels():
    with Database() as curs:
        _SQL = f"""select * from channels;"""
        curs.execute(_SQL)
        return curs.fetchall()

def add_channel(id: int, name: str):
    with Database() as curs:
        _SQL = f"""INSERT INTO channels (channel_id, name) 
                 VALUES ({id}, '{name}') 
                 ON CONFLICT DO NOTHING;"""
        curs.execute(_SQL)

def delete_channel(id: int):
    with Database() as curs:
        _SQL = f"""DELETE FROM channels where channel_id = {id};"""
        curs.execute(_SQL)

def add_code(code, type, channel_id):
    with Database() as curs:
        _SQL = f"""INSERT INTO access_codes (code, usage_count, limit_count, channel_id)
                    VALUES ('{code}', 0, {type}, {channel_id});"""
        curs.execute(_SQL)
    
