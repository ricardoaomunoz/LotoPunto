#include "stdafx.h"
#include <iostream>
#include <stdio.h>
#include <unistd.h>

using namespace std;


class pareja {
   public:
      // Constructor
      acl::redis_pubsub redis;
      pareja();
      
      
      // Funciones miembro de la clase "pareja"
      bool test_subscribe(acl::string channel);
      bool test_publish(acl::string channel, acl::string msg);
   private:
      // Datos miembro de la clase "pareja"
      int a, b; 
};

pareja::pareja() {
   int conn_timeout = 10, rw_timeout = 0;
   acl::string addr("127.0.0.1:6379"), cmd;    
   acl::acl_cpp_init();
   acl::log::stdout_open(true);    
   acl::redis_client_cluster cluster;
   cluster.set(addr.c_str(), 100, conn_timeout, rw_timeout);   
   acl::redis_client client(addr.c_str(), conn_timeout, rw_timeout);
   redis.set_client(&client);
   // int ret;
   // ret = redis.subscribe("redis", NULL);
   //  if (ret <= 0)
   //  {
   //      printf("subscribe %s error(), ret: %d\r\n",
   //             redis.result_error(), ret);
   //    //   return false;
   //  }
   //  //else if (i < 10)
   //  printf("subscribe  ok\r\n");
}

bool pareja::test_subscribe(acl::string __channel) {
    printf("do it %s", __channel.c_str());
    acl::string channel;
    int ret;

    channel.format("%s", __channel.c_str());
    // channel2.format("%s_2_%d", __channel_prefix.c_str(), i);
    this->redis.clear();

    ret = redis.subscribe(channel.c_str(), NULL);
    printf("%d", ret);
   //  if (ret <= 0)
   //  {
   //      printf("subscribe %s error(%s), ret: %d\r\n",
   //             channel.c_str(), redis.result_error(), ret);
   //      return false;
   //  }
   //  //else if (i < 10)
   //  printf("subscribe %s ok\r\n", channel.c_str());

   //  acl::string msg;

   //  channel.clear();
   //  msg.clear();
   //  redis.clear();

   //  if ((redis.get_message(channel, msg)) == false)
   //  {
   //      printf("get_message error(%s)\r\n",
   //             redis.result_error());
   //      return false;
   //  }
   //  //else if (i < 10)
   //  printf("get one message: %s, channel: %s\r\n",
   //         msg.c_str(), channel.c_str());

    return true;
}

bool pareja::test_publish(acl::string __channel, acl::string __msg) {
    printf("do it %s %s", __channel.c_str(), __msg.c_str());
    acl::string channel, msg;
    int ret;

    channel.format("%s", __channel.c_str());
    msg.format("%s", __msg.c_str());
    redis.clear();
    ret = redis.publish(channel.c_str(), msg.c_str(), msg.length());
    printf("%d", ret);
   //  if (ret <= 0)
   //  {
   //      printf("publish to %s %s error(%s), ret: %d\r\n",
   //             channel.c_str(), msg.c_str(),
   //             redis.result_error(), ret);
   //      return false;
   //  }
   //  //else if (i < 10)
   //  printf("publish to %s %s ok\r\n", channel.c_str(),
   //         msg.c_str());

    return true;
}
void delay(int secs) {
  for(int i = (time(NULL) + secs); time(NULL) != i; time(NULL));
}


int main() {
   pareja par1;
   delay(1); 
   par1.test_subscribe("saldo");
   // par1.test_publish("saldo", "2000");
   // par1.Guarda("Dos", "tres");
   return true;
//    int x, y;
   
   // par1.Lee("dos");
//    cout << "Valor de par1.a: " << x << endl;
//    cout << "Valor de par1.b: " << y << endl;
   
   return 0;
}

// class publishsubscribe
// {
//     public:
//         acl::redis_pubsub redis;
//         publishsubscribe();
//         static bool test_subscribe(acl::redis_pubsub redis, acl::string channel);
//         static bool test_publish(acl::redis_pubsub redis, acl::string channel, acl::string msg);
// };

// publishsubscribe::publishsubscribe()
// {
//     int conn_timeout = 10, rw_timeout = 0;
//     acl::string addr("127.0.0.1:6379"), cmd;

//     acl::acl_cpp_init();
//     acl::log::stdout_open(true);

//     acl::redis_client_cluster cluster;
//     cluster.set(addr.c_str(), 100, conn_timeout, rw_timeout);

//     acl::redis_client client(addr.c_str(), conn_timeout, rw_timeout);
//     redis.set_client(&client);

// }

// static bool publishsubscribe::test_subscribe(acl::redis_pubsub &redis, acl::string __channel)
// {
//     acl::string channel;
//     int ret;

//     channel.format("%s", __channel.c_str());
//     // channel2.format("%s_2_%d", __channel_prefix.c_str(), i);
//     redis.clear();

//     ret = redis.subscribe(channel.c_str(), NULL);
//     if (ret <= 0)
//     {
//         printf("subscribe %s error(%s), ret: %d\r\n",
//                channel.c_str(), redis.result_error(), ret);
//         return false;
//     }
//     //else if (i < 10)
//     printf("subscribe %s ok\r\n", channel.c_str());

//     acl::string msg;

//     channel.clear();
//     msg.clear();
//     redis.clear();

//     if ((redis.get_message(channel, msg)) == false)
//     {
//         printf("get_message error(%s)\r\n",
//                redis.result_error());
//         return false;
//     }
//     //else if (i < 10)
//     printf("get one message: %s, channel: %s\r\n",
//            msg.c_str(), channel.c_str());

//     return true;
// }

// static bool publishsubscribe::test_publish(acl::redis_pubsub &redis, acl::string __channel, acl::string __msg)
// {
//     acl::string channel, msg;
//     int ret;

//     channel.format("%s", __channel.c_str());
//     msg.format("%s", __msg.c_str());
//     redis.clear();
//     ret = redis.publish(channel.c_str(), msg.c_str(), msg.length());
//     if (ret <= 0)
//     {
//         printf("publish to %s %s error(%s), ret: %d\r\n",
//                channel.c_str(), msg.c_str(),
//                redis.result_error(), ret);
//         return false;
//     }
//     //else if (i < 10)
//     printf("publish to %s %s ok\r\n", channel.c_str(),
//            msg.c_str());

//     return true;
// }

// int main()
// {
//     acl::redis_pubsub redis;
//     PublishSubscribe redis_cli();
//     static acl::string __channel("test_channel");
//     redis_cli.test_subscribe(redis, __channel);
// }