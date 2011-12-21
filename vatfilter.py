#!/usr/bin/python

import sys
import re

header = []
header_line = """##INFO=<ID=VAchange,Number=A,Type=Integer,Description="the number of transcripts which corresponding VAT annotation (VA) suggests this allele will functionally impact">"""

for line in sys.stdin:
    if line.startswith('#'):
        header.append(line.strip())
        continue
    elif header:
        # add our annotation to the end of the header
        header.insert(len(header) - 1, header_line)
        print "\n".join(header)
        header = []
    fields = line.strip().split()
    info = fields[7]
    # find the VAT field, if there is one
    # for each annotation, check if it indicates AA change or not
    VAchange = []
    for field in info.split(';'):
        if field.startswith('VA='):
            VATrecords = field.split('=')[1].split(',')
            for record in VATrecords:
                # split out the AA sequence change diagram(s)
                # using a regex
                affectedtranscripts = 0
                for a, b in [x.split('->') for x in re.findall("_(\w?->\w)", record)]:
                    if a != b:
                        affectedtranscripts += 1
                VAchange.append(str(affectedtranscripts))
    info = "VAchange=" + ",".join(VAchange) + ";" + info
    fields[7] = info
    print "\t".join(fields)
