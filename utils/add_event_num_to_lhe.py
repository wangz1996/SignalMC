#!/usr/bin/python

#
# add_event_num_to_lhe.py
#   author  Omar Moreno
#           SLAC National Accelerator Laboratory
#   date    August 08, 2016
#
# Script that parses lhe files and replaces the second value of the first line
# of the event block with an event number.
#

import argparse
import gzip
import sys
import xml.etree.cElementTree as et

#----------#
#   Main   # 
#----------#

def main() : 
    
    # Parse all command line arguments using the argparse module
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-i", "--input", help="lhe.gz file to process.")
    parser.add_argument("-n", "--event_number", help="Event number to start count from.")
    parser.add_argument("-o", "--output", help="Name of output lhe.gz file.")
    args = parser.parse_args()

    # If an LHE.gz file hasn't been specified, warn the user and exit the 
    # application.
    if args.input is None : 
        print 'Please specify an LHE.gz file to process'
        sys.exit(2)

    # Decompress the file
    print "Decompressing file " + args.input
    lhe_file = gzip.GzipFile(args.input, 'rb')

    lhe_tree = et.parse(lhe_file)

    # Loop over all the event elements
    event_index = 0
    if args.event_number is not None: 
        event_index = int(args.event_number)
    print "Event number will begin from " + str(event_index)

    for event in lhe_tree.findall('event') : 
        
        # Split the event block up
        event_block = event.text.split('\n')

        # Get the first line of the block and split it by whitespace.
        block_header = event_block[1].split()

        # Update the new event number
        block_header[1] = str(event_index)
        event_block[1] = "   ".join(block_header)
        
        # Build the update event block
        event.text = "\n".join(event_block)
        
        # Increment the event number
        event_index += 1
    
    lhe_gzip = gzip.open(args.output, 'wb')
    lhe_tree.write(lhe_gzip)
    lhe_gzip.close()


if __name__ == "__main__" : 
    main()

