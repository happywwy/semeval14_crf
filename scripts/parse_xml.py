#!/usr/bin/env python 


"""                                                                                                                                                                                      
SemEval 2014 Task 4 XML parser

Usage: parser_xml.py < INPUT > OUTPUT
                                                                                                                                                                                         
Arguments:                                                                                                                                                                               
 INPUT       Input semeval 2014 task 4 xml file 
 
                                                                                                                                                                                         
"""

import xml.sax


class SentenceHandler(xml.sax.ContentHandler):
    def __init__(self, output):
        self.output = output
        self.text = ""

    def startElement(self, name, attrs):
        if name == "text":
            self.text = ""

    def characters(self, content):
        self.text += content

    def endElement(self, name):
        if name == "text":
            print self.text.encode("utf8")


if __name__ == "__main__":
    import sys

    handler = SentenceHandler(sys.stdout)
    xml.sax.parse(sys.stdin, handler)
