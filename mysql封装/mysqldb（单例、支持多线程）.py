#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
支持多线程；
每次实例化都获得相同的MysqlDB对象和PooledDB连接池，所以无法在项目中访问多个不同的数据库。
"""

import threading

import pymysql
from DBUtils.PooledDB import PooledDB


class MysqlDB(object):
    __instance = None
    __pool = None
    __lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __init__(self, host, port, user, passwd, db, charset='UTF8', mincached=5, maxconnections=5):
        with self.__lock:
            if self.__pool is None:
                self.__pool = PooledDB(creator=pymysql,
                                       mincached=mincached, maxconnections=maxconnections, blocking=True,
                                       host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

    @staticmethod
    def __close(cur, conn):
        try:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        except Exception as ex:
            print(ex)

    def insert_by_proc(self, proc, *args):
        conn, cur = None, None
        try:
            conn = self.__pool.connection()
            cur = conn.cursor()
            cur.callproc(proc, args)
            conn.commit()
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            self.__close(cur, conn)

    def update_by_proc(self, proc, *args):
        conn, cur = None, None
        try:
            conn = self.__pool.connection()
            cur = conn.cursor()
            cur.callproc(proc, args) if args else cur.callproc(proc)
            conn.commit()
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            self.__close(cur, conn)

    def select_by_proc(self, proc, one=False, *args):
        conn, cur = None, None
        try:
            conn = self.__pool.connection()
            cur = conn.cursor()
            cur.callproc(proc, *args) if args else cur.callproc(proc)
            if one:
                return dict(zip([k[0] for k in cur.description], cur.fetchone()))
            else:
                return [dict(zip([k[0] for k in cur.description], row)) for row in cur.fetchall()]
        finally:
            self.__close(cur, conn)

    def select_by_sql(self, sql, one=False):
        conn, cur = None, None
        try:
            conn = self.__pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            if one:
                return dict(zip([k[0] for k in cur.description], cur.fetchone()))
            else:
                return [dict(zip([k[0] for k in cur.description], row)) for row in cur.fetchall()]
        finally:
            self.__close(cur, conn)

    def update_by_sql(self, sql):
        conn, cur = None, None
        try:
            conn = self.__pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            self.__close(cur, conn)
