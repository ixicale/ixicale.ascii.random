""" 
run: python ascii_drop.py [--random | --list | --help] [--all | --safe]

Available args:
    [--random | -r]:  print random ascii art (default)
    [--list | -l]:    print all keys
    [--safe | -s]:    ignore nsfw ascii arts (default)
    [--all | -a]:     include nsfw ascii arts
    [--help | -h]:    print this message

Combinable options are:
1. print random and safe ascii art
    > python ascii_drop.py --random --safe (default)
    > python ascii_drop.py -rs (default)
    > python ascii_drop.py -sr (default)
2. print random ascii art (including nsfw)
    > python ascii_drop.py --random --all
    > python ascii_drop.py -ra
    > python ascii_drop.py -ar
3. print all keys and safe ascii art
    > python ascii_drop.py --list --safe
    > python ascii_drop.py -ls
    > python ascii_drop.py -sl
4. print all keys and all ascii art
    > python ascii_drop.py --list --all
    > python ascii_drop.py -la
    > python ascii_drop.py -al
"""
import random
import argparse
from ascii.catalog import ASCII_ART

NSFW_TAGS = ["ahegao", "oppai", "nude", "nsfw", "sexy"]

def print_random_ascii(safe):
    keys = list(ASCII_ART.keys())
    if safe:
        keys = list(filter(lambda x: not any(tag in x.lower() for tag in NSFW_TAGS), keys))
    random_key = random.choice(keys)
    print(ASCII_ART[random_key])

def print_all_keys(safe):
    keys = list(ASCII_ART.keys())
    if safe:
        keys = list(filter(lambda x: not any(tag in x.lower() for tag in NSFW_TAGS), keys))
    for key in keys:
        print(key)

def main():
    parser = argparse.ArgumentParser(description="ASCII Art Viewer")
    parser.add_argument('--random', '-r', action='store_true', help='Print random ASCII art (default)')
    parser.add_argument('--list', '-l', action='store_true', help='Print all keys')
    parser.add_argument('--safe', '-s', action='store_true', help='Ignore NSFW ASCII arts (default)')
    parser.add_argument('--all', '-a', action='store_true', help='Include NSFW ASCII arts')

    args = parser.parse_args()

    if args.all:
        safe = False
    else:
        safe = True

    if args.list:
        print_all_keys(safe)
    else:
        print_random_ascii(safe)

if __name__ == "__main__":
    main()
