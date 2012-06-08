# -*- coding: utf-8 -*-

import urlparse

import unicodedata


def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii


def clean(text):
    new_string = ''
    for i in text.split():
        s, n, p, pa, q, f = urlparse.urlparse(i)
        if s and n:
            pass
        elif i[:1] == '@':
            pass
        elif i[:1] == '#':
            new_string = new_string.strip() + ' ' + i[1:]
        else:
            new_string = new_string.strip() + ' ' + i
    return remove_accents(new_string)


def is_valid(tweet, user):
    return not tweet.in_reply_to_status_id and tweet.user.screen_name == user
