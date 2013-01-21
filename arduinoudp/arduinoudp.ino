#include <SPI.h>         // needed for Arduino versions later than 0018
#include <Ethernet.h>
#include <EthernetUdp.h>         // UDP library from: bjoern@cs.stanford.edu 12/30/2008
#include <stdlib.h>


// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {  
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 23, 199);
byte remote[] = {192,168,23,29};
byte dnsip[] = {192,168,23,1};
byte gateway[] = {192,168,23,1};
byte subnet[] = {255,255,255,0};

unsigned int localPort = 8888;      // local port to listen on
unsigned int remotePort = 8888;


// buffers for receiving and sending data
//char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,
char  value[5];
char identity[] = "Machine01 ";
char valtype[] ="temp ";
//char  ReplyBuffer[] = "Machine01 +21.5C"; // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

void setup() {
  //For Serial enable that
  // Serial.begin(9600);
  // start the Ethernet and UDP:
  Ethernet.begin(mac,ip,dnsip,gateway,subnet);
  Udp.begin(localPort);

  Serial.begin(9600);
}

float kty(unsigned int port) {
         float temp              = 82;
         ADCSRA = 0x00;
         ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
         ADMUX = 0x00;
         ADMUX = (1<<REFS0);
         ADMUX |= port;   

         for (int i=0;i<=64;i++)
         {
                 ADCSRA|=(1<<ADSC);
                 while (ADCSRA & (1<<ADSC));
                 temp += (ADCL + ADCH*256);
         }

         temp /= 101;
         temp -= 256;
       return (temp);
 }

void loop() {
    char ReplyBuffer [100];
    ReplyBuffer[0] = '\0';
    dtostrf(kty(0),2,2,value);
    strcat(ReplyBuffer, identity);
    strcat(ReplyBuffer, valtype);
    strcat(ReplyBuffer, value);
    Serial.print("Package Sent: ");
    Serial.print(ReplyBuffer);
    Serial.print("\n");
    Udp.beginPacket(remote, remotePort);
    Udp.write(ReplyBuffer);
    Udp.endPacket();
    delay(10000);
}

