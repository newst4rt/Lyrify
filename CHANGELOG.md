# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Update Readme.
- Refactor code in `main.py`
- Improve performance in `src/utils/romanizer_uroman.py`
- Refactor `src/lyric_providers/lrclib.py`

### Fixed

 - Fixed Bug in `w_chars`for displaying lyrics with Asian characters off-center  

## [v0.4] - 2025-10-31

### Add

- Added romanizer [uroman](https://pypi.org/project/uroman).
- Added new argument `-r --romanize`.
- Added romanizer support for translation.
- Added custom-built argument parser `Commander`.

### Changed

- Refactored code due to added romanizer.
- Refactored `main.py` due to `Commander`.
- Removed `argparse` and `rich-argparse`.
- Updated Readme.
- Updated Changelog.
- Updated Contributing.


### Fixed
- Terminal cursor is now disabled during runtime.

## [v0.3] - 2025-10-24

### Added

 - Added CHANGELOG.
   <!-- 5e0f5e86f97728b2f0ed8b649fcf413cb0fe21e5, 264379bd7dac5a9eeb128bae9142934320c1600f -->
 - Added CONTRIBUTING guide.
   <!-- 017161360d9fba626ea35bba79eb82d9c53b2bef, 35b08f9239e96a5cfca24c7aae943dafd5a18e08 -->
 - Added `-0 --hide-sourcelyric`.
<!-- c80c0c90a25ba7abc73d9368a18e27c25f6668bf, c9ce720d0fe88223e8ce7d4870b8d8216ac40b0d, 11aa67eca59bdc81a6ac587cc1de82995026039e -->
### Fixed
 - Fixed bug related to handle keys from w_chars dictionary correctly.  
   <!-- b41c2f2690297a18786a1a09d951b12759bdbebf  --> 
 - Fixed bug related to use `--mode dbus <player>`.
   <!-- 27dd914f9ca3db0634518e707e588740388ed994 -->
 - Fixed program termination when an unavailable player is passed to `--mode dbus <player>`.
   <!-- 8b8c83df5012bbf6b6e4e9b0ffcaa23c2e26b8a5 -->

### Changed
 - Offline storage parameter is now `-o` instead of `-0`.
   <!-- 11aa67eca59bdc81a6ac587cc1de82995026039e -->
  - Updated Readme.
    <!-- 9a2706ff1c2374ab8f2f682bdcbdd275b2971f5f, 20a34638a7a6211d86f9ee5401b005736b47d743, 543331cdfbad8395d74fcd022f83a156adb194ca -->
  - Updated doc/status_code
    <!-- 8ea46f5e39e07fe7f45cac6e1344e9af9b237174 -->

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


