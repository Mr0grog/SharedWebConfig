#!/usr/bin/env python

# CONFIGURATION #
working_files      = '/Users/[your username]/Documents/WebWork' # Path to all your directories that will serve as virtual hosts
apache_config_file = '/private/etc/apache2/other/shared_config.conf' # Apache config file to change
apache_config_url  = 'http://localhost:9000/test/testapache.conf' # URL for updated Apache config files
self_update_url    = 'http://localhost:9000/test/testremoteupdate.py' # Selfupdate URL


# PROGRAM #
# 
# SharedWebConfig 1.0
# Copyright (c) 2009 Rob Brackett (http://robbrackett.com/)
# Licensed under the MIT license:
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
import os
import datetime
import urllib
import urllib2

# datetimeto822 module inline
import rfc822, calendar, datetime, time

def to_datetime(time_str):
    rfc_date = rfc822.parsedate(time_str)
    date_obj = datetime.datetime.utcfromtimestamp(calendar.timegm(rfc_date))
    return date_obj

def to_rfc822(date_obj):
    time_tuple = date_obj.timetuple()
    rfc_date = rfc822.formatdate(time.mktime(time_tuple))
    return rfc_date
# end module




def get_from_server(url):
	"""
	Fetch content by URL.
	Returns a tuple containing the content(0) and headers(1).
	"""
	request = urllib2.Request(url)
	try:
		data = urllib2.urlopen(request)
		content = data.read()
		info = data.info()
	except:
		content = ''
		info = {}
	
	return (content, info)

def get_from_server_if_modified(url, since):
	"""
	Fetch the content of a URL if it has changed since a given datetime.
	"""
	data = get_from_server(url)
	headers = data[1]
	
	mod_date = to_datetime(headers['Last-Modified'])
	if mod_date > since:
		return data[0]
	else:
		return None

def when_modified(path):
	"""
	Get datetime for when a file was last modified.
	"""
	mod_time = os.path.getmtime(path)
	mod_time = datetime.datetime.utcfromtimestamp(mod_time)
	return mod_time;

def update_file(to_update, from_url, value_dict={}, callback=None):
	"""
	Update a file from a URL. 
	Optionally, substitute values into the file or 
	execute a callback when the file is updated.
	Returns True if the file was modified, False if not.
	"""
	# Get new content
	local_mod_time = when_modified(to_update)
	new_content = get_from_server_if_modified(from_url, local_mod_time)
	
	if new_content:
		print '+ Updating %s' % to_update
		
		# Substitute values 
		# This could be done better, but it will suffice for now.
		for (key, val) in value_dict.iteritems():
			new_content = new_content.replace(('{$%s$}' % key), val)
		
		# Write out the file
		f = open(to_update, 'w')
		f.write(new_content)
		f.close()
		
		# Execute any callbacks
		if callback:
			callback()
		
		return True
	else:
		print '- No new content for %s' % to_update
		return False

def restart_apache():
	# TODO: Should probably pop a dialog here
	os.system('apachectl graceful')

def run_again():
	os.system('python %s' % __file__)
	exit(0)


# Update self
update_file(__file__,
            self_update_url,
            callback=run_again)

# TODO: Test file apache config file to make sure it exists

# Update apache config file
update_file(apache_config_file, 
            apache_config_url, 
            {'working_files':working_files}, 
            restart_apache)


