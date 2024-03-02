# Chatroom-App

Chatroom Application implemented using python3 and socket programming.

## Prerequisites

Ensure python3 is installed in your machine to run the command line implementation.

You can download Python from the official website [here](https://www.python.org/downloads/).

## Command-line implementation

In many systems, using ports below `1024` requires superuser (sudo) privileges. This is a security feature to prevent non-privileged users from starting services that listen on well-known ports.

If you don't want to run the server with sudo privileges, you can use a port number greater than `1024`.Change the PORTS variable appropriately.

### Starting the server

![Starting_Server](img/start.png)

### Clients

`Client CC created.Messages sent`
![Client_Server](img/client1.png)

`Client Noni created.Messages sent`
![Client_Server](img/client2.png)

`Client Imposter created.Messages sent`
![Client_Server](img/client3.png)

### Main server receiving messages

`Messages being received`
![Main_Server](img/receiving_messages.png)

### Connections closed by clients

`Connections closed`
![Starting_Server](img/closed.png)

## Disclaimer

Host `0.0.0.0` will listen to all IP addresses.Listening on all interfaces could potentially expose your server to the internet (if it's connected), which could be a security risk if your server is not secured properly.

Always make sure to implement proper security measures when writing server software.
