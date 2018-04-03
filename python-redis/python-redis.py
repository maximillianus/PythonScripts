import redis

# Ensure redis-server.exe is running

print('** Start python-redis script **')

r = redis.Redis(host = '127.0.0.1',
                port = 6379,
                password = '')
print('Available Keys:', r.keys('*'))

r.set('foo', 'bar')
value = r.get('foo').decode('utf-8')
print('value of "foo":',value)

# creating list 'mylist'
r.rpush('mylist', 'hello')
r.rpush('mylist', 'world')
listvalue = r.lrange('mylist', 0, -1)

# decode byte-value to unicode
listvalue = [t.decode('utf8') for t in listvalue]
print("printing list:", listvalue)

# deleting list 'mylist'
r.delete('mylist')
