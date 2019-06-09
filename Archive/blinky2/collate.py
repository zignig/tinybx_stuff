# linear shift feedback register periph

#  collection of mls , https://users.ece.cmu.edu/~koopman/lfsr
import os
def gen_output():
    sizes = os.listdir('max_len_seq/')
    seq = {}
    for i in sizes:
        if i.endswith('.txt'):
            t = int(i[:-4])
            f = open('max_len_seq/'+i)
            li = f.readlines()
            f.close()
            tmp = []
            for j in li:
                tmp.append(j.strip())
            seq[t] = tmp
    return seq        

a = {}
if __name__ == "__main__":
    a = gen_output()
    a = 'seq = ' + str(a)
    print(a)
