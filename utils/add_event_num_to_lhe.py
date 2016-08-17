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
    parser.add_argument('-g', '--targz', action='store_true', help='File is gzipped')
    parser.add_argument('-i', '--input', help='lhe.gz file to process.')
    parser.add_argument('-l', '--input_list', help='Text file containing a list of lhe.gz files.')
    parser.add_argument('-n', '--event_number', help='Event number to start count from.')
    args = parser.parse_args()

    # If an LHE.gz file hasn't been specified, warn the user and exit the 
    # application.
    if args.input is None and args.input_list is None : 
        print 'Please specify a file or list of files to process.'
        sys.exit(2)

    file_list = []
    if args.input_list is not None : 
        try :
            file_list = open(args.input_list, 'r')
        except IOError :
            print 'Unable to open file ' + str(args.input_list)
            sys.exit(2)
    else : 
        file_list.append(args.input)

    event_index = 0
    for lhegz_file in file_list : 

        # Decompress the file
        print 'Decompressing file ' + lhegz_file.strip()
        if args.targz : lhe_file = gzip.GzipFile(lhegz_file.strip(), 'rb')
        else : lhe_file = lhegz_file.strip()

        lhe_tree = et.parse(lhe_file)

        # Loop over all the event elements
        if args.event_number is not None: 
            event_index = int(args.event_number)
        print 'Event number will begin from ' + str(event_index)

        for event in lhe_tree.findall('event') : 
        
            # Split the event block up
            event_block = event.text.split('\n')

            # Get the first line of the block and split it by whitespace.
            block_header = event_block[1].split()

            # Update the new event number
            block_header[1] = str(event_index)
            event_block[1] = '   '.join(block_header)
        
            # Build the updated event block
            event.text = '\n'.join(event_block)
        
            # Increment the event number
            event_index += 1
   
        print 'Event number ended at ' + str(event_index - 1)
        
        output_file = lhegz_file[:lhegz_file.rfind('.')] + '_event_num.lhe.gz'
        print 'Writing output to ' + output_file

        lhe_gzip = gzip.open(output_file, 'wb')
        lhe_tree.write(lhe_gzip)
        lhe_gzip.close()


if __name__ == '__main__' : 
    main()

