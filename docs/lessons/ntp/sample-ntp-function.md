# NTP Function

Here is a step-by-step walk though of our NTP function in MicroPython

## Function Listing

```python
# Adapted from official ntptime by Peter Hinch July 2022
# The main aim is portability:
# Detects host device's epoch and returns time relative to that.
# Basic approach to local time: add offset in hours relative to UTC.
# Timeouts return a time of 0. These happen: caller should check for this.
# Replace socket timeout with select.poll as per docs:
# http://docs.micropython.org/en/latest/library/socket.html#socket.socket.settimeout

import socket
import struct
import select
from time import gmtime

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
# (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600 if gmtime(0)[0] == 2000 else 2208988800

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
host = "pool.ntp.org"

def time(hrs_offset=0):  # Local time offset in hrs relative to UTC
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    try:
        addr = socket.getaddrinfo(host, 123)[0][-1]
    except OSError:
        return 0
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    poller = select.poll()
    poller.register(s, select.POLLIN)
    try:
        s.sendto(NTP_QUERY, addr)
        if poller.poll(1000):  # time in milliseconds
            msg = s.recv(48)
            val = struct.unpack("!I", msg[40:44])[0]  # Can return 0
            return max(val - NTP_DELTA + hrs_offset * 3600, 0)
    except OSError:
        pass  # LAN error
    finally:
        s.close()
    return 0  # Timeout or LAN error occurred
```

Let's break down the key parts of this code.



```python
# Time difference constants
NTP_DELTA = 3155673600 if gmtime(0)[0] == 2000 else 2208988800
```
This line determines which epoch your device uses (2000 or 1970) and sets the correct conversion factor.

```python
# Create the NTP request packet
NTP_QUERY = bytearray(48)
NTP_QUERY[0] = 0x1B
```
This creates the special message format that NTP servers expect. The `0x1B` tells the server this is a time request.

```python
# Connect to NTP server
addr = socket.getaddrinfo(host, 123)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```
This code:
1. Looks up the NTP server address
2. Creates a UDP socket for communication
3. Port 123 is the standard NTP port

```python
# Send request and get response
s.sendto(NTP_QUERY, addr)
if poller.poll(1000):  # wait up to 1 second
    msg = s.recv(48)
    val = struct.unpack("!I", msg[40:44])[0]
```
This section:
1. Sends our time request
2. Waits for up to 1 second for a response
3. Extracts the timestamp from the response

## Part 4: Hands-on Exercise

Let's use this code to synchronize a clock:

1. Save the code as `ntp_sync.py`
2. Create a simple clock program:

```python
from machine import RTC
import ntp_sync

def sync_time():
    # Get time with UTC offset for your timezone
    # Example: -4 for EDT
    current_time = ntp_sync.time(-4)  
    if current_time > 0:
        # Convert to time tuple and set RTC
        rtc = RTC()
        rtc.datetime(gmtime(current_time))
        print("Time synchronized!")
    else:
        print("Time sync failed")

# Run the synchronization
sync_time()
```

## Part 5: Understanding Results

After running the code, you might see:
1. Success: Your device's time is now synchronized
2. Failure: Common causes include:
   - No internet connection
   - NTP server timeout
   - Network restrictions

Remember that in real applications, you should:
- Handle errors gracefully
- Implement periodic resynchronization
- Consider time zones and daylight saving time
- Add timeout handling for reliability

## References

[Peter Hinch NTP Function](https://github.com/peterhinch/micropython-samples/blob/master/ntptime/ntptime.py0