"""Print  'find_element' length and set a pause between searches"""
import time
import random


def t_delay(st_t, name):
    """
    :param st_t: start time
    :param name: name of element(s) searched for
    :return: new start time
    """
    now = time.time()
    lapse = now - st_t
    rand_delay = random.randrange(500, 700, 1) / 100
    print(f"{name} took {lapse} sec, sleep {rand_delay} sec")
    time.sleep(rand_delay)
    now = time.time()
    return now
