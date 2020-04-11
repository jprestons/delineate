import socket
import struct
import sys
import textwrap


def serve():
    try:
        # Try to create a socket with the family of INET, streaming a raw socket, and UDP protocol.
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    except socket.error as msg:
        print ('Error code : ' + str(msg[0]) + ' Message' + msg[1])
        sys.exit()

    while True:
        # receive from buffer of 65565
        raw_data, address = s.recvfrom(65565)
        eth_proto, dest_mac, src_mac, data = etherframe(raw_data)
        print('\nEthernet Frame: ')
        print('Protocol: {}, Source: {}, Destination: {}'.format(src_mac, dest_mac, eth_proto))


def etherframe(data):
    # Using C Type format unpack the first 14 characters of the frame.
    dest_mac, src_mac, eth_proto = struct.unpack('!6s6sH', data[:14])
    return get_macadd(dest_mac), get_macadd(src_mac), socket.htons(eth_proto), data[14:]


def get_macadd(b_addr):
    b_str = map('{:02x}'.format, b_addr)
    return ':'.join(b_str).upper()


serve()
