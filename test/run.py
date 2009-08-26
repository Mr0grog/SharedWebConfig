# Dumb simple test; nothing too formal (not quite unit testing)

import os
import shutil
import filecmp
import time
import sharedwebconfig

TEST_PATH   = os.path.abspath(os.path.dirname(__file__))
SOURCE_PATH = TEST_PATH + "/test_source"
DEST_PATH   = TEST_PATH + "/test_dest"

def create_file(path, content=''):
	f = open(path, 'w')
	f.write(content)
	f.close()

def should_update_file():
	# Create destination first, then source (so source is newer)
	create_file(DEST_PATH)
	time.sleep(1)
	create_file(SOURCE_PATH, "Source Content!")
	
	# Test Update
	sharedwebconfig.update_file(DEST_PATH, "file://" + SOURCE_PATH)
	
	print("TEST: File updated?\n%s" % str(filecmp.cmp(SOURCE_PATH, DEST_PATH, False)))
	
	# Cleanup
	os.remove(SOURCE_PATH)
	os.remove(DEST_PATH)

def should_not_update_file():
	# Create source first, then destination (so source is older)
	create_file(SOURCE_PATH, "Source Content!")
	time.sleep(1)
	create_file(DEST_PATH)

	# Test Update
	sharedwebconfig.update_file(DEST_PATH, "file://" + SOURCE_PATH)

	print("TEST: File not updated?\n%s" % str(not filecmp.cmp(SOURCE_PATH, DEST_PATH, False)))

	# Cleanup
	os.remove(SOURCE_PATH)
	os.remove(DEST_PATH)

def update_file_with_subs():
	# Create destination first, then source (so source is newer)
	create_file(DEST_PATH)
	time.sleep(1)
	create_file(SOURCE_PATH, "Source Content! {$working_files$}")
	
	# Test Update
	WORKING_FILES = 'location for working files'
	sharedwebconfig.update_file(DEST_PATH, "file://" + SOURCE_PATH, {'working_files':WORKING_FILES})
	
	f = open(DEST_PATH)
	content = f.read()
	f.close()
	print("TEST: File written correctly?\n%s" % str(content == "Source Content! %s" % WORKING_FILES))
	
	# Cleanup
	os.remove(SOURCE_PATH)
	os.remove(DEST_PATH)


# Run tests
if __name__ == "__main__":
	should_update_file()
	should_not_update_file()
	update_file_with_subs()