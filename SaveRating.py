import sys
import traceback
from codeforces import CodeforcesAPI
from First import get_users


def save_ratings_to_file(users, file):
    sys.stdout = open(file, 'wt')
    for user in users:
        print(user.handle, user.rating)


def main():
    api = CodeforcesAPI()

    users = get_users(api)
    save_ratings_to_file(users, 'rating4.txt')


if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
        sys.exit(1)
