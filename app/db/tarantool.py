import tarantool

conn = tarantool.connect(host='tarantool', port=3301)
citizens_conn = conn.space('citizens')

