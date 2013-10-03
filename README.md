jsonbot-wol-plug
================

Wake on Lan plug for jsonbot.
Jsonbot is used as a base for NURDbot, an IRC bot for our hackerspace called NURDspace.

The plug manages a list of hosts and their MAC addresses and can send WoL magic packets when given a listed hostname.

Commands
!wol <hostname>
!wol-add <hostname> <macaddress>
!wol-del <hostname>
!wol-hostlist
!wol-maclist
