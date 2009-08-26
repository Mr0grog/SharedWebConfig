"""
Modify this to reconfigure how SharedWebConfig works.
"""
# Path to all your directories that will serve as virtual hosts
working_files      = '/Users/[your username]/Documents/WebWork'

# Apache config file to change
apache_config_file = '/private/etc/apache2/other/shared_config.conf'

# URL for updated Apache config files
apache_config_url  = 'http://localhost:9000/test/testapache.conf'

# Selfupdate URL
self_update_url    = 'http://localhost:9000/test/testremoteupdate.py'