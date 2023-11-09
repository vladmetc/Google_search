"""Parse google's query-result-number text"""


def parse_txt(num_txt):
    """
    :param num_txt: google's query result number text string
    :return: int - total number of query results
    """
    spl_str = num_txt.split()
    for i in range(len(spl_str)):
        if 'bout' in spl_str[i]:
            num = int(spl_str[i + 1])
            return num
    print(f"Unexpected result-number text wording: {num_txt}")
    return 0
