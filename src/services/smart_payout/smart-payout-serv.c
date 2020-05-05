#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h> 
#include <sys/types.h> 
#include <sys/select.h>
#include <sys/socket.h> 
#include <sys/time.h>
#include <arpa/inet.h> 
#include <netinet/in.h> 
#include <signal.h>
  
#define CLIENT_PORT     8080 
#define SERVER_PORT     8081 
#define MAXLINE 1024 
// #define RASPBERRY 1

#ifdef RASPBERRY
#include "../../../../ITLSSPLinux.tar/ITLSSPLinux/inc/SSPComs.h"
#include "../../../../ITLSSPLinux.tar/ITLSSPLinux/BasicValidator6/port_linux.h"
#include "../../../../ITLSSPLinux.tar/ITLSSPLinux/BasicValidator6/ssp_helpers.h"
#else
#include "../../../ITLSSPLinux/inc/SSPComs.h"
#include "../../../ITLSSPLinux/BasicValidator6/port_linux.h"
#include "../../../ITLSSPLinux/BasicValidator6/ssp_helpers.h"
#endif


/* This is a UDP service that control de payout, the service wait for a command with a timeout 10 us
and send a message whe is necessary */
int hash_fuction(char *buff)
{
	int value_return;
	printf("Function buff : %s\n", buff);
	if (strcmp(buff, "UDP server up and listening") == 0)
	{
		value_return = 1;
	}
	else if (strcmp(buff, "--------") == 0)
	{
		value_return = 2;
	}
	else
	{
		value_return = 0;
	}
	return value_return;
	
	

}

void read_udp_message(int sockfd, struct sockaddr_in cliaddr, struct sockaddr_in servaddr)
{
    char buffer[MAXLINE];
	char msg[256];

    int len, n; 
  
    len = sizeof(cliaddr);  //len is value/resuslt 
	 
	while(1)
	{
		n = recvfrom(sockfd, (char *)buffer, MAXLINE,  
                MSG_WAITALL, ( struct sockaddr *) &cliaddr, 
                &len); 
		// printf("N : %d.\n.", n);
    	buffer[n] = '\0'; 
    	// printf("Client : %s\n", buffer);
		if (n != 16777215)
		{
			printf("Is a valid msg\n");
			printf("Client : %s.\n", buffer);
			/* There is a valid msg*/
			switch (hash_fuction(buffer))
			{
			case 1:
				printf("Primer Mesane\n");
				break;
			case 2:
				printf("Segundo mensaje\n");
				break;
			
			default:
				printf("Mensaje no encontrado\n");
				break;
			}
		}
		else
		{
			// printf("Mensaje no valido\n");
		}
		
		memset(buffer, 0, sizeof buffer);
		
		

	}
	

}

void start_pauout()
{

    SSP_COMMAND sspC;

	char *port_c = "/dev/ttyUSB0";
	int addr_c = 0;
	sspC.SSPAddress = (addr_c);
	// free(addr_c);

	init_lib();
	// Setup the SSP_COMMAND structure for the validator at ssp_address
	sspC.Timeout = 1000;
	sspC.EncryptionStatus = NO_ENCRYPTION;
	sspC.RetryLevel = 3;
	sspC.BaudRate = 9600;

}

int main()
{
    int sockfd; 
	
	char msg[256];
	SSP_POLL_DATA6 poll;
	SSP6_SETUP_REQUEST_DATA setup_req;
	unsigned int i = 0;
	struct sockaddr_in servaddr, cliaddr;
	struct timeval read_timeout;
	read_timeout.tv_sec = 0;
	read_timeout.tv_usec = 10; 
      
    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket creation failed"); 
        exit(EXIT_FAILURE); 
    } 
	setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &read_timeout, sizeof read_timeout);
     
      
    memset(&servaddr, 0, sizeof(servaddr)); 
    memset(&cliaddr, 0, sizeof(cliaddr));
	// Filling server information 
    servaddr.sin_family    = AF_INET; // IPv4 
    servaddr.sin_addr.s_addr = INADDR_ANY; 
    servaddr.sin_port = htons(CLIENT_PORT); 

    cliaddr.sin_family    = AF_INET; // IPv4 
    cliaddr.sin_addr.s_addr = INADDR_ANY; 
    cliaddr.sin_port = htons(SERVER_PORT); 

	if ( bind(sockfd, (const struct sockaddr *)&cliaddr,  
            sizeof(cliaddr)) < 0 ) 
    { 
        perror("bind failed"); 
        exit(EXIT_FAILURE); 
    }


    read_udp_message(sockfd, cliaddr, servaddr);
    
}