def check_neg_pos(pol: list):
    # check the polarity is negative or positive
    neg = 0
    pos = 0
    for p in pol:
        if p == -1:
            neg += 1
        elif p == 1:
            pos += 1
        else:
            pass
    if neg % 2 == 0 and neg != 0:
        return 1
    elif neg % 2 == 1:
        return -1
    elif pos != 0:
        return 1
    else:
        return 0


def diff_po(pol1, pol2):
    # [0,0,0,1]  [0,-1,1,0]
    # check the negative or positive for the polarity list

    return abs(pol2 - pol1)


def main():
    res1 = check_neg_pos([0,0,0,1])
    print(f'res1: 1 is {res1}')
    res2 = check_neg_pos([0,-1,-1,1])
    print(f'res2: 1 is {res2}')
    res3 = check_neg_pos([-1,1,1,1])
    print(f'res3: -1 is {res3}')
    res4 = check_neg_pos([0,0,0,0])
    print(f'res4: 0 is {res4}')
    pol_distances = 0
    mapids = [(0, 1), (1, 1), (4,8), (1,4)]
    for id in mapids:
        i = id[0]
        j = id[1]
        pol_distance = diff_po(i, j)
        pol_distances += pol_distance
    print(f'polarity distance: 1 -> {pol_distances}')


if __name__ == '__main__':
    main()