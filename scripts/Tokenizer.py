#!/usr/bin/env python

# -*- coding: iso-8859-15 -*-
'''
Penn Treebank tokenizer based on MOSES implementation.
'''

import sys
import re
import getopt

class PTBTokenizer(object):
     # UTF-8 code pages
     # Numbers
     # [\u0030-\u0039]
     # English alpha characters
     # [\u0041-\u005a\u0061-\u007a]
     # Latin-1 Supplement
     # [\u00c0-\u00ff]
     # Latin-1 extended A
     # [\u0100-\u017F]
     # Latin-1 extended B
     # [\u0180-\u01af\u01c0-\u024f]
     # Latin-1 extended C
     # [\u2c60-\u2c7f]
     alpha = u"\u0041-\u005a\u0061-\u007a\u00c0-\u00ff\u0100-\u017f\u0180-\u01af\u01c0-\u024f\u2c60-\u2c7f"
     alnum = u"\u0030-\u0039\u0041-\u005a\u0061-\u007a\u00c0-\u00ff\u0100-\u017f\u0180-\u01af\u01c0-\u024f\u2c60-\u2c7f"

     def __init__(self, language="en"):
         self.language = language
         self.nonbreaking_prefixes = {}
         self.nonbreaking_prefixes_numeric = {}
         self.nonbreaking_prefixes["en"] = ''' A B C D E F G H I J K L  
             M N O P Q R S T U V W X Y Z
             Adj Adm Adv Asst Bart Bldg Brig Bros Capt Cmdr Col Comdr  
             Con Corp Cpl DR Dr Drs Ens
             Gen Gov Hon Hr Hosp Insp Lt MM MR MRS MS Maj Messrs Mlle  
             Mme Mr Mrs Ms Msgr Op Ord
             Pfc Ph Prof Pvt Rep Reps Res Rev Rt Sen Sens Sfc Sgt Sr  
             St Supt Surg
             v vs i.e rev e.g Nos Nr'''.split()
         self.nonbreaking_prefixes_numeric["en"] = '''No Art pp'''.split()


     def tokenize(self, text, ptbTokenization = False):
         text = text.strip()
         text = " " + text + " "

         # Separate all "other" punctuation
         text = re.sub(u"([^" + self.alnum + u"\s\.\'\`\,\-\"\|])", r' \1 ', text, re.UNICODE)
         text = re.sub(r";", r' ; ', text, re.UNICODE)
         text = re.sub(r":", r' : ', text, re.UNICODE)

         # replace the pipe character
         text = re.sub(r"\|", r' -PIPE- ', text, re.UNICODE)

         # PTB tokenization
         if ptbTokenization:
             text = re.sub(r"\(", r' -LRB- ', text, re.UNICODE)
             text = re.sub(r"\)", r' -RRB- ', text, re.UNICODE)
             text = re.sub(r"\[", r' -LSB- ', text, re.UNICODE)
             text = re.sub(r"\]", r' -RSB- ', text, re.UNICODE)
             text = re.sub(r"\{", r' -LCB- ', text, re.UNICODE)
             text = re.sub(r"\}", r' -RCB- ', text, re.UNICODE)

             text = re.sub(r"\"\s*$", r" '' ", text, re.UNICODE)
             text = re.sub(r"^\s*\"", r' `` ', text, re.UNICODE)
             text = re.sub(r"(\S)\"\s", r"\1 '' ", text, re.UNICODE)
             text = re.sub(r"\s\"(\S)", r" `` \1", text, re.UNICODE)
             text = re.sub(r"(\S)\"", r"\1 '' ", text, re.UNICODE)
             text = re.sub(r"\"(\S)", r" `` \1", text, re.UNICODE)
             text = re.sub(r"'\s*$", r" ' ", text, re.UNICODE)
             text = re.sub(r"^\s*'", r" ` ", text, re.UNICODE)
             text = re.sub(r"(\S)'\s", r"\1 ' ", text, re.UNICODE)
             text = re.sub(r"\s'(\S)", r" ` \1", text, re.UNICODE)

             text = re.sub(r"'ll", r" -CONTRACT-ll", text, re.UNICODE)
             text = re.sub(r"'re", r" -CONTRACT-re", text, re.UNICODE)
             text = re.sub(r"'ve", r" -CONTRACT-ve", text, re.UNICODE)
             text = re.sub(r"n't", r" n-CONTRACT-t", text, re.UNICODE)
             text = re.sub(r"'LL", r" -CONTRACT-LL", text, re.UNICODE)
             text = re.sub(r"'RE", r" -CONTRACT-RE", text, re.UNICODE)
             text = re.sub(r"'VE", r" -CONTRACT-VE", text, re.UNICODE)
             text = re.sub(r"N'T", r" N-CONTRACT-T", text, re.UNICODE)
             text = re.sub(r"cannot", r"can not", text, re.UNICODE)
             text = re.sub(r"Cannot", r"Can not", text, re.UNICODE)

         # multidots stay together
         text = re.sub(r"\.([\.]+)", r" DOTMULTI\1", text, re.UNICODE)
         while re.search("DOTMULTI\.", text):
             text = re.sub(r"DOTMULTI\.([^\.])", r"DOTDOTMULTI \1", text, re.UNICODE)
             text = re.sub(r"DOTMULTI\.", r"DOTDOTMULTI", text, re.UNICODE)

         # multidashes stay together
         text = re.sub(r"\-([\-]+)", r" DASHMULTI\1", text, re.UNICODE)
         while re.search("DASHMULTI\-", text, re.UNICODE):
             text = re.sub(r"DASHMULTI\-([^\-])", r"DASHDASHMULTI \1", text, re.UNICODE)
             text = re.sub(r"DASHMULTI\-", r"DASHDASHMULTI", text, re.UNICODE)

         # Separate ',' except if within number.
         text = re.sub(r"(\D),(\D)", r'\1 , \2', text, re.UNICODE)
         # Separate ',' pre and post number.
         text = re.sub(r"(\d),(\D)", r'\1 , \2', text, re.UNICODE)
         text = re.sub(r"(\D),(\d)", r'\1 , \2', text, re.UNICODE)

         if not ptbTokenization:
             text = re.sub(r"\"", r' " ', text, re.UNICODE)
             # turn ` into '
             text = re.sub(r"\`", r" ' ", text, re.UNICODE)
             # turn '' into "
             text = re.sub(r"''", r' " ', text, re.UNICODE)


         if self.language == "en":
             text = re.sub(u"([^a-z" + self.alpha + u"])'([^a-z" + self.alpha + u"])", r"\1 ' \2", text, re.UNICODE)
             text = re.sub(r"(\W)'([a-z" + self.alpha + u"])", r"\1 ' \2", text, re.UNICODE)
             text = re.sub(r"([a-z" + self.alpha + u"])'([^a-z" + self.alpha + u"])", r"\1 ' \2", text, re.UNICODE)
             text = re.sub(r"([a-z" + self.alpha + u"])'([a-z" + self.alpha + u"])", r"\1 '\2", text, re.UNICODE)
             text = re.sub(r"(\d)'(s)", r"\1 '\2", text, re.UNICODE)
             text = re.sub(r" '\s+s ", r" 's ", text, re.UNICODE)
             text = re.sub(r" '\s+s ", r" 's ", text, re.UNICODE)
         elif self.language == "fr" or self.language == "it":
             text = re.sub(r"([^a-z" + self.alpha + u"])'([^a-z" + self.alpha + u"])", r"\1 ' \2", text, re.UNICODE)
             text = re.sub(r"([^a-z" + self.alpha + u"])'([a-z" + self.alpha + u"])", r"\1 ' \2", text, re.UNICODE)
             text = re.sub(r"([a-z" + self.alpha + u"])'([^a-z" + self.alpha + "])", r"\1 ' \2", text, re.UNICODE)
             text = re.sub(r"([a-z" + self.alpha + u"])'([a-z" + self.alpha + u"])", r"\1' \2", text, re.UNICODE)
         else:
             text = re.sub(r"'", r" ' ", re.UNICODE)

         # re-combine single quotes
         text = re.sub(r"' '", r"''", text, re.UNICODE)

         words = text.split()
         text = ''
         for i, word in enumerate(words):
             m = re.match("^(\S+)\.$", word, re.UNICODE)
             if m:
                 pre = m.group(1)
                 ## debug
                 if ((re.search("\.", pre, re.UNICODE) and 
                      re.search("[a-z" + self.alpha + u"]", pre)) or \
                     (pre in self.nonbreaking_prefixes[self.language])  or \
                          ((i < len(words)-1) and re.match("^[a-z]", words[i+1]))):
                      pass  # do nothing
                 elif ((pre in self.nonbreaking_prefixes_numeric[self.language] ) and \
                       (i < len(words)-1) and re.match("\d+", words[i+1])):
                     pass  # do nothing
                 else:
                     word = pre + " ."

             text += word + " "
         text = re.sub(r"'\s+'", r"''", text, re.UNICODE)

         # restore multidots
         while re.search("DOTDOTMULTI", text, re.UNICODE):
             text = re.sub(r"DOTDOTMULTI", r"DOTMULTI.", text, re.UNICODE)
         text = re.sub(r"DOTMULTI", r".", text, re.UNICODE)

         # restore multidashes
         while re.search("DASHDASHMULTI", text, re.UNICODE):
             text = re.sub(r"DASHDASHMULTI", r"DASHMULTI-", text, re.UNICODE)
         text = re.sub(r"DASHMULTI", r"-", text, re.UNICODE)
         text = re.sub(r"-CONTRACT-", r"'", text, re.UNICODE)

         return text.split()


     def tokenize_all(self,sentences):
         return [self.tokenize(t) for t in sentences]


class DummyTokenizer(object):

     def tokenize(self, text):
         return text.split()


# entry point
# usage : %prog [-p]  < input > output
if __name__ == '__main__':
     opts, args = getopt.getopt(sys.argv[1:], "p")
     ptb = False
     assert len(args) == 0
     for o, v in opts:
         if o == "-p":
             ptb = True
         else:
             print >> sys.stderr, "Unknown option : ", o
     tokenizer = PTBTokenizer()
     for line in sys.stdin:
         line = line.decode("utf8")
         line = line.strip()
         out = ' '.join(tokenizer.tokenize(line, ptb))
         print out.encode("utf8")
