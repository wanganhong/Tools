#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
支持多线程；
每次实例化都获得不同的MysqlDB实例，且每个MysqlDB实例都对应不同PooledDB连接池，所以支持多个不同数据库的访问；
MysqlDB实例过多时，会存在问题
"""

import pymysql
from DBUtils.PooledDB import PooledDB


class MysqlDB(object):

    def __init__(self, host, port, user, passwd, db, charset='UTF8', mincached=5, maxconnections=5):
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
