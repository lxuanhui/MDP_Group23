instructions = [['W', 0], ['Right', 1], ['W', 9], ['Left', 1], ['W', 2], ['180 Turn', 1], ['W', 0], ['Left', 1],
                ['W', 1], ['Left', 1], ['W', 6], ['Right', 1], ['W', 1], ['Right', 1], ['W', 0], ['180 Turn', 1],
                ['W', 6], ['Left', 1], ['W', 9], ['Right', 1], ['W', 1], ['Right', 1]]

for el in instructions:
    print(el)

import serial

# Define the list of commands to send to the STM
commands = [
    b'\x01',  # Command 1
    b'\x02',  # Command 2
    # ...
    b'\x0F',  # Command 15
]


# Define the callback function to handle incoming data from the STM
def handle_data(data):
    # Process the data received from the STM
    pass


# Open the UART port
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Loop over the list of commands
for command in commands:
    # Send the command over the UART port
    ser.write(command)

    # Wait for an acknowledgement from the STM
    ack = ser.read(1)
    while ack != b'\xAA':
        ack = ser.read(1)

    # Execute the callback function to handle any data from the STM
    handle_data(ser.read())

# Close the UART port
ser.close()
