### Monitoring auto_increment_ratio of MySQL tables by Zabbix 

# Overview

For Zabbix version: 3.x and higher

This template was tested on:

MySQL version 5.6, 5.7
Percona version 5.6, 5.7

Template has a discovery rule (Table Discovery) which include,
- an item prototype:
		MySQL {#TABLESCHEMA}:{#TABLENAME} auto increment ratio ) 
- two trigger prototypes:
		MySQL Table:  {#TABLESCHEMA}:{#TABLENAME} auto increment ratio is higher than 0.9 
		MySQL Table:  {#TABLESCHEMA}:{#TABLENAME} auto increment ratio is higher than 0.8) 

##  Setup

- Copy template_mysql_tables_auto_increment_ratio.conf into directory with Zabbix agent configuration (/etc/zabbix/zabbix_agentd.d/ by default). 
- Copy zbxAutoIncrementRatio.py script into /usr/local/bin directory. If you would like to copy to another directory you have to change directory path in template_mysql_tables_auto_increment_ratio.conf file. 
- Restart zabbix-agent.
- Create MySQL user for monitoring and grant limited privileges to user on 'sys' database.

## Zabbix configuration

- Import template: zbx_template_mysql_tables_auto_increment_ratio_exports.xml 

## Notes


Script discoveries the top 20 mysql tables. If you want to monitor auto-increment ratio for more tables you should change LIMIT value in discovery_tables function

		 def discovery_tables(self):
  			return self.__select("""SELECT  `table_schema`,`table_name`
                                FROM `schema_auto_increment_columns`
                                ORDER BY `auto_increment_ratio` DESC
                                LIMIT 20;
        """)

-----------
