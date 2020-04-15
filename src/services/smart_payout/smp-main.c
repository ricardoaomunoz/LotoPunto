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
// pase the validators response to the poll command. the SSP_POLL_DATA6 structure has an
// array of structures which contain values and country codes

int get_amount(char a)
{
	int amount = 0;
	switch (a)
	{
	case '1':
	{
		amount = 100000;
	}
	break;
	case '2':
	{
		amount = 200000;
	}
	break;
	case '3':
	{
		amount = 500000;
	}
	break;
	case '4':
	{
		amount = 1000000;
	}
	break;
	case '5':
	{
		amount = 2000000;
	}
	break;
	case '6':
	{
		amount = 5000000;
	}
	break;
	default:
		break;
	}
	return amount;


}


void do_action(SSP_COMMAND *sspC, int sockfd, struct sockaddr_in cliaddr, struct sockaddr_in servaddr)
{
	char buffer[MAXLINE];
	char msg[256];

    int len, n; 
  
    len = sizeof(cliaddr);  //len is value/resuslt 
	 

	n = recvfrom(sockfd, (char *)buffer, MAXLINE,  
                MSG_WAITALL, ( struct sockaddr *) &cliaddr, 
                &len); 
    buffer[n] = '\0'; 
    printf("Client : %s\n", buffer);


	// #####################################################3
	switch (buffer[0]) {
		
            
                
			case 'p':// Make a payout
			{
				int amount = 0;
				printf("buffer1: %d\n", buffer[1]);
				// printf("buffer1: %d\n", buffer[1]);
				amount = buffer[1] * 100000;
				// amount = get_amount(buffer[1]);
				
				printf("into p amount: %d \n", amount);
				// char *pay = "2000";
				// int amount = (int)(strtod(pay, NULL)*100);
				// // free(pay);
				// printf("into p");
				
				if (amount > 0) {
					// ask the user what currency to payout in
					// char *cc = ask(sspC, "Enter payout curency");
					char *cc = "COP";

					// send the payout command
					if (ssp6_payout(sspC, amount, cc, SSP6_OPTION_BYTE_DO) != SSP_RESPONSE_OK){

						printf("ERROR: Payout failed");
						// when the payout fails it should return 0xf5 0xNN, where 0xNN is an error code
						switch(sspC->ResponseData[1]) {
							case 0x01:
								snprintf(msg, sizeof msg, "Error: Not enough value in Smart Payout\n");
								printf(": Not enough value in Smart Payout\n");
								break;
							case 0x02:
								snprintf(msg, sizeof msg, "Error: Cant pay exact amount\n");
								printf(": Cant pay exact amount\n");
								break;
							case 0x03:
								snprintf(msg, sizeof msg, "Error: Smart Payout Busy\n");
								printf(": Smart Payout Busy\n");
								break;
							case 0x04:
								snprintf(msg, sizeof msg, "Error: Smart Payout Disabled\n");
								printf(": Smart Payout Disabled\n");
								break;
							default:
								printf("\n");
						}
					}
					// free(cc);
				} else {
					break;
				}
            }
            	break;

			case 'v': // get_value_level
			{
				int amount = 0;
				amount = get_amount(buffer[1]);
				
				if (amount > 0) {
					// ask the user what currency to payout in
					char *cc = "COP";

					// send the payout command
					if (ssp6_get_value_level(sspC, amount, cc) != SSP_RESPONSE_OK){

						printf("ERROR: get value level");
						snprintf(msg, sizeof msg, "Error: getting value level\n");
						
						// when the payout fails it should return 0xf5 0xNN, where 0xNN is an error code
						for (int i = 0; i<4; i++)
							printf("%d\n",sspC->ResponseData[i]);
						
					}
					else {
					printf("command ok");
					snprintf(msg, sizeof msg, "Value level: %d %d\n", amount, sspC->ResponseData[1]);
					printf("value level: %d %d\n",amount, sspC->ResponseData[1]);
	
				}
				} 

			}
			break;
            	
            case 'r': // reset the validator
            	if (ssp6_reset(sspC) != SSP_RESPONSE_OK){
					printf("ERROR: Reset failed\n");
					snprintf(msg, sizeof msg, "Error: Reset failed\n");
				}
            	break;
            	
            case 'e': // enable the validator (and un-inhibit every channel)
            {
   				SSP6_SETUP_REQUEST_DATA setup_req;
	            if (ssp6_enable(sspC) != SSP_RESPONSE_OK){
					printf("ERROR: Enable failed\n");
					snprintf(msg, sizeof msg, "Error: Enable failed\n");
					break;
				}

				// SMART Hopper requires diferent inhibit commands, so use setup request to see if it is an SH
				if (ssp6_setup_request(sspC, &setup_req) != SSP_RESPONSE_OK) {
			        printf("Setup Request Failed\n");
			        break;
			    }
				if (setup_req.UnitType == 0x03) {	
					unsigned int i;
			        // SMART Hopper requires different inhibit commands
	    		    for (i=0; i<setup_req.NumberOfChannels; i++){
        				ssp6_set_coinmech_inhibits(sspC, setup_req.ChannelData[i].value, setup_req.ChannelData[i].cc, ENABLED);
        			}
				} else {   
    				// set the inhibits (enable all note acceptance)
				    if (ssp6_set_inhibits(sspC,0xFF,0xFF) != SSP_RESPONSE_OK)
				    {
				        printf("Inhibits Failed\n");
			            break;
				    }
				}
			}
				break;
			case 'd': // disable the validator
	            if (ssp6_disable(sspC) != SSP_RESPONSE_OK){
					printf("ERROR: Disable failed\n");
					snprintf(msg, sizeof msg, "Error: Disable failed\n");
				}
				break;
			case 'E': // enable the payout device
			{
				SSP6_SETUP_REQUEST_DATA setup_req;
				// NV11 requires an option byte, so use a setup request to see if its an NV11
				if (ssp6_setup_request(sspC, &setup_req) != SSP_RESPONSE_OK) {
			        printf("Setup Request Failed\n");
			        break;
			    }
			    
			    // send the enable payout command
	            if (ssp6_enable_payout(sspC, setup_req.UnitType) != SSP_RESPONSE_OK){
					printf("ERROR: Enable Payout failed\n");
				}
			}
				break;
			case 'D': // disable the payout device
	            if (ssp6_disable_payout(sspC) != SSP_RESPONSE_OK){
					printf("ERROR: Disable Payout failed\n");
				}
				break;
				
			case 'c': // route a channel to the cashobox
			{
				char *cc = "COP";
				// ask the user what value to route to the cashbox
				// char *pay = ask(sspC, "Enter value to route to cashbox");
				int amount = get_amount(buffer[1]);
				
				// ask the user what currency this value is
				// cc = ask(sspC, "Enter curency");
	
				// send the route command
				if (ssp6_set_route(sspC, amount, cc, 0x01) != SSP_RESPONSE_OK){
					printf("ERROR: Route to cashbox failed\n");
					snprintf(msg, sizeof msg, "Error: Route to cashbox failed\n");
				}

            }
            	break;
            	
            case 's': // route a channel to storage (the payout device)
			{
				char *cc = "COP";
				// ask the user what value to route to storage
				// char *pay = ask(sspC, "Enter value to route to storage.");
				int amount = get_amount(buffer[1]);
				
				// ask the user what currency this value is
				// cc = ask(sspC, "Enter curency");

				
				// send the route command
				if (ssp6_set_route(sspC, amount, cc, 0x00) != SSP_RESPONSE_OK){
					printf("ERROR: Route to storage failed\n");
					snprintf(msg, sizeof msg, "Error: Route to storage failed\n");
				}

            }
            	break;
            	
            case 'n':// Payout next note (NV11 only)
            {
            	SSP6_SETUP_REQUEST_DATA setup_req;
            	// send a setup request to test if this is an NV11
				if (ssp6_setup_request(sspC, &setup_req) != SSP_RESPONSE_OK) {
			        printf("Setup Request Failed\n");
			        break;
			    }
			    if (setup_req.UnitType != 0x07) {
				    printf ("Payout next note is only valid for NV11\n");
	                break;
			    }
			    
			    // send the payout note command
			    if (ssp6_payout_note(sspC) != SSP_RESPONSE_OK) {
			        printf("Payout Note Failed\n");
			    }
			}
				break;
				
			case 'N':// Stack next note (NV11 only)
            {
            	SSP6_SETUP_REQUEST_DATA setup_req;
            	// send a setup request to test if this is an nv11
				if (ssp6_setup_request(sspC, &setup_req) != SSP_RESPONSE_OK) {
			        printf("Setup Request Failed\n");
			        break;
			    }
			    if (setup_req.UnitType != 0x07) {
				    printf ("Stack next note is only valid for NV11\n");
	                // print_help();
	                break;
			    }
			    
			    // send the stack note command
			    if (ssp6_stack_note(sspC) != SSP_RESPONSE_OK) {
			        printf("Stack Note Failed\n");
			    }
			}
				break;
			case 'h': // disable the payout device
			{
				snprintf(msg, sizeof msg, "no messages\n");
				printf("no messages");
			}
				
				break;
				
	}
	// printf("send msg.....");
	printf("msg from action: %s", msg);
	sendto(sockfd, (const char *)msg, strlen(msg), 
        MSG_CONFIRM, (const struct sockaddr *) &servaddr,  
            sizeof(servaddr));
	snprintf(msg, sizeof msg, "..");
	// #####################################################3

	
	
}
void parse_poll(SSP_COMMAND *sspC, SSP_POLL_DATA6 *poll, int sockfd, struct sockaddr_in servaddr)
{
	char msg[256]; 
	
	int i;
	for (i = 0; i < poll->event_count; ++i)
	{
		switch (poll->events[i].event)
		{
		case SSP_POLL_RESET:
			printf("Unit Reset\n");
			snprintf(msg, sizeof msg, "Warning: Unit Reset\n");
			// Make sure we are using ssp version 6
			if (ssp6_host_protocol(sspC, 0x06) != SSP_RESPONSE_OK)
			{
				snprintf(msg, sizeof msg, "Error: Host Protocol Failed\n");
				printf("Host Protocol Failed\n");
				return;
			}
			break;
		case SSP_POLL_READ:
			// the 'read' event contains 1 data value, which if >0 means a note has been validated and is in escrow
			if (poll->events[i].data1 > 0)
			{
				snprintf(msg, sizeof msg, "Warning: Note Read %ld %s\n", poll->events[i].data1, poll->events[i].cc);
				printf("Note Read %ld %s\n", poll->events[i].data1, poll->events[i].cc);
			}
			break;
		case SSP_POLL_CREDIT:
			// The note which was in escrow has been accepted
			
			snprintf(msg, sizeof msg, "Credit: %ld %s\n", poll->events[i].data1, poll->events[i].cc);
			printf("Credit %ld %s\n", poll->events[i].data1, poll->events[i].cc);
			break;
		case SSP_POLL_DISPENSED:
			snprintf(msg, sizeof msg, "Dispensed\n");
			printf("Dispensed\n");
			break;

		case SSP_POLL_INCOMPLETE_PAYOUT:
			// the validator shutdown during a payout, this event is reporting that some value remains to payout
			printf("Warning: Incomplete payout %ld of %ld %s\n", poll->events[i].data1, poll->events[i].data2, poll->events[i].cc);
			snprintf(msg, sizeof msg, "Warning: Incomplete payout %ld of %ld %s\n", poll->events[i].data1, poll->events[i].data2, poll->events[i].cc);
			break;
		case SSP_POLL_INCOMPLETE_FLOAT:
			// the validator shutdown during a float, this event is reporting that some value remains to float
			printf("Warning: Incomplete float %ld of %ld %s\n", poll->events[i].data1, poll->events[i].data2, poll->events[i].cc);
			snprintf(msg, sizeof msg, "Warning: Incomplete float %ld of %ld %s\n", poll->events[i].data1, poll->events[i].data2, poll->events[i].cc);
			break;
		case SSP_POLL_REJECTING:
			break;
		case SSP_POLL_REJECTED:
			// The note was rejected
			snprintf(msg, sizeof msg, "Warning: Note Rejected\n");
			printf("Warning: Note Rejected\n");
			break;
		case SSP_POLL_STACKING:
			break;
		case SSP_POLL_STORED:
			// The note has been stored in the payout unit
			snprintf(msg, sizeof msg, "Stored\n");
			printf("Stored\n");
			break;
		case SSP_POLL_STACKED:
			// The note has been stacked in the cashbox
			snprintf(msg, sizeof msg, "Stacked\n");
			
			printf("Stacked\n");
			break;
		case SSP_POLL_SAFE_JAM:
			snprintf(msg, sizeof msg, "Warning: Safe Jam\n");
			printf("Safe Jam\n");
			break;
		case SSP_POLL_UNSAFE_JAM:
			snprintf(msg, sizeof msg, "Warning: Unsafe Jam\n");
			printf("Unsafe Jam\n");
			break;
		case SSP_POLL_DISABLED:
			// The validator has been disabled
			snprintf(msg, sizeof msg, "DISABLED\n");
			printf("DISABLED\n");
			break;
		case SSP_POLL_FRAUD_ATTEMPT:
			// The validator has detected a fraud attempt
			snprintf(msg, sizeof msg, "Alert: Fraud Attempt %ld %s\n", poll->events[i].data1, poll->events[i].cc);
			printf("Fraud Attempt %ld %s\n", poll->events[i].data1, poll->events[i].cc);
			break;
		case SSP_POLL_STACKER_FULL:
			// The cashbox is full
			snprintf(msg, sizeof msg, "Alert: Stacker Full\n");
			printf("Stacker Full\n");
			break;
		case SSP_POLL_CASH_BOX_REMOVED:
			// The cashbox has been removed
			snprintf(msg, sizeof msg, "Alert: Cashbox Removed\n");
			printf("Cashbox Removed\n");
			break;
		case SSP_POLL_CASH_BOX_REPLACED:
			// The cashbox has been replaced
			snprintf(msg, sizeof msg, "Alert: Cashbox Replaced\n");
			printf("Cashbox Replaced\n");
			break;
		case SSP_POLL_CLEARED_FROM_FRONT:
			// A note was in the notepath at startup and has been cleared from the front of the validator
			snprintf(msg, sizeof msg, "Warning: Cleared from front\n");
			printf("Cleared from front\n");
			break;
		case SSP_POLL_CLEARED_INTO_CASHBOX:
			// A note was in the notepath at startup and has been cleared into the cashbox
			snprintf(msg, sizeof msg, "Warning: Cleared Into Cashbox\n");
			printf("Cleared Into Cashbox\n");
			break;
		case SSP_POLL_CALIBRATION_FAIL:
			// the hopper calibration has failed. An extra byte is available with an error code.
			snprintf(msg, sizeof msg, "Error: Calibration fail\n");
			printf("Calibration fail: ");

			switch (poll->events[i].data1)
			{
			case NO_FAILUE:
				printf("No failure\n");
			case SENSOR_FLAP:
				printf("Optical sensor flap\n");
			case SENSOR_EXIT:
				printf("Optical sensor exit\n");
			case SENSOR_COIL1:
				printf("Coil sensor 1\n");
			case SENSOR_COIL2:
				printf("Coil sensor 2\n");
			case NOT_INITIALISED:
				printf("Unit not initialised\n");
			case CHECKSUM_ERROR:
				printf("Data checksum error\n");
			case COMMAND_RECAL:
				printf("Recalibration by command required\n");
				ssp6_run_calibration(sspC);
			}
			break;
		}
		printf("msg from poll: %s", msg);
		sendto(sockfd, (const char *)msg, strlen(msg), 
        MSG_CONFIRM, (const struct sockaddr *) &servaddr,  
            sizeof(servaddr)); 
		snprintf(msg, sizeof msg, "..");
	}
	// return msg;
}

void run_validator(SSP_COMMAND *sspC)
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



	//check validator is present
	if (ssp6_sync(sspC) != SSP_RESPONSE_OK)
	{
		printf("NO VALIDATOR FOUND\n");
		snprintf(msg, sizeof msg, "Error: NO VALIDATOR FOUND\n");
		sendto(sockfd, (const char *)msg, strlen(msg), 
        MSG_CONFIRM, (const struct sockaddr *) &servaddr,  
            sizeof(servaddr));
		return;
	}
	printf("Validator Found\n");

	//try to setup encryption using the default key
	if (ssp6_setup_encryption(sspC, (unsigned long long)0x123456701234567LL) != SSP_RESPONSE_OK)
		printf("Encryption Failed\n");
	else
		printf("Encryption Setup\n");

	// Make sure we are using ssp version 6
	if (ssp6_host_protocol(sspC, 0x06) != SSP_RESPONSE_OK)
	{
		printf("Host Protocol Failed\n");
		return;
	}

	// Collect some information about the validator
	if (ssp6_setup_request(sspC, &setup_req) != SSP_RESPONSE_OK)
	{
		printf("Setup Request Failed\n");
		return;
	}
	printf("Firmware: %s\n", setup_req.FirmwareVersion);
	printf("Channels:\n");
	for (i = 0; i < setup_req.NumberOfChannels; i++)
	{
		printf("channel %d: %d %s\n", i + 1, setup_req.ChannelData[i].value, setup_req.ChannelData[i].cc);
	}

	//enable the validator
	if (ssp6_enable(sspC) != SSP_RESPONSE_OK)
	{
		printf("Enable Failed\n");
		return;
	}

	if (setup_req.UnitType == 0x03)
	{
		// SMART Hopper requires different inhibit commands
		for (i = 0; i < setup_req.NumberOfChannels; i++)
		{
			ssp6_set_coinmech_inhibits(sspC, setup_req.ChannelData[i].value, setup_req.ChannelData[i].cc, ENABLED);
		}
	}
	else
	{
		if (setup_req.UnitType == 0x06 || setup_req.UnitType == 0x07)
		{
			//enable the payout unit
			if (ssp6_enable_payout(sspC, setup_req.UnitType) != SSP_RESPONSE_OK)
			{
				printf("Enable Failed\n");
				return;
			}
		}

		// set the inhibits (enable all note acceptance)
		if (ssp6_set_inhibits(sspC, 0xFF, 0xFF) != SSP_RESPONSE_OK)
		{
			printf("Inhibits Failed\n");
			return;
		}
	}

	snprintf(msg, sizeof msg, "Start\n");
		sendto(sockfd, (const char *)msg, strlen(msg), 
        MSG_CONFIRM, (const struct sockaddr *) &servaddr,  
            sizeof(servaddr));
	while (1)
	{
		//poll the unit
		SSP_RESPONSE_ENUM rsp_status;
		if ((rsp_status = ssp6_poll(sspC, &poll)) != SSP_RESPONSE_OK)
		{
			if (rsp_status == SSP_RESPONSE_TIMEOUT)
			{
				// If the poll timed out, then give up
				snprintf(msg, sizeof msg, "Error: SSP Poll Timeout\n");
				sendto(sockfd, (const char *)msg, strlen(msg), 
        		MSG_CONFIRM, (const struct sockaddr *) &servaddr,  
        		    sizeof(servaddr));
				printf("SSP Poll Timeout\n");
				return;
			}
			else
			{
				if (rsp_status == 0xFA)
				{
					// The validator has responded with key not set, so we should try to negotiate one
					if (ssp6_setup_encryption(sspC, (unsigned long long)0x123456701234567LL) != SSP_RESPONSE_OK)
						printf("Encryption Failed\n");
					else
						printf("Encryption Setup\n");
				}
				else
				{
					snprintf(msg, sizeof msg, "Error: SSP Poll Error: 0x%x\n", rsp_status);
					sendto(sockfd, (const char *)msg, strlen(msg), 
        			MSG_CONFIRM, (const struct sockaddr *) &servaddr,  
        			    sizeof(servaddr));
					printf("SSP Poll Error: 0x%x\n", rsp_status);
				}
			}
		}

		// printf("doing parse...");
		parse_poll(sspC, &poll, sockfd, servaddr);
		// printf("doing action...");
		do_action(sspC, sockfd, cliaddr, servaddr);
		// printf("doing action...");
		// do_action(sspC);
		usleep(500000); //500 ms delay between polls
	}
}


int main()
{
	// int ssp_address;
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
	

	printf("##%s##\n", port_c);
	if (open_ssp_port(port_c) == 0)
	{
		// Do something with this error ##############
		printf("Port Error\n");
		return 1;
	}

	//run the validator

	run_validator(&sspC);

	// close the com port
	close_ssp_port();

	return 0;
}