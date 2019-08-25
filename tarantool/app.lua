#!/usr/bin/env tarantool

local log = require('log')
local console = require('console')

box.cfg {
  listen = 3301;
}

if not box.space.citizens then
	box.schema.space.create('citizens', {format={ {name = 'id', type = 'string'}, {name = 'citizen_id', type = 'number'}, {name = 'town', type = 'string'}, {name = 'street', type = 'string'}, {name = 'building', type = 'string'}, {name = 'apartment', type = 'number'}, {name = 'name', type = 'string'}, {name = 'birth_date', type = 'string'}, {name = 'gender', type = 'string'}, {name = 'relatives', type = 'array'} }})
	box.space.citizens:create_index('primary', {type='tree', parts={1, 'string', 2, 'number'}})
end


function by_months(import_id)
  local v, t
  local lua_month_table = {['1'] = {}, ['2'] = {}, ['3'] = {}, ['4'] = {}, ['5'] = {}, ['6'] = {}, ['7'] = {},
  ['8'] = {}, ['9'] = {}, ['10'] = {}, ['11'] = {}, ['12'] = {}}
  for v, t in box.space.citizens:pairs(import_id, {iterator = "EQ"}) do
    local month = tostring(tonumber(t[8]:split('.')[2]))
    local citizen_id = tostring(t[2])
    local relatives = t[10]

    local rel_table = {}
    for count = 1,#relatives do
        rel_table = {[tostring(relatives[count])] = 1}
    end

    for key, val in pairs(rel_table) do
        if not lua_month_table[month][key] then
            lua_month_table[month][key] = val
        else
            lua_month_table[month][key] = tonumber(lua_month_table[month][key]) + tonumber(val)
        end
    end
  end
  return lua_month_table
end


function by_cities(import_id)
    local v, t
    local cities_table = {}
    for v, t in box.space.citizens:pairs(import_id, {iterator = "EQ"}) do
        local city = tostring(t[3])
        local age = t[8]
        if not cities_table[city] then
            cities_table[city] = {age}
        else
            table.insert(cities_table[city], age)
        end
    end
    return cities_table
end
