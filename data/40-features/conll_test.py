#!/usr/bin/env python 


"""                                                                                                                                                                                      

Create CoNLL style column format files which one attribute per column.

Usage: conll_format.py [-d DELIM] < INPUT > OUTPUT
                                                                                                                                                                                         
Arguments:                                                                                                                                                                               
 INPUT       Tokenized xml file with semeval task 4 annotation
 OUTPUT      Output CoNLL-style column file

Options:
                                                                                                                                                                                         
"""

import xml.sax
import sys
from collections import namedtuple, defaultdict
from future_builtins import zip
import nltk
from nltk.parse.stanford import StanfordParser

from nltk.corpus import wordnet as wn

# data types for annotation 
aspect_term = namedtuple("aspect_term", "term start end")
aspect_category = namedtuple("aspect_category", "category")



def output_columns(features, labels):
    for label, featureItem in zip(zip(*labels), zip(*features)):
        print " ".join(label),"----", " ".join(featureItem)
				
		

def make_bio_annotation(offsets, length, category=None):
    def make_label(i):
        for start, end in offsets:
            if i == start:
                return 'B-%s' % category if category else 'B'
            elif start < i < end:
                return 'I-%s' % category if category else 'I'
        return 'O'
    return (make_label(i) for i in xrange(length))
    
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
            self.aspect_terms[self.id].append(aspect_term(attrs['term'], int(attrs['from']), int(attrs['to'])))
        elif name == "aspectCategory":
            self.aspect_categories[self.id].append(aspect_category(attrs['category']))

    def characters(self, content):
        self.text += content

    def endElement(self, name):
        if name == "text":
            self.sentences[self.id] = self.text

def sent_dep(filename):
    f = filename.read().splitlines()
    plist = []
    all_dep = []
    count = 0
    
    for line in f:
        count += 1

        if line.strip():
            rel_split = line.split('(')
            rel = rel_split[0]
            if len(rel_split) > 2:
                deps = ''.join(rel_split[1:])[:-1]
            else:
                deps = rel_split[1][:-1]
                
            deps = deps.replace(')','')
            '''
            if len(rel_split) != 2:
                print 'error ', rel_split
                sys.exit(0)
            '''
    
            dep_split = deps.split(',')
                
            if len(dep_split) > 2:
                fixed = []
                half = ''
                for piece in dep_split:
                    piece = piece.strip()
                    if '-' not in piece:
                        half += piece
    
                    else:
                        fixed.append(half + piece)
                        half = ''
    
                        #print 'fixed: ', fixed
                dep_split = fixed
    
            final_deps = []
            for dep in dep_split:
                words = dep.split('-')
                if len(words) > 2:
                    char = words[len(words) - 1]
                    char_len = len(char)
                    word = dep[:len(dep) - char_len - 1]
                else:
                    word = words[0]
                
                #print words[len(words) - 1]
                #print count
                if "'" in words[len(words) - 1]:
                    ind = int(words[len(words) - 1][:-1])
                else:
                    ind = int(words[len(words) - 1])
                '''
                if len(words) > 2:
                    word = '-'.join([w for w in words[:-1]])
                '''
                final_deps.append( [ind, word.strip()] )
                
            plist.append([rel,final_deps])
                
        else:
            all_dep.append(plist)
            plist = []
            
    return all_dep
    

if __name__ == "__main__":
    import sys    
    import getopt
    
    count = 0


    opts, args = getopt.getopt(sys.argv[1:]," ")
    assert len(args) == 0
    for o, v in opts:
        print >> sys.stderr, "Unknown option : ", o
        sys.exit(1)

    # parse xml
    handler = AnnotationHandler()
    #xml.sax.parse(sys.stdin, handler)
    xml.sax.parse("Restaurants_Test.xml", handler)
	

    all_deps = sent_dep(open('Restaurants_Test.parsenew', 'r'))
    head_rel = ['amod', 'nsubj', 'dep']
    tail_rel = ['nsubj', 'dobj', 'dep']

    # convert to column format
    for id, sentence in sorted(handler.sentences.items()):
        # tokenized sentence
        count += 1
        sentence = sentence.split()
        pos_review = nltk.pos_tag(sentence)
        pos = [row[1] for row in pos_review]
        sentence_deps = all_deps[count - 1]
        
        #head word
        head_word = []
        #head pos
        head_pos = []
        #dependence relation
        dep_rel1 = []
        dep_rel2 = []
        
        
        #bigram
        next_word = []
        previous_word = []
        #wordnet synsets
        sent_synsets = []
        #next_pos = []
        #previous_pos = []
        for ind, word in enumerate(sentence):
            if ind < len(sentence) - 1:
                right = sentence[ind + 1]
                #right_pos = pos[ind + 1]
            else:
                right = '<e>'
                #right_pos = '<e>'
            next_word.append(right)
            #next_pos.append(right_pos)
            
            if ind > 0:
                left = sentence[ind - 1]
                #left_pos = pos[ind - 1]
            else:
                left = '<s>'
                #left_pos = '<s>'
            previous_word.append(left)
            #previous_pos.append(left_pos)
            
            
        is_cap = []
        for word in sentence:
            if any(c.islower() for c in word):
                cap = 'capitalized'
            else:
                cap = 'non-capitalized'
            is_cap.append(cap)
            
            #head_word
            check_head = False
            check_rel1 = False
            check_rel2 = False
            
            rel_1 = []
            
            for dep in sentence_deps:
                if dep[1][1][1] == word:
                    head = dep[1][0][1]
                    head_tag = pos[dep[1][0][0] - 1]
                    check_head = True
                    
                    
                    #check dep_rel
                    rel_2 = dep[0]
                    if rel_2 in tail_rel:
                        check_rel2 = True

                    
                if dep[1][0][1] == word:
                    relation = dep[0]
                    if relation in head_rel:
                        rel_1.append(relation)
                        check_rel1 = True
                        
                    
                        
                    
            if check_head:
                head_word.append(head)
                head_pos.append(head_tag)
            else:
                head_word.append('null')
                head_pos.append('null')
                
            if check_rel2:
                dep_rel2.append(rel_2)
            else:
                dep_rel2.append('null')
                
            if check_rel1:
                dep_rel1.append(''.join(item + '|' for item in rel_1)[:-1])
            else:
                dep_rel1.append('null')
                
            #add WordNet synsets
            
            if wn.synsets(word, pos=wn.NOUN):
                word_synsets = ','.join(item.name() for item in wn.synsets(word, pos=wn.NOUN))
            else:
                word_synsets = 'null'
            sent_synsets.append(word_synsets)
                

        features = [sentence, pos, next_word, previous_word, is_cap, head_word, dep_rel1, dep_rel2, sent_synsets]
        
        # BIO annotation
        aspect_offsets = map(lambda x: (x.start, x.end), handler.aspect_terms[id]) 
        labels= []
        labels.append(make_bio_annotation(aspect_offsets, len(sentence)))
        '''
        UpperCase= sentence.upper()
        LowerCase= sentence.lower()
        sentence = sentence.split()
        #elongated_words= isElongated(sentence) 
    
        upperCaseSentence= UpperCase.split()
        lowerCaseSentence= LowerCase.split()
        features = [sentence, upperCaseSentence, lowerCaseSentence]
        
		
	  	
        # BIO annotation
        aspect_offsets = map(lambda x: (x.start, x.end), handler.aspect_terms[id]) 
        labels= []
        labels.append(make_bio_annotation(aspect_offsets, len(sentence)))
	  '''
        # output in ConLL format
        output_columns(features, labels)
        print ""
        

