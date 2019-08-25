import tarantool

conn = tarantool.connect(host='127.0.0.1', port=3301)
citizens_conn = conn.space('citizens')

