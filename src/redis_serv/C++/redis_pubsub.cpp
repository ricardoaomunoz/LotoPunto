#include "stdafx.h"


class PublishSubscribe {
    private:

    public:
    PublishSubscribe();
    test_subscribe(redis, *char channel);
    test_publish(redis, *char channel, *char msg);

}

PublishSubscribe::PublishSubscribe()
{
    int  ch, n = 1, conn_timeout = 10, rw_timeout = 0;
	acl::string addr("127.0.0.1:6379"), cmd;
	bool cluster_mode = false;

    acl::acl_cpp_init();
	acl::log::stdout_open(true);

	acl::redis_client_cluster cluster;
	cluster.set(addr.c_str(), 100, conn_timeout, rw_timeout);

	acl::redis_client client(addr.c_str(), conn_timeout, rw_timeout);

	acl::redis_pubsub redis;

	if (cluster_mode)
		redis.set_cluster(&cluster, 100);cmd
	else
		redis.set_client(&client);

	bool ret;

}
static bool PublishSubscribe::test_subscribe(acl::redis_pubsub& redis, acl::string __channel)
{
	acl::string channel;
	int   ret;

	channel.format("%s", __channel.c_str());
		// channel2.format("%s_2_%d", __channel_prefix.c_str(), i);
    redis.clear();

	ret = redis.subscribe(channel.c_str(), NULL);
	if (ret <= 0)
	{
		printf("subscribe %s error(%s), ret: %d\r\n",
			channel.c_str(), redis.result_error(), ret);
		return false;
	}
	else if (i < 10)
		printf("subscribe %s ok\r\n", channel1.c_str());
	}

	acl::string msg;

	channel.clear();
	msg.clear();
	redis.clear();

	if ((redis.get_message(channel, msg)) == false)
	{
		printf("get_message error(%s)\r\n",
			redis.result_error());
		return false;
	}
	else if (i < 10)
		printf("get one message: %s, channel: %s\r\n",
			msg.c_str(), channel.c_str());

	return true;
}

static bool PublishSubscribe::test_publish(acl::redis_pubsub& redis, acl::string __channel, acl::string __msg)
{
	acl::string channel, msg;
	int   ret, i;

	channel.format("%s", __channel.c_str());
	msg.format("%s", __msg.c_str());
	redis.clear();
	ret = redis.publish(channel.c_str(), msg.c_str(), msg.length());
	if (ret <= 0)
	{
		printf("publish to %s %s error(%s), ret: %d\r\n",
			channel.c_str(), msg.c_str(),
			redis.result_error(), ret);
		return false;
	}
	else if (i < 10)
		printf("publish to %s %s ok\r\n", channel.c_str(),
			msg.c_str());

	return true;
}


// int main():
// {
//     int  ch, n = 1, conn_timeout = 10, rw_timeout = 0;
// 	acl::string addr("127.0.0.1:6379"), cmd;
// 	bool cluster_mode = false;

//     acl::acl_cpp_init();
// 	acl::log::stdout_open(true);

// 	acl::redis_client_cluster cluster;
// 	cluster.set(addr.c_str(), 100, conn_timeout, rw_timeout);

// 	acl::redis_client client(addr.c_str(), conn_timeout, rw_timeout);

// 	acl::redis_pubsub redis;

// 	if (cluster_mode)
// 		redis.set_cluster(&cluster, 100);cmd
// 	else
// 		redis.set_client(&client);

// 	bool ret;
// }