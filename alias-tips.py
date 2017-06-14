from __future__ import print_function

import os
import sys


def format_tip(s, prefix):
    color_blue_normal = '\033[94m'
    color_blue_bold = '\033[1;94m'
    color_reset = '\033[0m'
    return color_blue_normal + prefix + color_blue_bold + s + color_reset


def split(input):
    aliases, functions = [], []
    for line in input:
        line = line.strip('\n')
        if line.endswith(' () {'):
            functions.append(line[:-5].strip())
        elif '=' in line:
            # It's hard to exclude all accidental lines in function body without
            # parsing it. This is "good enough"(tm)
            aliases.append(line)
    return aliases, functions


def parse_aliases(raw_aliases):
    aliases = []
    for alias_line in raw_aliases:
        try:
            alias, expanded = alias_line.strip().split('=', 1)

            alias = alias.strip()
            if alias.startswith('\'') and alias.endswith('\''):
                alias = alias.strip('\'')
            alias = alias.strip()

            expanded = expanded.strip()
            if expanded.startswith('\'') and expanded.endswith('\''):
                expanded = expanded.strip('\'')
            expanded = expanded.strip()

            aliases.append((alias, expanded))
        except:
            # If this fails, it's likely a multi-line declared alias,
            # which is currently not handled.
            pass
    return aliases


def exclude_aliases(aliases, excludes):
    return [alias for alias in aliases if alias[0] not in excludes]


def expand_input(input, aliases):
    max_exp, max_expanded = 0, None
    for alias, expanded in aliases:
        if (input.startswith(alias + ' ') and
            len(expanded) > len(alias) and
            len(expanded) > max_exp):
            max_expanded = input.replace(alias, expanded, 1)
            max_exp = len(expanded)
    return max_expanded if max_expanded else input


def find_alias(aliases, input):
    aliases.sort(key=lambda x: len(x[1]), reverse=True)

    res_prev, res = None, input

    while res_prev != res:
        res_prev = res
        for alias, expanded in aliases:
            if res == expanded or res.startswith(expanded + ' '):
                idx = len(expanded)
                res = alias + res[idx:]

    return res


def run(aliases, input, expand, excludes):
    if excludes:
        aliases = exclude_aliases(aliases, excludes.split())

    if expand:
        input = expand_input(input, aliases)

    return find_alias(aliases, input)


def main(args):
    prefix   = os.getenv('ZSH_PLUGINS_ALIAS_TIPS_TEXT', 'Alias tip: ')
    expand   = os.getenv('ZSH_PLUGINS_ALIAS_TIPS_EXPAND', '1') == '1'
    excludes = os.getenv('ZSH_PLUGINS_ALIAS_TIPS_EXCLUDES', '')
    force    = os.getenv('ZSH_PLUGINS_ALIAS_TIPS_FORCE', '0') == '1'
    input    = args[0].strip()  # Other args are resolved aliases
    als, fns = split(sys.stdin.readlines())

    # Don't suggest alias for functions
    for fn in fns:
        if input.startswith(fn):
            sys.exit(1)

    aliases  = parse_aliases(als)
    alias    = run(aliases, input, expand, excludes)

    if len(alias) < len(input) and alias != input:
        print(format_tip(alias, prefix))
        if force:
            sys.exit(10)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
