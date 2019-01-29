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


def solved_in_div2(problem, solved):
    for ok in solved:
        if (abs(int(problem.contest_id) - int(ok.contest_id)) == 1) and (problem.name == ok.name):
            return True
    return False


def filter_solved_in_div2(iterable, solved):
    return filter(lambda problem: not solved_in_div2(problem, solved), iterable)


def filter_difficult(iterable, difficulty, max_d):
    return filter(lambda problem: difficulty['{}{}'.format(problem.contest_id, problem.index)] <= max_d, iterable)


def filter_easy(iterable, difficulty, min_d, id2contest):
    return filter(lambda problem: (('Div. 3' not in id2contest[problem.contest_id].name) and ('Div. 2' not in id2contest[problem.contest_id].name)) or
                                  (difficulty['{}{}'.format(problem.contest_id, problem.index)] >= min_d), iterable)


def filter_easy_div2(iterable, difficulty, min_d):
    return filter(lambda problem: (difficulty['{}{}'.format(problem.contest_id, problem.index)] >= min_d), iterable)


div1 = {'legendary grandmaster', 'international grandmaster', 'grandmaster', 'international master', 'master'}

def get_users(api):
    f = open('participants.txt', 'r')
    handles = []
    for line in f:
        handles.append(line)
    # handles = ['mukhametgalin']

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


def cnt_upsolving(runs, problems, id2contest, difficulty):
    res = 0
    for problem in problems:
        print(problem, difficulty['{}{}'.format(problem.contest_id, problem.index)])
        solved_in_contest = False
        for run in runs:
            if (run.problem.name == problem.name) and \
                    (run.creation_time <= id2contest[problem.contest_id].start_time + id2contest[problem.contest_id].duration):
                solved_in_contest = True
                break

        if solved_in_contest:
            continue

        for run in runs:
            if (run.problem.name == problem.name) and \
                    (run.creation_time > id2contest[problem.contest_id].start_time + id2contest[problem.contest_id].duration):
                res += 1
                break
    return res


def print_for_users(api, users, difficulties):
    C_HARD = 1.2
    C_EASY_DIV1 = 0.7
    C_EASY_DIV2 = 0.5
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
        problems = api.problemset_problems()['problems']
        problems = filter_week(problems, contest_ids)

        runs = filter_accepted(api.user_status(user.handle))
        solved = set(run.problem for run in runs)
        ok = set(filter_accepted(api.user_status(user.handle)))

        to_solve = filter_difficult(problems, difficulties, user.rating * C_HARD)
        if user.rank in div1:
            to_solve = filter_easy(to_solve, difficulties, user.rating * C_EASY_DIV1, id2contest)
        else:
            to_solve = filter_easy_div2(to_solve, difficulties, user.rating * C_EASY_DIV2)

        prob = set(to_solve)
        ok_ups = cnt_upsolving(ok, prob, id2contest, difficulties)

        to_solve = filter(lambda p: p not in solved, prob)
        to_solve = filter_solved_in_div2(to_solve, solved)
        should = set(to_solve)

        print("-----", user.handle, "{}/{}-----".format(ok_ups, ok_ups + len(should)))
        for p in should:
            print(make_url(p))


def main(argv):
    api = CodeforcesAPI()

    users = get_users(api)
    diff = get_difficult()

    print_for_users(api, users, diff)


if __name__ == '__main__':
    main(sys.argv)
