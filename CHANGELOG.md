# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.6]  - 2025-11-08

### Added

 - **Added `src/core/winrt_wmc.py` as new mode options on Windows.**
   <!-- 37399237cdb5bc0b03321cf8725394e942e3968e -->
 - Added requirements
   <!-- 7c1d972c09e209fa374f5f1bb31d8a0c990f7c50 -->
 - Added utility script to list all player on Windows.
   <!-- f5bdb4f4c4e8a73b0f05dd3550d0666d9203484c -->

### Changed
 - Refactored code in the modes modules by adding them into class
   <!-- 37399237cdb5bc0b03321cf8725394e942e3968e -->
 - Updated README
   <!-- bbb2d42b8f7029ff69d623767ba11c294e915929
   8a5f421709e41bc7ade3a7645d589169bba979b1  
   0ec30dbeb6af69f452983b2cc19b67809e40a543 -->
 - Updated submodule @Commander
   <!-- ce2f21cd782ebbd36890db11d032da34b6827bb1 -->
 - Fixed bug by using `--store-offline` on Windows
   <!-- 47840bcb5cfb670c55fe253ebf0af223e29b3d59 -->
 - Fixed issues, removed useless lines, improved performance and logic in `main.py`
   <!-- 26bd5eac657e7f2fc3404896f567cf8410c6b797 -->
 - Fixed adjusting center position for displaying status code
   <!-- d8e189aea8419b284ca27b19a499ef71af410f77 -->

### Removed

- Removed duration check between playback and lyrics <sup>*it makes status code 6 useless</sup>
  <!-- 5b91d2c191bec54cd8d4e06d8efa51c75d752adf -->
- Removed status code 6 in `docs/status_codes.md`
  <!-- d63dbd1d07e9356c950c69448b885ea4726a8494 -->

## [v0.5]  - 2025-11-03

### Added

- **Added Windows support.**
  <!-- b9df4f6f58c477f2119832cc41926800b00baf57 -->
- Added type hints and comments.
  <!-- fc03b9560b0a4f331b9a1c41f6ea7997a298ae1a
  9d296f8940a0ee91ad86244b4a3ad04cb68638ed
  e6e2d8eec525cabd72439eb64b8e1022da1fdce6 --> 
- Added fallbacks in the Spotify API modules.
  <!-- 7ab228efe5961d159e7443eff6ce30afbcf27085
  13b5d90a444ec5b2b98086fb8b63f13006d947e3
  4145b4ae7877281acfa560fa586c2fa182dc9b01 -->


### Changed

- Update Readme.
  <!-- 71555c3b12efdef425966dc851b1fc62648c966a -->
- Improve performance in `src/utils/romanizer_uroman.py`.
  <!-- 01a6afc3a7344bdcf4bfae019ec1bc5d6d24560f -->
- improved performance in `src/core/__main__.py` and `src/utils/romanizer_uroman.py` .
  <!-- 73de41b115d50eff303bce2d910333b164152c8b 
  01a6afc3a7344bdcf4bfae019ec1bc5d6d24560f
  -->

### Removed

 - Removed `--mode dbus` argument in Windows.
  <!-- 4c33b4277bf214fa40888ebb459aed5d7d40bfa7 -->

### Fixed

 - Fixed Bug in `w_chars`for displaying lyrics with Asian characters off-center.
   <!-- a89096ef30c12959c7d416bfa97c2d8975ec80a9 -->
 - Fixed possible crash if `w_chars` is None.
   <!-- 0f719e4a6cebc32c4fa8003614d438507aabe062  --> 
 - Fixed errors in `main.py`.
   <!-- 0219ed6bd1056922a8be3267c02d7c3db083d08c -->
 - Fixed disappearing terminal cursor if a crash occurs.
   <!-- 2428aba64e862cbadde335577feb855c85a66507 -->
 - Fixed potential issues in older Python versions caused by nested f-strings.
   <!-- b9df4f6f58c477f2119832cc41926800b00baf57 -->


## [v0.4] - 2025-10-31

### Added

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


