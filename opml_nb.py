"""Parses opml file and newsboat url file and matches urls"""
import argparse
from os import path
from typing import Set, Iterable
import xml.etree.ElementTree as ET


def init_parser() -> argparse.ArgumentParser:
    """Inits script args parser"""
    parser = argparse.ArgumentParser(description="Args for script")
    parser.add_argument("opml_filepath", help="Opml file path")
    parser.add_argument(
        "newsboat_filepath", help="Newsboat urls file path", default="~/.newsboat/urls"
    )
    return parser


def check_files(*files: Iterable[str]):
    """Check files exists"""
    for file in files:
        if not path.exists(file):
            raise FileNotFound(f'File "{file}" not found')


def parse_newsboat_links(newsboat_filepath: str) -> Set:
    """Parses links from newsboat urls file"""
    return {
        line.rstrip()
        for line in open(newsboat_filepath, "r")
        if not line.startswith("[--")
    }


def parse_opml_links(opml_filepath: str) -> Set:
    """Parses links from opml file"""
    tree = ET.parse(opml_filepath)
    root = tree.getroot()
    body = root.find("body")
    return {outline.attrib["xmlUrl"] for outline in body.findall("outline")}


def main(opml_filepath: str, newsboat_filepath: str):
    """Main func"""
    nb_urls = parse_newsboat_links(newsboat_filepath)
    opml_links = parse_opml_links(opml_filepath)
    print("New links from opml:")
    [print(link) for link in opml_links - nb_urls]
    print("New links from newsboat:")
    [print(link) for link in nb_urls - opml_links]


if __name__ == "__main__":
    arg_parser = init_parser()
    args = arg_parser.parse_args()
    check_files(args.opml_filepath, args.newsboat_filepath)
    main(args.opml_filepath, args.newsboat_filepath)
