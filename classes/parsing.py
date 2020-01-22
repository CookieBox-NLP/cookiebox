import sys

class Parsing:
    def __init__(self, file_name, output_name):
        self.PATH = "../data/"
        if file_name != '':
            try:
                self.read_file = open(self.PATH + file_name, 'r')
                self.lines = self.read_file.readlines()
            except:
                print("ERR => Couldn't fine filename")
                sys.exit(1)
            else:
                self.out_file = open(self.PATH + output_name, 'w')
        else:
            print("ERR => Please provide a filename")
            sys.exit(1)

    def perform_remove_white(self):
        tmp_str = str(self.lines)
        tmp_str.replace()
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
