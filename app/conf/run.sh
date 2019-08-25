
# run docker container locally
sudo docker run \
  --name mytarantool \
  -v /home/entrant/tarantool:/var/lib/tarantool \
  -d -p 3301:3301 \
  tarantool/tarantool:1

# connect to docker container
sudo docker exec -i -t mytarantool console

# create space citizens
box.schema.space.create('citizens', {format={ {name = 'id', type = 'string'}, {name = 'citizen_id', type = 'number'}, {name = 'town', type = 'string'}, {name = 'street', type = 'string'}, {name = 'building', type = 'string'}, {name = 'apartment', type = 'number'}, {name = 'name', type = 'string'}, {name = 'birth_date', type = 'string'}, {name = 'gender', type = 'string'}, {name = 'relatives', type = 'array'} }})

# create index
box.space.citizens:create_index('primary', {type='tree', parts={1, 'string', 2, 'number'}})

# docker delete all <null> containers
docker rmi $(docker images -f "dangling=true" -q) --force

# docker run container
sudo docker run --name gift-store -it -p 8080:8080 dsaenko/yandex-backend-school-second-milestone:firsttry

sudo docker network create mynet
sudo docker run -d -p 3301:3301 --name tarantool --network='mynet' dsaenko/yandex-backend-school-second-milestone:tarantool
sudo docker run -d -p 8080:8080 --name web --network='mynet' dsaenko/yandex-backend-school-second-milestone:web
