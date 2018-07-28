
# Import standard python modules.
import sys

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '5f5fc6b5d6ec40f5a1f3ad6406342c83'
ADAFRUIT_IO_USERNAME = 'Ramkarde'
FEED_ID = 'relay1'
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID)
    client.subscribe('relay2')
    client.subscribe('relay3')
    client.subscribe('relay4')
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)
def message(client, feed_id, payload, retain):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if feed_id == 'relay1':
       if payload == 'ON':
          GPIO.output(relay1,True)
       if payload == 'OFF':
          GPIO.output(relay1,False)
    if feed_id == 'relay2':
       if payload == 'ON':
          GPIO.output(relay2,True)
       if payload == 'OFF':
          GPIO.output(relay2,False)
    if feed_id == 'relay1':
       if payload == 'ON':
          GPIO.output(relay1,True)
       if payload == 'OFF':
          GPIO.output(relay1,False)
# Create an MQTT client instance.
client2 = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client2.on_connect    = connected
client2.on_disconnect = disconnected
client2.on_message    = message
# Connect to the Adafruit IO server.
client2.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client2.loop_blocking()
