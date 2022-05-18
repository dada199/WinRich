# -*- coding:utf-8 -*-


import os
import sqlite3


class Cache:
    """

    """
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.isfile(self.file_name):
            self._create_file(self.file_name)

        self.conn = sqlite3.connect(self.file_name)
        self.cur = self.conn.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")

    def __del__(self):
        """ commit the change and close conn"""
        if getattr(self, 'conn', None):
            self.conn.commit()
            self.conn.close()

    def _create_file(self, cache_file):
        """ Create the table need to store the information"""
        conn = sqlite3.connect(cache_file)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_key = ON")
        cur.execute('''
            CREATE TABLE jobs(
                hash TEXT NOT NULL UNIQUE PRIMARY KEY, 
                description TEXT NOT NULL,
                last_run REAL, next_run REAL, 
                last_run_result INTEGER)''')

        cur.execute('''
            CREATE TABLE history(
                hash TEXT, 
                description TEXT, 
                time REAL, 
                result INTEGER,
                FOREIGN KEY(hash) REFERENCES jobs(hash))''')

        conn.commit()
        conn.close()

    def has(self, job):
        """ check if a job is exist in the table """
        return bool(self.cur.execute("SELECT count(*) FROM jobs WHERE hash=?", (job['id'], )))

    def get(self, id):
        """retrieves job with select id"""
        self.cur.execute("SELECT * FROM jobs WHERE hash=?", (id,))
        item = self.cur.fetchone()
        if item:
            return dict(zip(("id", "description", "last-run", "next-run", "last-run-result"), item))
        return None

    def update(self, job):
        self.cur.execute('''UPDATE jobs SET last_run=?,next_run=?,last_run_result=? WHERE hash=?''', (
            job["last-run"], job["next-run"], job["last-run-result"], job["id"]))



