#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""


import requests

def count_words(subreddit, word_list, after=None, word_dict=None):
    """A function that queries the Reddit API recursively, parses the title of
    all hot articles, and prints a sorted count of given keywords."""
    
    if word_dict is None:
        word_dict = {}

    if after is None:
        sorted_word_dict = sorted(word_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_word_dict:
            print(f"{word.lower()}: {count}")
        return

    url = f"https://www.reddit.com/r/subreddit/hot/.json"
    headers = {"User-Agent": "python:reddit_keyword_counter:v1.0 (by /u/ernest_b_shong)"}
    params = {"limit": 100, "after": after}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        print("Invalid subreddit or no posts match.")
        return

    try:
        data = response.json()
        posts = data["data"]["children"]
        after = data["data"]["after"]

        for post in posts:
            title = post["data"]["title"].lower()
            words = title.split()

            for word in words:
                word = word.rstrip('.!?')
                if word.lower() in word_list:
                    word_dict[word.lower()] = word_dict.get(word.lower(), 0) + 1

    except Exception as e:
        print(f"Error: {e}")
        return

    count_words(subreddit, word_list, after, word_dict)
