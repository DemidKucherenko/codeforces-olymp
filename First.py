#!/usr/bin/env python3

from collections import defaultdict
from itertools import groupby
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


def filter_difficult(iterable, difficulty, max_d):
    return filter(lambda problem: difficulty['{}{}'.format(problem.contest_id, problem.index)] <= max_d, iterable)


def filter_easy(iterable, difficulty, min_d, id2contest):
    return filter(lambda problem: (('Div. 3' not in id2contest[problem.contest_id].name) and ('Div. 2' not in id2contest[problem.contest_id].name)) or
                                  (difficulty['{}{}'.format(problem.contest_id, problem.index)] >= min_d), iterable)


div1 = {'legendary grandmaster', 'international grandmaster', 'grandmaster', 'international master', 'master'}

def get_users(api):
    f = open('participants.txt', 'r')
    handles = []
    for line in f:
        handles.append(line)
    # handles = ['sava-cska']

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

def print_for_users(api, users, difficulties):
    C_HARD = 1.2
    C_EASY = 0.7
    week_start = datetime.fromisoformat("2019-01-21 00:00:00")
    week_end = datetime.fromisoformat("2019-01-28 00:00:00")

    contests = api.contest_list()
    contests_week = filter(lambda s: (s.start_time > datetime.timestamp(week_start)) and
                                (s.start_time < datetime.timestamp(week_end)), contests)

    id2contest = {}
    for contest in contests_week:
        id2contest[get_contest_id(contest)] = contest

    contests_week = id2contest.values()

    contest_ids = set(contest.id for contest in contests_week)


    for user in users:
        print("-----", user.handle, "-----")
        problems = api.problemset_problems()['problems']
        problems = filter_week(problems, contest_ids)

        runs = filter_accepted(api.user_status(user.handle))
        solved = set(run.problem for run in runs)

        to_solve = filter(lambda p: p not in solved, problems)
        to_solve = filter_difficult(to_solve, difficulties, user.rating * C_HARD)

        if user.rank in div1:
            to_solve = filter_easy(to_solve, difficulties, user.rating * C_EASY, id2contest)


        for p in to_solve:
            print(make_url(p))


def main(argv):
    api = CodeforcesAPI()

    users = get_users(api)
    diff = get_difficult()

    print_for_users(api, users, diff)


if __name__ == '__main__':
    main(sys.argv)
