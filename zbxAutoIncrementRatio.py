#!/usr/bin/python
# -*- coding: utf-8
#
# for monitoring auto increment ratio of mysql tables on zabbix
# Selman Birlik - 23.06.2020
# 
# Usage: 
#   $0 discovery <tables>
#	$0 get <auto_increment_ratio> [table_name]

import sys
import json
import MySQLdb
import itertools

db_host     = "127.0.0.1"
db_port     = 3306
db_user     = "$dbuser"
db_password = "$dbuserpassword"

class AutoIncrementRatio:
    def __init__(self, db_host, db_port, db_user, db_password):
        self.__connection = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db="sys")
        self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.__connection.close()

    def __select(self, sql):
        self.__cursor.execute(sql)

        field_names = [d[0] for d in self.__cursor.description]
        while True:
            rows = self.__cursor.fetchmany()
            if not rows: return
            for row in rows:
                yield dict(itertools.izip(field_names, row))

    def discovery_tables(self):
        return self.__select("""SELECT  `table_schema`,`table_name`
                                FROM `schema_auto_increment_columns`
                                ORDER BY `auto_increment_ratio` DESC
                                LIMIT 20;
        """)

    def get_auto_increment_ratio(self,table_schema,table_name):
        return self.__select("""SELECT `auto_increment_ratio` 
                                FROM `schema_auto_increment_columns` 
                                WHERE `table_schema` = '{0}'
                                AND `table_name`= '{1}' ;
        """.format(table_schema,table_name))


def print_help():
    print("\nUsage:\t%s discovery <tables>\n\t%s get <auto_increment_ratio> [table_name]\n" % (sys.argv[0], sys.argv[0]))

db_conn = AutoIncrementRatio(db_host, db_port, db_user, db_password)

if sys.argv[1] == 'discovery':
    discovery = {"data":[]}
    if sys.argv[2] == 'tables':
        for table in db_conn.discovery_tables():
            discovery["data"].append({"{#TABLESCHEMA}":table['table_schema'], "{#TABLENAME}":table['table_name']})
        print(json.dumps(discovery, indent=2, sort_keys=True))
        sys.exit(0)
    else:
        print_help()
        sys.exit(1)
elif sys.argv[1] == 'get':
    if len(sys.argv) <= 3:
        print_help()
        sys.exit(1)
    else:
        for ratio in db_conn.get_auto_increment_ratio(sys.argv[2],sys.argv[3]):
            ratio_result=float(ratio['auto_increment_ratio'])
            print(ratio_result)