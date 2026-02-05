# Weather station on macOS

## Eclipse Mosquitto Broker + Python venv + Paho MQTT

The following are the steps how to setup the weather station project. 

1 Create and use a **Python virtual environment**(venv).
2 Install and run the **Eclipse Mosquitto** MQTT broker.
3 Use the **Paho MQTT** Python client library
4 Exchange basic messages between:
    4.1 three **subscribers** (listening), and
    4.2 one **publisher** (sending messages)
5 Experiment with **QoS levels** and **retained messages**[B in MQTT

## 1 Prerequisites
### 1.1 Install Homebrew
On macOS, the easiest way to install Mosquitto is with Homebrew.
Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, follow any instructions Homebrew prints (e.g., adding it to your PATH).
The verify:

```bash
brew --vision
```

### 1.2. Install Python3 (if needed)

Many macOs systems already have Python3, but you can also install it via Homebrew:

```bash
brew install python
```

Check:

```bash
python3 --version
```

You should see something like:

```text
Python 3.11.x
```

---
## 2. Clone or download this repository

You can either:

-**Clone with Git**:

```bash
git clone *******
cd  weatherstation
```

or
-**Download as ZIP** from GitHub, unzip it, and then in Terminal `cd` into the unzipped folder.

All the following commands assume you are inside the project folder.

---

## 3. Create and activate a virtual environment (venv)
A virtual environment keeps the Python packages for this project isolated.

### 3.1. Create the venv

```bash
python3 -m venv .venv
```

This creates a folder called '.venv' in the current directory.

### 3.2. Activate the venv (macOS / Linux style)

```bash
source .venv/bin/activate
```

If activation worked, your prompt should look similar to:

```text
(.venv) your-mac:~/path/to/mqtt-macos-tutorial user$
```

Whenever you see `(.venv)` at the beginning of your prompt, it means the virtual environment is active.

To **deactivate** it later, you can run:

```bash
deactivate
```

---
## 4. Install Python dependencies (Paho MQTT)
With the virtual environment **activated**, run:

```bash
pip3 install -r requirements.txt
```

This will install the [Paho MQTT](hppts://pypi.org/project/paho-mqtt) client library required by the example scripts.

You can verify:

```bash
pip3 list
```

You should see `paho-mqtt` in the list.
---

## 5. Install Eclipse Mosquitto MQTT broker (macOS via Homebrew)

Install Mosquitto with Homebrew:

```bash
brew install mosquitto
```

After installation, check it's avaiable:

```bash
mosquitto -h
```

You should see the help text.

---

## 6. Use the included Mosquitto config

From version 2.0 onward, Mosquitto is more restrictive by defaults.
To keep things imple for a local tutorial, this repo includes a minimal config file that:

- set per_llistener_settings to true.
- listens on port **1883**
- Doesn't allows **anonymous** local connections.
- password file link

The config file is in:

```text
broker/weatherstation.conf
```

```conf
per_listener_settings true
listener 1883
allow_anonymous false
password_file $path/authority.txt
```

## 7. set the username and password file
Create a file under broker directory, named authority.txt
Within **authority.txt**, set username:password in this format

The users and passwords are
ivy:test
sub1:test1
sub2:test2
sub3:test3

Afterwards, use mosquitto command to encrypt the password:

```bash
mosquitto_passwd -U authority.txt
```

## 8. Start the Mosquitto broker

From the **project root** (weatherstation), run:

```bash
mosquitto -c "$(pwd)/mosquitto/mosquitto.conf" -v
```

Explanation:
- `-c` tells Mosquitto which configuration file to use.
- `-v` enables **verbose** logging so you can see connections and messages.
- `$(pwd)` expands to the full path of the current directory.

You should now see Mosquitto output like:
```text
1767363071: mosquitto version 2.0.22 starting
1767363071: Config loaded from weatherstation.conf.
1767363071: Opening ipv6 listen socket on port 1883.
```

Leave this Terminal window **open**. The broker must keep running. 

---

## 9. Basic example: subscriber (listener)

Open a **new Terminal** window or tab.
Go to the project folder and activate the venv:

```bash
cd /path/to/weatherstation
source .venv/bin/activate
```

Then run the subscriber:

```bash
python src/subscriber.py temperature or visibility or windspeed
```

You should see something like:

```text
[SUBSCRIBER] Connected with result code 0
[SUBSCRIBER] Subscribed to topic:temperature
```

## 10. Basic example: publisher (sender)

Open **another Terminal** window or tab, go to the project folder, and activate the venv again:

```bash
cd /path/to/weatherstation
source .venv/bin/activate
python3 src/weather_publisher.py
```

You should see:

```text
[PUBLISHER] Connecting to broker at localhost:1883...
[PUBLISHER] Connected with result code 0
[PUBLISHER] publishing message: temperature is 26.28,windspped is 12.27, and visibility is 1373.05
[PUBLISHER] publishing message: temperature is 25.86,windspped is 13.48, and visibility is 1374.74
...
```

On the **subscriber** window, you should see:

```text
[SUBSCRIBER] Message received!
	Topic:temperature
	Payload:The temperature is 27.07 degree celsius
        QoS:0
        Retained:0        
[SUBSCRIBER] Message received!
	Topic:temperature
	Payload:The temperature is 27.43 degree celsius
        QoS:0
        Retained:0
...
```
---

## 11. QoS and retained examples

The basic example uses **QoS 0** and **non-retained** messages.

For example: temperature is QoS=0, retained=False, 
             the message will be sent at most once, it may be lost, but will be not sent again

When the **Qos=1** and **retained=False**.

For example: windspeed is QoS=1, retained=False,
             the message will be sent at least once, will not lost, but may duplicate

When the **QoS=0** and **retained=True**.

For example: visibility is Qos=0, retained=False,
             the last sent message will be sent if the subscriber disconnected and reconnected again. 


### 11.1 Run the QoS =1

In a Terminal with the virtual environment active:

```bash
python3 src/subscriber.py windspeed
```

Expected output (simplified):

```text
[SUBSCRIBER] Connected with result code 0
[SUBSCRIBER] Subscribed to topic:windspeed
[SUBSCRIBER] Message received!
	Topic:windspeed
	Payload:The wind speed is 66.31 m/s
	Qos:1
	Retained:0
[SUBSCRIBER] Message received!
	Topic:windspeed
	Payload:The wind speed is 61.33 m/s
	Qos:1
	Retained:0
```
Check the Terminal with the publisher:

Expected output (simplified):

```text
[PUBLISHER] Connecting to broker at localhost:1883...
[PUBLISHER] Connected with result code 0
[PUBLISHER] publishing message: temperature is 20.04, windspeed 66.31, and visibility is 1898.2
[PUBLISHER] publishing message: temperature is 19.67, windspeed is 61.33, and visibility is 1898.71
```

### 11.2 Run the retain=True

In a Terminal with the virtual environment active:

```bash
python3 src/subscriber.py visibility
```

Expected output (simplified):
```text
[SUBSCRIBER] Connected with result code 0
[SUBSCRIBER] Subscribed to topic:visibility
[SUBSCRIBER] Message received!
	Topic: visibility
	Payload: The visibility is 1965.19m
	Qos:0
	Retained:0
[SUBSCRIBER] Message received!
	Topic:visibility
	Payload:The visibility is 1964.56m
	Qos:0
	Retained:0
```

Stop the visibility subscriber by `Ctrl + C`, run the subscriber.py again

Expected output (simplified):
```text
[SUBSCRIBER] Connected with result code 0
[SUBSCRIBER] Subscribed to topic:visibility
[SUBSCRIBER] Message received!
	Topic:visibility
	Payload:The visibility is 1965.03m
	Qos:0
	Retained:1
```

Check the Terminal with publisher:

Expected output (simplified)

```text
[PUBLISHER] Connecting to broker at localhost:1883...
[PUBLISHER] Connected with result code 0
[PUBLISHER] publishing message: temperature is 9.73, windspeed is 20.88, and visibility is 1965.19
[PUBLISHER] publishing message: temperature is 10.16, windspeed is 25.0, and visibility is 1964.56
[PUBLISHER] publishing message: temperature is 10.73, windspeed is 23.75, and visibility is 1965.03
```
## 12. Stopping everything

- To stop the **publisher scripts**: go to their Terminal window and press `Ctrl + C`. 
- To stop the **subscriber scripts**: go to their Terminal window and press `Ctrl + C`.
- To stop the **broker** (Mosquitto): go to the broker Terminal window and press `Ctrl + C`.

## 13. Troubleshotting
**1. `ModuleNotFoundError: No module named 'paho'`**

- Make sure your **virtual environment is activated** (`(.venv)` visible in the prompt).
- Run:

  ```bash
  pip3 install -r requirements.txt
  ```
**2. `Connection Refused` error in Python clients**

- Check that Mosquitto is running and listening:
  - Is the broker Terminal open with no obvious errors?
  - Did you pass the correct path to `weatherstation.conf`?

- Confirm the broker is listening on port 1883 with this config:
  - `listener 1883`
  - `allow_anonymous false`

** 3. Port 1883 already in use**

- Maybe you have another MQTT broker or service using this port.
- You can change the port number in `weatherstation.conf`, e.g.:

  ```conf
  listener 1884
  allow_anonymous false
  ```

- Then update the Python scripts to use port `1884`.

---

## 14. How this example works

- The *weatherstation broker* is the *middleman* that receives and routes messages.
- The **subscriber** tells the broker:
  "I am interested in messages on topic `temperature` (or `windspeed`,or `visibility`)."
- The **publisher** sends message to the broker on that topic.
- The broker forwards those messages to any client subscribed to that topic. 

QoS levels change **how hard MQTT tries to deliver** a message:

- **QoS 0** - **at most once**: fire-and-forget, no acknowledgement.
- **QoS 1** - **at least once**: the broker will retry until it knows that client got it (can result in duplicates).
- **Qos 2** - **exactly once**: more expensive handshake to ensure no duplicates.

Retained messages let the broker remember the **last known value** for a topic and give it immediately to new subscribers.

This pattern is called **publish/subscribe**, and it's very popular in IoT and distributed systems. 



