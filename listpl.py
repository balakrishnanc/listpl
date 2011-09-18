#!/usr/bin/env python
# encoding: utf-8
## ------------------------------
# listpl.py
# 
# Created by Balakrishnan Chandrasekaran on 2011-09-18 16:39 -0400.
# Copyright (c) 2011 Balakrishnan Chandrasekaran <balac@cs.duke.edu>.
# All rights reserved.
# 
# This file is part of listpl.  
# 
# listpl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# listpl is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with listpl.  If not, see <http://www.gnu.org/licenses/>.
## ------------------------------
"""
listpl.py
Lists all PlanetLab nodes and their associated location information.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@cs.duke.edu>'
__version__ = '1.0'
__license__ = 'GPL v3'


import sys
# reject if not Python 2.x!
if not sys.version_info < (3, 0):
    sys.exit('Error: Requires Python 2.x!')


import codecs
from optparse import OptionParser
import os
import socket
import time
import xmlrpclib as rpc


# PlanetLab RPC API URL
_PL_RPC_URL_ = 'https://www.planet-lab.org/PLCAPI/'

# authentication credentials
_AUTH_CREDS_ = {'AuthMethod': 'anonymous', 'Role': 'user'}

# required list of data on PlanetLab sites
_REQ_SITE_DATA_ = ('site_id', 'name', 'longitude', 'latitude', 'node_ids')
# required list of data on PlanetLab nodes
_REQ_NODE_DATA_ = ('node_id', 'hostname')


# output file name where PlanetLab nodes and associated data is dumped
_TIME_FMT_ = '%m%d%Y-%H%M'
_OUT_FILE_ = ("pl-nodes-%s.txt" % time.strftime(_TIME_FMT_, time.localtime()))

# output record format - 
# <site id>, <site name>, <node_id>, <hostname>, <IP>, <latitude>, <longitude>
_OUT_DATA_FMT_ = '%6d, %60s, %6d, %40s, %15s, %12.8f, %12.8f \n'


def __getPlanetLabNodeList(out):
    """__getPlanetLabNodeList(out) - retrieves the list of PlanetLab nodes and
    associated information using the PLC API.
    """
    try:
        plc = rpc.ServerProxy(_PL_RPC_URL_)
        
        # retrieve a list of all sites
        # NOTE:
        # It doesn't matter if the site is up or not!
        sites = plc.GetSites(_AUTH_CREDS_, '*', _REQ_SITE_DATA_)
        
        # for each site, retrieve the node IPs
        for site in sites:
            node_ids = site['node_ids']
            
            if not len(node_ids) > 0:
                # No nodes in the site!
                # (perhaps disabled or currently down or newly created?)
                continue
            
            # retrieve details on the nodes at the site
            nodes = plc.GetNodes(_AUTH_CREDS_, node_ids, _REQ_NODE_DATA_)
            
            site_id = site['site_id']
            site_name = site['name']
            site_lon = site['longitude']
            site_lat = site['latitude']
            
            for node in nodes:
                node_id = node['node_id']
                node_host = node['hostname']
                
                # resolve hostname, if possible
                try:
                    node_ip = socket.gethostbyname(node_host)
                except socket.gaierror as e:
                    node_ip = node_host
                
                out.write(_OUT_DATA_FMT_ % (site_id, site_name, 
                                            node_id, node_host, node_ip, 
                                            site_lat, site_lon))
    except Exception as e:
        __die(e)


def __configOptParser ():
    """ __configOptParser () - configures the options' parser and returns the
    parser.
    """
    usage = ("usage: %prog [options] ")
    opt_parser = OptionParser(version = '%prog 1.0', usage = usage)
    
    opt_parser.add_option('-o', '--output',
                          help = 'absolute/relative path for output file', 
                          default = '.',
                          dest = 'out_path')
    
    return opt_parser


def __die(msg):
    """__die(msg) - display error message on STDERR and exit with an error code.
    """
    sys.stderr.write("Error: %s\n" % (msg))
    sys.exit(1)



if __name__ == '__main__':
    opt_parser = __configOptParser()
    opts, args = opt_parser.parse_args()
    
    if len(args) != 0:
        __die('Program does not accept any arguments!')
    
    if not os.path.isdir(opts.out_path):
        __die('Output path does not exist')
    
    out_file = os.path.sep.join((opts.out_path, _OUT_FILE_))
    with codecs.open(out_file, 'w', 'utf-8') as out:
        __getPlanetLabNodeList(out)
