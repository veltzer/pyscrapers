"""Behavioural tests for pyscrapers' pure helpers.

These exercise real parsing, URL joining, JSON path search and the
duplicate-free URL set - none of which touch the network, cookies or
the filesystem.
"""

import http.client
import unittest

import pytest

from pyscrapers.core import json as core_json
from pyscrapers.core import utils
from pyscrapers.core.url_set import UrlSet


class HttpUtilsTests(unittest.TestCase):
    def test_add_http_joins_relative_path(self) -> None:
        got = utils.add_http("/photos/1.jpg", "https://example.com/gallery/")
        assert got == "https://example.com/photos/1.jpg"

    def test_add_http_absolute_url_wins(self) -> None:
        got = utils.add_http("https://cdn.example.com/x.png", "https://example.com/")
        assert got == "https://cdn.example.com/x.png"

    def test_get_http_status_string_contains_reason(self) -> None:
        got = utils.get_http_status_string(404)
        assert got == f"http code [404], [{http.client.responses[404]}]"
        assert "Not Found" in got


class FindPathsTests(unittest.TestCase):
    def test_finds_matching_key(self) -> None:
        data = {"a": {"b": 1}, "target": 2}
        assert core_json.find_paths("target", data) == ["[target]"]

    def test_finds_matching_string_value_in_list(self) -> None:
        data = {"items": ["needle", "other"]}
        assert core_json.find_paths("needle", data) == ["[items][0]"]

    def test_no_match_returns_empty(self) -> None:
        data = {"a": [1, 2, 3], "b": {"c": True}}
        assert core_json.find_paths("absent", data) == []


class UrlSetTests(unittest.TestCase):
    def test_append_deduplicates(self) -> None:
        url_set = UrlSet()
        url_set.append("https://example.com/a")
        url_set.append("https://example.com/a")
        url_set.append("https://example.com/b")
        assert url_set.urls_list == ["https://example.com/a", "https://example.com/b"]
        assert url_set.appended_twice == 1

    def test_extend_adds_all_unique(self) -> None:
        url_set = UrlSet()
        url_set.extend(["u1", "u2", "u1"])
        assert url_set.urls_list == ["u1", "u2"]

    def test_suggest_filename_counts_per_suffix(self) -> None:
        url_set = UrlSet()
        assert url_set.suggest_filename(".jpg") == "image0000.jpg"
        assert url_set.suggest_filename(".jpg") == "image0001.jpg"
        assert url_set.suggest_filename(".mp4") == "video0000.mp4"

    def test_suggest_filename_rejects_unknown_suffix(self) -> None:
        url_set = UrlSet()
        with pytest.raises(ValueError, match="dont know how to handle suffix"):
            url_set.suggest_filename(".txt")


if __name__ == "__main__":
    unittest.main()
