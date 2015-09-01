#!/usr/bin/env python 


"""                                                                                                                                                                                      

Tokenize text fields and convert annotation to token offsets. 

Usage: token_annotation.py < INPUT > OUTPUT
                                                                                                                                                                                         
Arguments:                                                                                                                                                                               
 INPUT       Input semeval 2014 task 4 xml file 
 OUTPUT      Output xml file with tokenized text
                                                                                                                                                                                         
"""

import xml.sax
import sys
from collections import namedtuple, defaultdict

from nltk.tokenize import word_tokenize
#tokenizer = PTBTokenizer()


# data types for annotation 
aspect_term = namedtuple("aspect_term", "term polarity start end")
aspect_category = namedtuple("aspect_category", "category polarity")


# create Penn Treebank tokenizer
#tokenizer = PTBTokenizer()

def token_offset(sentence, offset):
    return len(word_tokenize(sentence[:offset]))


if __name__ == "__main__":
    import xml.etree.ElementTree as ET
    
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    
    # print header
    print '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <sentences>'''
    
    for ind, child in enumerate(root):
        new_id = ind
        sentence = child[0].text
        print '    <sentence id="%d">' % new_id
        print '        <text>%s</text>' % ' '.join(word_tokenize(sentence)).encode('utf-8').strip()
        if len(child) > 1 and child[1].tag == 'aspectTerms':
            print '        <aspectTerms>'
            for item in child[1]:
                start_token = token_offset(sentence, int(item.attrib['from']))
                end_token = token_offset(sentence, int(item.attrib['to']))
                print '            <aspectTerm term="%s" from="%d" to="%d"/>' % (' '.join(word_tokenize(item.attrib['term'])).encode('utf-8').strip(), start_token, end_token)
            print '        </aspectTerms>'
        if child[-1].tag == 'aspectCategories':
            print '        <aspectCategories>'
            for item in child[-1]:
                print '            <aspectCategory category="%s"/>' % item.attrib['category']
            print '        </aspectCategories>'
            print '    </sentence>' 
        
    print '</sentences>'
            

'''
class AnnotationHandler(xml.sax.ContentHandler):
    def __init__(self):
	self.sentences = {}
	self.aspect_terms = defaultdict(list)
	self.aspect_categories = defaultdict(list)
        self.text = ""

    def startElement(self, name, attrs):
	if name == "sentence":
	    self.id = int(attrs['id'])
	elif name == "text":
            self.text = ""
	elif name == "aspectTerm":
	    self.aspect_terms[self.id].append(aspect_term(attrs['term'], attrs['polarity'], int(attrs['from']), int(attrs['to'])))
        elif name == "aspectCategory":
	    self.aspect_categories[self.id].append(aspect_category(attrs['category'], attrs['polarity']))

    def characters(self, content):
        self.text += content

    def endElement(self, name):
        if name == "text":
	    self.sentences[self.id] = self.text


def token_offset(sentence, offset):
    return len(tokenizer.tokenize(sentence[:offset], ptbTokenization=True))

if __name__ == "__main__":
    import sys
    
    # parse xml
    handler = AnnotationHandler()
    xml.sax.parse(sys.stdin, handler)

    # print header
    print '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    print '<sentences>'
    
    # convert to token level offsets and output
    for id, sentence in sorted(handler.sentences.items()):
        print '    <sentence id="%d">' % id
        print '        <text>%s</text>' % ' '.join(tokenizer.tokenize(sentence))
        print '        <aspectTerms>'
        for item in handler.aspect_terms[id]:
            start_token = token_offset(sentence, item.start)
            end_token = token_offset(sentence, item.end)
            print '            <aspectTerm term="%s" polarity="%s" from="%d" to="%d"/>' % (' '.join(tokenizer.tokenize(item.term, ptbTokenization=True)), item.polarity, start_token, end_token)
        print '        </aspectTerms>'
        print '        <aspectCategories>'
        for item in handler.aspect_categories[id]:
            print '            <aspectCategory category="%s" polarity="%s"/>' % (item.category, item.polarity)
        print '        </aspectCategories>'
        print '    </sentence>'
    print '</sentences>'
'''