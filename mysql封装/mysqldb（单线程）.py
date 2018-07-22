#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
不支持多线程；
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
        self.__conn = None
        self.__cur = None

    def __connect(self):
        self.__conn = self.__pool.connection()
        self.__cur = self.__conn.cursor()

    def __close(self):
        try:
            if self.__cur is not None:
                self.__cur.close()
                self.__cur = None

            if self.__conn is not None:
                self.__conn.close()
                self.__conn = None
        except Exception as ex:
            print(ex)

    def insert_by_proc(self, proc, *args):
        try:
            self.__connect()
            self.__cur.callproc(proc, args)
            self.__conn.commit()
        except Exception as ex:
            self.__conn.rollback()
            raise ex
        finally:
            self.__close()

    def update_by_proc(self, proc, *args):
        try:
            self.__connect()
            self.__cur.callproc(proc, args) if args else self.__cur.callproc(proc)
            self.__conn.commit()
        except Exception as ex:
            self.__conn.rollback()
            raise ex
        finally:
            self.__close()

    def select_by_proc(self, proc, one=False, *args):
        try:
            self.__connect()
            self.__cur.callproc(proc, *args) if args else self.__cur.callproc(proc)
            if one:
                return dict(zip([k[0] for k in self.__cur.description], self.__cur.fetchone()))
            else:
                return [dict(zip([k[0] for k in self.__cur.description], row)) for row in self.__cur.fetchall()]
        finally:
            self.__close()

    def select_by_sql(self, sql, one=False):
        try:
            self.__connect()
            self.__cur.execute(sql)
            if one:
                return dict(zip([k[0] for k in self.__cur.description], self.__cur.fetchone()))
            else:
                return [dict(zip([k[0] for k in self.__cur.description], row)) for row in self.__cur.fetchall()]
        finally:
            self.__close()

    def update_by_sql(self, sql):
        try:
            self.__connect()
            self.__cur.execute(sql)
            self.__conn.commit()
        except Exception as ex:
            self.__conn.rollback()
            raise ex
        finally:
            self.__close()
