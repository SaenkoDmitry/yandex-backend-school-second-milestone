
# run docker container locally
docker run \
  --name mytarantool \
  -d -p 3301:3301 \
  -v /Users/ruasedi/docker/mytarantool:/var/lib/tarantool \
  tarantool/tarantool

# connect to docker container
docker exec -i -t mytarantool console

# create space citizens
box.schema.space.create('citizens', {format={ {name = 'id', type = 'string'}, {name = 'citizen_id', type = 'number'}, {name = 'town', type = 'string'}, {name = 'street', type = 'string'}, {name = 'building', type = 'string'}, {name = 'apartment', type = 'number'}, {name = 'name', type = 'string'}, {name = 'birth_date', type = 'string'}, {name = 'gender', type = 'string'}, {name = 'relatives', type = 'array'} }})

# create index
box.space.citizens:create_index('primary', {type='tree', parts={1, 'string', 2, 'number'}})
