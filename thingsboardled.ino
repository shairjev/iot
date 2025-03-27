#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Lanith";
const char* password = "Lanith@21";
const char* mqtt_server = "demo.thingsboard.io";
const char* token = "00lyEO22bPI11Ovfb5mM";

WiFiClient espClient;
PubSubClient client(espClient);

bool ledState = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // Turn the LED off initially
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
     }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  if (String(topic).startsWith("v1/devices/me/rpc/request/")) {
    int requestId = String(topic).substring(26).toInt();
    if (message.indexOf("method") != -1) {
      if (message.indexOf("getState") != -1) {
        String responseTopic = "v1/devices/me/rpc/response/" + String(requestId);
        String response = "{\"ledState\":" + String(ledState ? "true" : "false") + "}";
        client.publish(responseTopic.c_str(), response.c_str());
      } else if (message.indexOf("setValue") != -1) {
        if (message.indexOf("true") != -1) {
          digitalWrite(LED_BUILTIN, LOW); // Turn the LED on
          ledState = true;
        } else {
          digitalWrite(LED_BUILTIN, HIGH); // Turn the LED off
          ledState = false;
        }
        String responseTopic = "v1/devices/me/rpc/response/" + String(requestId);
        client.publish(responseTopic.c_str(), "{\"success\":true}");
      }
    }
  }
}

void reconnect() {
  if (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client", token, NULL)) {
      Serial.println("connected");
      client.subscribe("v1/devices/me/rpc/request/+");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
