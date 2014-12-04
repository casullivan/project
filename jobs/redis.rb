require "redis"
require 'json'
 
dashing_env = ENV['DASHING_ENV'] || 'development'
redis_config = YAML.load_file(File.dirname(__FILE__) + '/../config/redis.yml')
 
if redis_config[dashing_env].include? ":"
	t = redis_config[dashing_env].split(":")
	redis = Redis.new({:host => t[0], :port => t[1].to_i})
elsif redis_config[dashing_env][-5, 5] == ".sock"
	redis = Redis.new({ :path => redis_config[dashing_env] })
end

@tags = JSON.parse(redis.get('registry'))
 
SCHEDULER.every('2s', first_in: '1s') {
	info = redis.info
 
	send_event('redis_connected_clients', {
		current: info["connected_clients"],
		moreinfo: "Number of connected clients"
	})

	@tags.each do |item|
		@value = redis.get(item).to_i
		send_event(item, {
			#value: redis.get(item),
				value: @value,
				current: redis.get(item),
		title: redis.get(item),
		text: redis.get(item)
		})
		puts @value == 90
	end

	send_event('connected', {
		current: redis.get('opc_server'),
		text: redis.get('connected')
	})
	send_event('opc_server', {
		current: redis.get('opc_server'),
		title: redis.get('opc_server_name'),
		text: redis.get('opc_server')
	})
	send_event('plc', {
		current: redis.get('plc'),
		title: redis.get('opc_server_name'),
		text: redis.get('opc_server')
	})
 
	# Send memory usage stats in bytes
	send_event('redis_used_memory', {
		# Use peak memory as maximum in case no hard limit was defined in redis.conf
		max: [info["used_memory_peak"].to_i, redis.config("GET", "maxmemory")[1].to_i].max,
		value: info["used_memory"].to_i
	})
}