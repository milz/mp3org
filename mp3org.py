import os							# portable file operations 
from colorama import init, deinit	# for cross-platform terminal colours
from termcolor import colored		# for coloured terminal output


# Perform a walk on the user-supplied mu_dir to provide a brief summary
# of their collection (total size, number of folders/files).
def summarize(mu_dir):

	size, n_files, n_dirs = 0, 0, 0

	for root, dirs, files in os.walk(mu_dir):
		for f in files:
			n_files += 1;
			fp = os.path.join(root, f)
			size += os.path.getsize(fp)
		for d in dirs:
			n_dirs += 1;
			summarize(os.path.join(root, d))

	return (convert_bytes(size), n_files, n_dirs);


# Converts bytes to MB/GB/TB for friendly output.
def convert_bytes(n_bytes):

	n_bytes = float(n_bytes)

	if n_bytes >= 1099511627776:
		terabytes = n_bytes / 1099511627776
		size = '%.2fTB' % terabytes
	elif n_bytes >= 1073741824:
		gigabytes = n_bytes / 1073741824
		size = '%.2fGB' % gigabytes
	else:
		megabytes = n_bytes / 1048576
		size = '%.2fMB' % megabytes

	return size


# Prompt the user for their music library location, then call the organizer on the library dir.
def set_mu_dir():

	print 'Enter the location of your music library:'
	mu_dir = os.path.expanduser(raw_input('> ').strip()) # expand '~' paths

	while not os.path.isdir(mu_dir):
		print colored('Oops!', 'red'), 'The path', colored(mu_dir, 'blue'), 'does not exist. Try again:'
		mu_dir = os.path.expanduser(raw_input('> ').strip())

	summary = summarize(mu_dir)

	print '\nThe directory \'{!s}\' contains {!s} of data, spread across...'.format(colored(mu_dir, 'blue'), 
		colored(summary[0], 'blue'))
	print colored(summary[1], 'blue'), 'files, which are contained in...'
	print colored(summary[2], 'blue'), 'directories.\n'

	print 'Review the information above.'
	print 'To run mp3org on this directory, type {!s}. To change directories, type {!s}.'.format(colored('run', 'green'),
		colored('change', 'red'))
	
	what_do = raw_input('> ')

	while what_do.lower() not in {'run', 'change', 'r', 'c'}:
		print 'Please enter either RUN or CHANGE (case insensitive):'
		what_do = raw_input('> ')

	if what_do.lower() == 'change' or what_do.lower() == 'c':
		print set_mu_dir()
	else:
		print 'runnin'
	deinit()

	return mu_dir


if __name__ == '__main__':

	init() # for coloured output
	print colored('mp3org v0.1: a simple library organizer', 'magenta')
	print 'by Miles Gilchrist (http://milesgilchrist.com)\n'

	mu_dir = set_mu_dir()
	deinit()

