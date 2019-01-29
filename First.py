#!/usr/bin/env python3

"""
In this example we are loading only unsolved Div2.C problems
"""

from collections import defaultdict
from itertools import groupby
import os
import sys
import time

from datetime import datetime
from codeforces import CodeforcesAPI
from codeforces import VerdictType
from codeforces import Problem
from codeforces import Contest


def first_or_default(lst, f):
    return next(filter(f, lst), None)


def get_contest_id(x):
    assert isinstance(x, (Problem, Contest))

    if isinstance(x, Problem):
        return x.contest_id
    else:
        return x.id


def group_by_contest_id(iterable):
    res = defaultdict(list)

    for k, vs in groupby(iterable, get_contest_id):
        res[k].extend(vs)

    return res


def make_url(problem):
    return 'http://codeforces.com/contest/{}/problem/{}'.format(problem.contest_id, problem.index)


def filter_div2(iterable):
    return filter(lambda contest: 'Div. 2' in contest.name, iterable)


def filter_c(iterable):
    return filter(lambda problem: 'C' in problem.index, iterable)


def filter_accepted(iterable):
    return filter(lambda submission: submission.verdict is not None and submission.verdict == VerdictType.ok, iterable)


def filter_week(iterable, contests_ids):
    return filter(lambda problem: problem.contest_id in contests_ids, iterable)


def filter_difficult(iterable, diff, max_v):
    return filter(lambda problem: diff['{}{}'.format(problem.contest_id, problem.index)] < max_v, iterable)


def get_users(api):
    f = open('participants.txt', 'r')
    handles = []
    for line in f:
        handles.append(line)
    # handles = ['Dos']

    users = []
    for handle in handles:
        for u in api.user_info([handle]):
            users.append(u)
        time.sleep(0.1)

    return users


def get_difficult():
    f = open('problems.txt', 'r')
    res = {}
    for line in f:
        s = line.split()
        res[s[0]] = int(s[len(s) - 2])
    return res


def print_for_users(api, users, diff):
    C = 1.2
    week_start = datetime.fromisoformat("2019-01-21 00:00:00")
    week_end = datetime.fromisoformat("2019-01-28 00:00:00")

    contests = api.contest_list()
    contests = filter(lambda s: (s.start_time > datetime.timestamp(week_start)) and
                                (s.start_time < datetime.timestamp(week_end)), contests)

    contest_ids = set(contest.id for contest in contests)


    for user in users:
        print("-----", user.handle, "-----")
        problems = api.problemset_problems()['problems']
        problems = filter_week(problems, contest_ids)

        runs = filter_accepted(api.user_status(user.handle))
        solved = set(run.problem for run in runs)

        to_solve = filter(lambda p: p not in solved, problems)
        to_solve = filter_difficult(to_solve, diff, user.rating * C)

        for p in to_solve:
            print(make_url(p))


def main(argv):
    # assert len(argv) == 2

    api = CodeforcesAPI()

    users = get_users(api)
    diff = get_difficult()

    print_for_users(api, users, diff)

    #
    # print('Loading your submissions')
    # handle = argv[1]
    # submissions = filter_accepted(api.user_status(handle))
    # solved_problems = filter_c(submission.problem for submission in submissions)
    # solved_problems = set(solved_problems)
    # print('Loaded {} solved C problems'.format(len(solved_problems)))
    #
    # print('Loading contests...')
    # contests = group_by_contest_id(filter_div2(api.contest_list()))
    #
    # print('Loaded {} Div.2 contests'.format(len(contests)))
    #
    # print('Loading problemset...')
    # problemset = api.problemset_problems()
    #
    # problems = group_by_contest_id(filter_c(problemset['problems']))
    #
    # stats = problemset['problemStatistics']
    # stats = filter_c(stats)
    # stats = filter(lambda s: s.contest_id in contests, stats)
    # stats = filter(lambda s: problems[s.contest_id][0] not in solved_problems, stats)
    # stats = sorted(stats, key=lambda s: s.solved_count, reverse=True)
    #
    #
    # print()
    # print('{:30}{:15}{}'.format('Name', 'Solved count', 'Url'))
    #
    # for stat in stats[:10]:
    #     problem = problems[stat.contest_id][0]
    #     print('{:30}{:<15}{}'.format(problem.name, stat.solved_count, make_url(problem)))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main(sys.argv)
    else:
        print('Invalid number of arguments')
        print('Usage: python3 {} [user handle]'.format(os.path.basename(sys.argv[0])))
        sys.exit(1)