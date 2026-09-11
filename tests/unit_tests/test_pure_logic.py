"""Behavioural tests for pyscrapers' pure helpers.

These exercise real parsing, URL joining, JSON path search and the
duplicate-free URL set - none of which touch the network, cookies or
the filesystem.
"""

import http.client
import unittest

from pyscrapers.core import json as core_json
from pyscrapers.core import utils
from pyscrapers.core.url_set import UrlSet


class HttpUtilsTests(unittest.TestCase):
    def test_add_http_joins_relative_path(self) -> None:
        got = utils.add_http("/photos/1.jpg", "https://example.com/gallery/")
        self.assertEqual(got, "https://example.com/photos/1.jpg")

    def test_add_http_absolute_url_wins(self) -> None:
        got = utils.add_http("https://cdn.example.com/x.png", "https://example.com/")
        self.assertEqual(got, "https://cdn.example.com/x.png")

    def test_get_http_status_string_contains_reason(self) -> None:
        got = utils.get_http_status_string(404)
        self.assertEqual(got, f"http code [404], [{http.client.responses[404]}]")
        self.assertIn("Not Found", got)


class FindPathsTests(unittest.TestCase):
    def test_finds_matching_key(self) -> None:
        data = {"a": {"b": 1}, "target": 2}
        self.assertEqual(core_json.find_paths("target", data), ["[target]"])

    def test_finds_matching_string_value_in_list(self) -> None:
        data = {"items": ["needle", "other"]}
        self.assertEqual(core_json.find_paths("needle", data), ["[items][0]"])

    def test_no_match_returns_empty(self) -> None:
        data = {"a": [1, 2, 3], "b": {"c": True}}
        self.assertEqual(core_json.find_paths("absent", data), [])


class UrlSetTests(unittest.TestCase):
    def test_append_deduplicates(self) -> None:
        url_set = UrlSet()
        url_set.append("https://example.com/a")
        url_set.append("https://example.com/a")
        url_set.append("https://example.com/b")
        self.assertEqual(url_set.urls_list, ["https://example.com/a", "https://example.com/b"])
        self.assertEqual(url_set.appended_twice, 1)

    def test_extend_adds_all_unique(self) -> None:
        url_set = UrlSet()
        url_set.extend(["u1", "u2", "u1"])
        self.assertEqual(url_set.urls_list, ["u1", "u2"])

    def test_suggest_filename_counts_per_suffix(self) -> None:
        url_set = UrlSet()
        self.assertEqual(url_set.suggest_filename(".jpg"), "image0000.jpg")
        self.assertEqual(url_set.suggest_filename(".jpg"), "image0001.jpg")
        self.assertEqual(url_set.suggest_filename(".mp4"), "video0000.mp4")

    def test_suggest_filename_rejects_unknown_suffix(self) -> None:
        url_set = UrlSet()
        self.assertRaises(ValueError, url_set.suggest_filename, ".txt")


if __name__ == "__main__":
    unittest.main()
