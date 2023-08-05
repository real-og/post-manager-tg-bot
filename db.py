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

def add_code(code, channel_id, day_amount, all_post_number, tg_post_number):
    with Database() as curs:
        _SQL = f"""INSERT INTO access_codes (code, limit_count_all, limit_count_tg_link, limit_days, channel_id)
                    VALUES ('{code}', {all_post_number}, {tg_post_number}, {day_amount}, {channel_id});"""
        curs.execute(_SQL)

def get_code(code):
    with Database() as curs:
        _SQL = f"""SELECT * FROM access_codes WHERE code = '{code}';"""
        curs.execute(_SQL)
        return curs.fetchone()
    
def implement_usage_count_for_code(code, tg_link=False):
    with Database() as curs:
        _SQL = f"UPDATE access_codes SET usage_count = usage_count + 1 "
        if tg_link:
          _SQL += ", tg_link_usage_count = tg_link_usage_count + 1 "
        _SQL += f"WHERE code = '{code}'"
        curs.execute(_SQL)


def get_codes_and_channels(codes):
    with Database() as curs:
        code_values = ', '.join([f"'{code}'" for code in codes])
        _SQL = f""" SELECT * FROM channels
                             JOIN access_codes ON channels.channel_id = access_codes.channel_id
                             WHERE access_codes.code IN ({code_values});"""
        curs.execute(_SQL)
        return curs.fetchall()
    

def get_channel_name_by_id(id):
    with Database() as curs:
            _SQL = f"""SELECT * FROM channels WHERE channel_id = {id};"""
            curs.execute(_SQL)
            return curs.fetchone()

        
        
    
