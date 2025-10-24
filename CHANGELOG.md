# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add CHANGELOG.
- Add CONTRIBUTING guide.
- Add `-0 --hide-sourcelyric`.

### Fixed
 - Improve Readme.
  <!-- b41c2f2690297a18786a1a09d951b12759bdbebf  --> 
 - Fix bug related to handle keys from w_chars dictionary correctly.  
 - Fix bug related to centering text

### Changed
 - Store offline uses now the parameter `-o` instead of `-0`.

## [v0.2] - 2025-10-21

### Added

- Added new sections to README.
- Added column `track_duration` to the SQLite3 database.
- Added argument `--highlight-color`.

### Fixed
 - Improved Readme.
 - Fixed a bug related to wide characters and text centering in the terminal.
 - Fixed a bug related to wide characters and translation.


### Removed

 - Removed comments.

### Changed

- Code Refactoring.
  - Due to displaying the translation below the original lyric line, it was necessary to refactor the logic.

- Changed the behavior of the default print mode when translation is enabled – translation will be displayed below original lyric.
- Updated text for `--help`.

## [v0.1] - 2025-10-17

### Added

- Added new sections to Readme.
- Added doc/status_codes.md.
- Added logic for status code 6. The code appears when duration between lyric and current playback is mismatched.


### Fixed
 - Improved Readme.
 - Fixed bug related with SQLite3 and storing lyrics.


### Changed

- Code Refactoring.


