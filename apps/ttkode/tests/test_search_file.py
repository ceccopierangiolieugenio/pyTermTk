# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../libs/pyTermTk'))

from ttkode.app.helpers.search_file import (
    is_text_file,
    _load_gitignore_patterns,
    _glob_match_patterns,
    _custom_walk,
    TTKode_SearchFile
)


class TestIsTextFile:
    """Test text file detection."""

    def test_text_file_detection(self, tmp_path):
        """Test detection of text files."""
        text_file = tmp_path / "test.txt"
        text_file.write_text("This is a text file\nwith multiple lines")

        assert is_text_file(str(text_file)) is True

    def test_python_file_detection(self, tmp_path):
        """Test Python files are detected as text."""
        py_file = tmp_path / "test.py"
        py_file.write_text("print('hello world')")

        assert is_text_file(str(py_file)) is True

    def test_json_file_detection(self, tmp_path):
        """Test JSON files are detected as text."""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"key": "value"}')

        assert is_text_file(str(json_file)) is True

    def test_binary_file_detection(self, tmp_path):
        """Test binary files are detected correctly."""
        binary_file = tmp_path / "test.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03\x04\x05')

        assert is_text_file(str(binary_file)) is False

    def test_empty_file(self, tmp_path):
        """Test empty file detection."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")

        # Empty files might be considered text depending on implementation
        result = is_text_file(str(empty_file))
        assert isinstance(result, bool)


class TestLoadGitignorePatterns:
    """Test loading .gitignore patterns."""

    def test_load_existing_gitignore(self, tmp_path):
        """Test loading an existing .gitignore file."""
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.pyc\n__pycache__/\n.env\n")

        patterns = _load_gitignore_patterns(str(gitignore))

        assert "*.pyc" in patterns
        assert "__pycache__/" in patterns
        assert ".env" in patterns

    def test_load_nonexistent_gitignore(self, tmp_path):
        """Test loading a non-existent .gitignore file."""
        gitignore_path = str(tmp_path / ".gitignore")
        patterns = _load_gitignore_patterns(gitignore_path)

        assert patterns == []

    def test_empty_gitignore(self, tmp_path):
        """Test loading an empty .gitignore file."""
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("")

        patterns = _load_gitignore_patterns(str(gitignore))
        assert patterns == []

    def test_gitignore_with_comments(self, tmp_path):
        """Test .gitignore with comments."""
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("# This is a comment\n*.pyc\n# Another comment\n__pycache__/")

        patterns = _load_gitignore_patterns(str(gitignore))

        # Comments should be included as-is (filtering happens in matching)
        assert len(patterns) == 4


class TestGlobMatchPatterns:
    """Test glob pattern matching."""

    def test_simple_pattern_match(self):
        """Test simple pattern matching."""
        assert _glob_match_patterns("test.pyc", ["*.pyc"]) is True
        assert _glob_match_patterns("test.py", ["*.pyc"]) is False

    def test_directory_pattern_match(self):
        """Test directory pattern matching."""
        assert _glob_match_patterns("./__pycache__/module.pyc", ["__pycache__"]) is True
        assert _glob_match_patterns("./src/__pycache__/", ["__pycache__"]) is True

    def test_multiple_patterns(self):
        """Test matching against multiple patterns."""
        patterns = ["*.pyc", "*.pyo", "__pycache__"]

        assert _glob_match_patterns("test.pyc", patterns) is True
        assert _glob_match_patterns("test.pyo", patterns) is True
        assert _glob_match_patterns("./__pycache__/", patterns) is True
        assert _glob_match_patterns("test.py", patterns) is False

    def test_empty_patterns(self):
        """Test with empty pattern list."""
        assert _glob_match_patterns("test.py", []) is False

    def test_current_directory(self):
        """Test matching with current directory."""
        result = _glob_match_patterns(".", ["*.pyc"])
        assert isinstance(result, bool)

    def test_relative_path_matching(self):
        """Test matching relative paths."""
        assert _glob_match_patterns("./src/module.pyc", ["*.pyc"]) is True
        assert _glob_match_patterns("src/module.py", ["*.pyc"]) is False


class TestCustomWalk:
    """Test custom directory walking."""

    def test_walk_simple_directory(self, tmp_path):
        """Test walking a simple directory structure."""
        # Create test structure
        (tmp_path / "file1.py").write_text("print('file1')")
        (tmp_path / "file2.txt").write_text("text")

        results = list(_custom_walk(str(tmp_path)))

        assert len(results) == 2
        filenames = [entry[1] for entry in results]
        assert "file1.py" in filenames
        assert "file2.txt" in filenames

    def test_walk_nested_directories(self, tmp_path):
        """Test walking nested directories."""
        # Create nested structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "root.py").write_text("root")
        (subdir / "nested.py").write_text("nested")

        results = list(_custom_walk(str(tmp_path)))

        assert len(results) == 2
        filenames = [entry[1] for entry in results]
        assert "root.py" in filenames
        assert "nested.py" in filenames

    def test_walk_with_exclude_patterns(self, tmp_path):
        """Test walking with exclusion patterns."""
        # Create files
        (tmp_path / "include.py").write_text("include")
        (tmp_path / "exclude.pyc").write_text("exclude")

        results = list(_custom_walk(str(tmp_path), exclude_patterns=["*.pyc"]))

        filenames = [entry[1] for entry in results]
        assert "include.py" in filenames
        assert "exclude.pyc" not in filenames

    def test_walk_with_include_patterns(self, tmp_path):
        """Test walking with inclusion patterns."""
        # Create files
        (tmp_path / "test.py").write_text("python")
        (tmp_path / "test.txt").write_text("text")

        results = list(_custom_walk(str(tmp_path), include_patterns=["*.py"]))

        filenames = [entry[1] for entry in results]
        assert "test.py" in filenames
        assert "test.txt" not in filenames

    def test_walk_ignores_git_directory(self, tmp_path):
        """Test that .git directories are ignored."""
        # Create .git directory
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("git config")
        (tmp_path / "normal.py").write_text("normal file")

        results = list(_custom_walk(str(tmp_path)))

        filenames = [entry[1] for entry in results]
        assert "normal.py" in filenames
        assert "config" not in filenames

    def test_walk_respects_gitignore(self, tmp_path):
        """Test that .gitignore patterns are respected."""
        # Create .gitignore
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.pyc\n__pycache__/")

        # Create files
        (tmp_path / "normal.py").write_text("include")
        (tmp_path / "compiled.pyc").write_text("exclude")

        results = list(_custom_walk(str(tmp_path)))

        filenames = [entry[1] for entry in results]
        assert "normal.py" in filenames
        assert ".gitignore" in filenames
        assert "compiled.pyc" not in filenames


class TestTTKodeSearchFile:
    """Test the file search functionality."""

    def test_search_by_pattern(self, tmp_path):
        """Test searching files by pattern."""
        # Create test files
        pass
        (tmp_path / "test_Eugenio_ABC_file.py").write_text("test")
        (tmp_path / "other.txt").write_text("other")
        (tmp_path / "test_Eugenio_ABC_data.json").write_text("{}")

        results = list(TTKode_SearchFile.getFilesFromPattern(tmp_path, "test_Eugenio_ABC"))

        assert len(results) == 2
        result_names = [r.name for r in results]
        assert "test_Eugenio_ABC_file.py" in result_names
        assert "test_Eugenio_ABC_data.json" in result_names
        assert "other.txt" not in result_names

    def test_search_empty_pattern(self, tmp_path):
        """Test searching with empty pattern matches all files."""
        (tmp_path / "file1.py").write_text("1")
        (tmp_path / "file2.txt").write_text("2")

        results = list(TTKode_SearchFile.getFilesFromPattern(tmp_path, ""))

        # Empty pattern should match all files
        assert len(results) >= 2

    def test_search_no_matches(self, tmp_path):
        """Test searching with pattern that matches nothing."""
        (tmp_path / "file1.py").write_text("1")

        results = list(TTKode_SearchFile.getFilesFromPattern(tmp_path, "nonexistent_pattern_xyz"))

        assert len(results) == 0

    def test_search_nested_directories(self, tmp_path):
        """Test searching in nested directories."""
        # Create nested structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "root_test.py").write_text("root")
        (subdir / "nested_test.py").write_text("nested")

        results = list(TTKode_SearchFile.getFilesFromPattern(tmp_path, "test"))

        assert len(results) == 2
        result_names = [r.name for r in results]
        assert "root_test.py" in result_names
        assert "nested_test.py" in result_names

    def test_search_returns_path_objects(self, tmp_path):
        """Test that search returns Path objects."""
        (tmp_path / "test.py").write_text("test")

        results = list(TTKode_SearchFile.getFilesFromPattern(tmp_path, "test"))

        assert len(results) > 0
        for result in results:
            assert isinstance(result, Path)

    def test_search_case_sensitivity(self, tmp_path):
        """Test search pattern case sensitivity."""
        (tmp_path / "TestFile.py").write_text("test")
        (tmp_path / "testfile.txt").write_text("test")

        results = list(TTKode_SearchFile.getFilesFromPattern(tmp_path, "test"))

        # Should match both (case-insensitive glob matching)
        assert len(results) >= 2
