import sys
import spacy as sp
from spacy.matcher import Matcher
class Parsing:
    def __init__(self, file_name, output_name):
        self.WRITE_PATH = "../out/"
        self.OPEN_PATH = "../data/"
        if file_name != '':
            try:
                self.read_file = open(self.OPEN_PATH + file_name, 'r')
                self.lines = self.read_file.readlines()
                self.spacy = sp.load('en_core_web_sm')
            except:
                print("ERR => Couldn't find filename")
                sys.exit(1)
            else:
                self.out_file = open(self.WRITE_PATH + output_name, 'w')
        else:
            print("ERR => Please provide a filename")
            sys.exit(1)

    def perform_remove_white(self):

        tmp_str = str(self.lines)
        tmp_split = tmp_str.split(" ")
        self.out_file.writelines(''.join(tmp_split))

    def perform_remove_substring(self, string):

        for l in self.lines:
            tmp = l
            start = 0
            while string in l:
                ind = l.index(string, start, len(l))
                start = ind
                tmp = l[:ind] + l[ind + len(string):]
                l = tmp
            self.out_file.write(l)

    def perform_replace_substring(self, r_string, p_string):

        if r_string != p_string:
            for l in self.lines:
                tmp = l
                start = 0
                while r_string in l:
                    ind = l.index(r_string, start, len(l))
                    start = ind
                    end_ref = ind + len(r_string)
                    tmp = l[:ind] + p_string + l[end_ref:]
                    l = tmp
                self.out_file.write(l)
        else:
            [self.out_file.write(l) for l in self.lines]

    def perform_extract_all(self):
        ent = []
        attr = []
        for sent in self.lines[0].split('.'):
            ent += self.perform_extract_entites(sent)
            # attr += self.perform_extract_attributes(sent)
        print("Final =>", ent)

    def perform_extract_entites(self, sent):
        ent1 = ""
        ent2 = ""

        prv_tok_dep = ""  # dependency tag of previous token in the sentence
        prv_tok_text = ""  # previous token in the sentence

        prefix = ""
        modifier = ""


        for tok in self.spacy(sent):
            if tok.dep_ != "punct":
                if tok.dep_ == "compound":
                    prefix = tok.text
                    if prv_tok_dep == "compound":
                        prefix = prv_tok_text + " " + tok.text

                if tok.dep_.endswith("mod") == True:
                    modifier = tok.text
                    if prv_tok_dep == "compound":
                        modifier = prv_tok_text + " " + tok.text

                if tok.dep_.find("subj") == True:
                    ent1 = modifier + " " + prefix + " " + tok.text
                    prefix = ""
                    modifier = ""
                    prv_tok_dep = ""
                    prv_tok_text = ""

                if tok.dep_.find("obj") == True:
                    ent2 = modifier + " " + prefix + " " + tok.text
                prv_tok_dep = tok.dep_
                prv_tok_text = tok.text
        return [[ent1.strip(), ent2.strip()]]

    def perform_extract_attributes(self, sent):
        doc = self.spacy(sent)

        # Matcher class object
        matcher = Matcher(self.spacy.vocab)

        # define the pattern
        pattern = [{'DEP': 'ROOT'},
                   {'DEP': 'prep', 'OP': "?"},
                   {'DEP': 'agent', 'OP': "?"},
                   {'POS': 'ADJ', 'OP': "?"}]

        matcher.add("matching_1", None, pattern)

        matches = matcher(doc)
        k = len(matches) - 1

        span = doc[matches[k][1]:matches[k][2]]

        return [span.text]
