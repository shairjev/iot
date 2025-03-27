#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Lanith";
const char* password = "Lanith@21";
const char* mqtt_server = "demo.thingsboard.io";
const char* token = "00lyEO22bPI11Ovfb5mM";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client", token, NULL)) {
      Serial.println("connected");
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

  float h = random(20, 90); // Random humidity value between 20% and 90%
  float t = random(15, 35); // Random temperature value between 15°C and 35°C

  String payload = "{";
  payload += "\"temperature\":"; payload += t; payload += ",";
  payload += "\"humidity\":"; payload += h;
  payload += "}";

  Serial.print("Publishing payload: ");
  Serial.println(payload);

  client.publish("v1/devices/me/telemetry", (char*) payload.c_str());
  delay(2000);
}
