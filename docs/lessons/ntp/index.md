# Network Time Protocol (NTP)

## Part 1: Understanding Time Synchronization

### Why Do We Need NTP?

1. Computer clocks tend to drift over time
2. Different devices need to agree on the exact time for:
   - Coordinating events
   - Logging activities
   - Securing network communications
   - Scheduling tasks

### How NTP Works

#### Client-Server Model
   - Your device (client) asks specialized time servers (NTP servers) for the current time
   - The server responds with highly accurate time information
   - Your device adjusts its clock accordingly

#### Time Server Hierarchy
   - Level 0: Atomic clocks and GPS clocks (Stratum 0)
   - Level 1: Computers directly connected to Level 0 devices
   - Level 2: Computers that get time from Level 1

## Part 2: Basic NTP Communication

### The NTP Request Process
1. Your device sends a tiny message to an NTP server
2. The server adds its timestamp
3. Your device calculates the time difference, accounting for network delay
4. Your clock gets adjusted

### Understanding Time Formats
1. NTP uses seconds since January 1, 1900
2. Modern computers use seconds since:
   - January 1, 1970 (Unix time)
   - January 1, 2000 (Some embedded systems)
3. We need to convert between these formats

