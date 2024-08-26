# It ain't gotta be long to do damage.

# This program serves as a proof-of-concept, as its primary purpose is to demonstrate the ability to capture and
# analyze network traffic by sniffing packets and displaying their contents.

from scapy.all import sniff # Import the sniff function from the Scapy library. Use the sniff function as it is good
# when capturing packets from a network.

def packet_callback(packet): # Define the function 'packet_callback' and its one parameter, that being, 'packet.'
    # This function will be called when a packet is found and captured.
    print(packet.show()) # Print the Scapy method 'packet.show()' that prints a comprehensive overview of the packet's
    # contents, detailing all layers and their associated fields.
    # This function facilitates an in-depth analysis of the packet's underlying structure.

def raw_data_to_hex(raw_data):
    return raw_data.hex() # The hex() method creates a string of hexadecimal numbers from a byte object;
    # that 'bytes object' being 'packet.'

# Enter the raw data payload:
raw_data = b'...' # The "b'" prefix indicates a bytes object in Python that will start a string of byte
# literal characters.

# What I will do later is look into how a byte literal string can be converted into hexadecimal.

hex_rep = raw_data_to_hex(raw_data) # We want to see the hexadecimal representation of our data that is converted
# from the raw data detail of our packet.

def main(): # Define the main function which executes the entire script of this program.

    # If I wanted, could I add a filter to where I can filter for only TCP, UDP and Ethernet connections?

    bpf_filter = 'ip and (tcp or udp)'  # This code filters network traffic to extract IP packets that contain either
    # Transmission Control Protocol or User Datagram Protocol datab payloads. The term 'ip' is used to encompass the
    # entire Ethernet frame, as Ethernet serves as the layer 2 protocol that encapsulates IP packets.
    # bpf_filter = 'ether' # Ether or Ethernet frames are Ethernet frames are the fundamental data packet formatting
    # employed for communication between devices on the same local Ethernet network.


    # Include a specified filter to sniff specific packets
    sniff(prn=packet_callback, count=1, filter=bpf_filter) # Using the sniff function with the sniff function 'sniff(),'
    # that holds two arguments ('packet_callback' and 'count') prn assigned to the packet's callback of detailed
    # information, and 1 is assigned to the number of packets we want to capture.

    #*** Layer 2: The Data Link Layer within the OSI Model (that helps us understand the framework of network
    # communication systems) is responsible for governing node-to-node data
    # transmission, as well as implementing error detection and correction. This layer defines the protocols
    # for encapsulating data into frames and transferring them across a physical network infrastructure.

if __name__ == '__main__': # If the name of this program is called 'main' then call this main function to start
    # sniffing for packets.
    main()


