import json
import sys
import logging
import redis
import pymysql


# TODO 1
DB_HOST = "database-1.cluster-cducqy6ya2ge.us-east-1.rds.amazonaws.com" # Add DB end point
DB_USER = "admin" # Add your database user
DB_PASS = "UYJ%}yM%dI4)gVTx_MBSuB}gN?uz" # Add your database password
DB_NAME = "mp6" # Add your database name
DB_TABLE = "mp6data" # Add your table name
REDIS_URL = "redis://test.gobtxh.ng.0001.use1.cache.amazonaws.com:6379" # Add redis end point "redis://test.gobtxh.ng.0001.use1.cache.amazonaws.com:6379"

TTL = 60

class DB:
    def __init__(self, **params):
        params.setdefault("charset", "utf8mb4")
        params.setdefault("cursorclass", pymysql.cursors.DictCursor)

        self.mysql = pymysql.connect(**params)

    def query(self, sql):
        with self.mysql.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def record(self, sql, values):
        with self.mysql.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()

    def get_idx(self, table_name):
        with self.mysql.cursor() as cursor:
            cursor.execute(f"SELECT MAX(id) as id FROM {table_name}")
            idx = str(cursor.fetchone()['id'] + 1)
            return idx

    def insert(self, idx, data, table_name):
        with self.mysql.cursor() as cursor:
            hero = data["hero"]
            power = data["power"]
            name = data["name"]
            xp = data["xp"]
            color = data["color"]
            
            sql = f"INSERT INTO {table_name} (`id`, `hero`, `power`, `name`, `xp`, `color`) VALUES ('{idx}', '{hero}', '{power}', '{name}', '{xp}', '{color}')"
            cursor.execute(sql)
            self.mysql.commit()

 # TODO 2
# def read(use_cache, xps, Database, Cache):
#     # Implement Lazy Loading strategy
    
#     result = []
    
#     if use_cache: # Use cache
#       pass
#     else: # Do not use cache
        
#     return result

def read(use_cache, xps, Database, Cache):
    result = []
    if use_cache:  # Use cache
        pass
        # for xp in xps:
            # cache_key = f"xp:{xp}"
            # cached_row = Cache.get(cache_key)
            # if cached_row:
            #     result.append(json.loads(cached_row))
            # else:
            #     sql = f"SELECT * FROM {DB_TABLE} WHERE xp = {xp}"
            #     db_result = Database.query(sql)
            #     if db_result:
            #         Cache.set(cache_key, json.dumps(db_result[0]), ex=TTL)
            #         result.extend(db_result)
    else:  # Do not use cache
        for xp in xps:
            sql = f"SELECT * FROM {DB_TABLE} WHERE xp = {xp}"
            result.extend(Database.query(sql))
    return result
    
    
# TODO 3
def write(use_cache, sqls, Database, Cache):
    # Implement Write Through strategy
    
    if use_cache: # Use cache
       pass
    else: # Do not use cache
        pass

def lambda_handler(event, context):
    
    USE_CACHE = (event['USE_CACHE'] == "True")
    REQUEST = event['REQUEST']
    
    # Initialize database
    try:
        Database = DB(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        sys.exit()
        
    # Initialize cache
    Cache = redis.Redis.from_url(REDIS_URL)
    
    result = []
    if REQUEST == "read":
        # event["SQLS"] is a list of all xps for which you have to query the database or redis.
        result = read(USE_CACHE, event["SQLS"], Database, Cache)
        
    elif REQUEST == "write":
        # event["SQLS"] should be a list of jsons. You have to write these rows to the database.
        write(USE_CACHE, event["SQLS"], Database, Cache)
        result = "write success"
    
    
    return {
        'statusCode': 200,
        'body': result
    }