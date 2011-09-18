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


import xmlrpclib as rpc
