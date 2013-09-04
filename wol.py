# jsb/plugs/myplugs/wol.py
#
# Author: The_Niz
#
""" wake up workstations and manage list of mac addresses """

## jsb imports
from jsb.lib.commands import cmnds
from jsb.lib.persist import PlugPersist

##basic imports
import socket
import struct

wol_list = PlugPersist('wol_list')

## defines

def sendwolpacket(send_data):
	#taken from http://code.activestate.com/recipes/358449-wake-on-lan/
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.sendto(send_data, ('<broadcast>', 7))

def sanitize_macaddress(macaddress):
	#taken from http://code.activestate.com/recipes/358449-wake-on-lan/
	# Check macaddress format and try to compensate.
	if len(macaddress) == 12:
		clean_macaddress = macaddress.upper()
	elif len(macaddress) == 12 + 5:
		sep = macaddress[2]
		clean_macaddress = macaddress.replace(sep, '').upper()
	else:
		pass
	
	return (clean_macaddress)

def construct_packet(clean_macaddress):
	#taken from http://code.activestate.com/recipes/358449-wake-on-lan/
	# Pad the synchronization stream.
	data = ''.join(['FFFFFFFFFFFF', clean_macaddress * 20])
	send_data = '' 

	# Split up the hex values and pack.
	for i in range(0, len(data), 2):
		send_data = ''.join([send_data,
			struct.pack('B', int(data[i: i + 2], 16))])

	return (send_data)

#wol command
def handle_wol(bot, ievent):
	""" Wake host by hostname, usage: !wol <hostname> """
	if not ievent.rest: ievent.missing('<hostname>') ; return
	input = ievent.rest
	splitted_input = input.split()
	hostinput = splitted_input[0]
	try: clean_macaddress = wol_list.data[hostinput]
	except: ievent.reply("cannot find host named " + hostinput) ; return
	try: send_data = construct_packet(clean_macaddress)
	except: ievent.reply("Exception occurred while constructing packet") ; return
	sendwolpacket(send_data)
	ievent.reply("sending WoL packet to " + clean_macaddress)

cmnds.add('wol', handle_wol, 'WOL')

#wol-add command
def handle_wol_add(bot, ievent):
	""" Add Host and macaddress, usage: !wol-add <hostname> <macaddress> , overwrites existing entries """
	if not ievent.rest: ievent.missing('<hostname> <macaddress>') ; return
	input = ievent.rest
	splitted_input = input.split()
	hostinput = splitted_input[0]
	macinput = splitted_input[1]
	try: clean_macaddress = sanitize_macaddress(macinput)
	except: ievent.reply("no valid macaddress given") ; return
	ievent.reply(clean_macaddress + " added for " + hostinput)
	wol_list.data[hostinput] = clean_macaddress
	wol_list.save()

cmnds.add('wol-add', handle_wol_add, 'WOL')

#wol-hostlist
def handle_wol_hostlist(bot, event):
	""" Shows list of saved hostnames """
	hosts = wol_list.data
	hostlist = ""
	for h, m in hosts.iteritems():
		hostlist = hostlist + h + " "
	event.reply("Known hosts: " + str(hostlist))
cmnds.add('wol-hostlist', handle_wol_hostlist, ["OPER", "USER", "GUEST", "WOL"])

#wol-maclist
def handle_wol_maclist(bot, event):
        """ Shows list of saved macaddresses """
        hosts = wol_list.data
        maclist = ""
        for h, m in hosts.iteritems():
                maclist = maclist + m + " "
        event.reply("Known macaddresses: " + str(maclist))
cmnds.add('wol-maclist', handle_wol_maclist, ["OPER", "USER", "GUEST", "WOL"])

#wol-del
def handle_wol_del(bot, ievent):
	""" Delete hostname from list, usage: !wol-del <hostname> """
	if not ievent.rest: ievent.missing('<hostname>') ; return
	input = ievent.rest
	splitted_input = input.split()
	hostinput = splitted_input[0]
	try:
		del wol_list.data[hostinput]
		wol_list.save()
	except: ievent.reply("no such host") ; return
	ievent.reply(hostinput + " removed")

cmnds.add('wol-del', handle_wol_del, 'WOL')
