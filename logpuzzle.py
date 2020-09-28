#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    with open(filename) as f:
        content = f.read()
    puzzle_url_pattern = re.compile(r'GET (\S*puzzle\S*) HTTP')
    puzzle_urls = puzzle_url_pattern.findall(content)
    # Remove Duplicates
    puzzle_urls = list(set(puzzle_urls))
    puzzle_urls.sort()
    filepath_pattern = re.compile(r'\S*(code\S*)')
    filepath = filepath_pattern.findall(filename)
    full_path = [
        os.path.join('http://', filepath[0], x.strip('/')) for x in puzzle_urls
        ]
    return full_path


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if os.path.exists(dest_dir) is False:
        os.makedirs(dest_dir)

    with open(os.path.join(dest_dir, 'index.html'), 'a') as f:
        # clear file
        f.truncate(0)
        f.write(
            '<html>\n'
            '<body>\n'
        )
        for i, img_url in enumerate(img_urls):
            filepath = os.path.join(dest_dir, f'img{i}')
            urllib.request.urlretrieve(
                img_url, filepath, print(f'Retrieving {img_url}')
                )
            f.write(f'<img src="img{i}">')
        f.write(
            '\n'
            '</body>\n'
            '</html>\n'
        )
    pass


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
