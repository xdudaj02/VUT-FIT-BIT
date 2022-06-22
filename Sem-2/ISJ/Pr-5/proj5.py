import copy


def gen_quiz(qpool, *indexes, altcodes=('A', 'B', 'C', 'D', 'E', 'F'), quiz=None):
    new_qpool = []
    if quiz is None:
        quiz = []
    for i in indexes:
        if (i >= len(qpool)) | (i < -len(qpool)):
            print("Ignoring index  " + str(i) + " - list index out of range")
        else:
            new_qpool.append(copy.deepcopy(qpool[i]))
    for i in range(len(new_qpool)):
        for j in range(len(new_qpool[i][1])):
            if j > (len(altcodes)-1):
                new_qpool[i][1].pop()
            else:
                new_qpool[i][1][j] = altcodes[j] + ": " + new_qpool[i][1][j]
    quiz += new_qpool
    return quiz

