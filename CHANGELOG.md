# Changelog

All notable changes to the `pytransposer` extension will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- No unreleased changes.


## [1.2.0] - 2022-10-14
### Added
- Module configuration class `TransposerConfig` in a new sub-module `config`. This holds module-wide configurations that the user can modify.
### Changed
- Changed the `transpose_chord`, `transpose_chord_group` and `transpose_song` methods to always return musicaly correct chords taking into account the `to_key` given by the user or obtained from the first chord of the song.
- Added `standardized_transpose_chord`, `standardized_transpose_chord_group` and `standardized_transpose_song` methods to always return the simplest chord representations, without taking into account any `to_key` whatsoever.
- Changed the algorithm used to transpose chords.
- Update [`README.md`](README.md).
### Removed
- Sub-modules `abc.py` and `doremi.py` and all methods within them (old methods from the previously used transposing algorithm)
  
<!-- ### Changed
### Removed -->

## [1.1.2] - 2022-10-13
### Changed
- Moved the automatic detection of the `to_key` in `transpose_song` into a separate function `song_key`.
- Add function `chord_style` to get the notation system of a given chord.
- Fix minor bug.

## [1.1.1] - 2022-10-13
### Changed
- Made the `to_key` parameter optional in `tranpose_song` (if not given, it is automatically detected by using the first chord of the song).
- Update [`README.md`](README.md).

## [1.1.0] - 2022-10-13
### Added
- Function to transpose whole songs.
- This [`CHANGELOG.md`](CHANGELOG.md) to keep track of changes.


## [1.0.0] - 2022-10-13
### Added
- Initial version of the python package created by [@bfrangi](https://github.com/bfrangi/) and based on the python [`transposer`](https://github.com/davidparsson/transposer) tool by [@davidparsson](https://github.com/davidparsson).
- [`README.md`](README.md) with examples regarding the usage of the package.



[Unreleased]: https://github.com/bfrangi/pytransposer/compare/v1.2.0...HEAD
<!-- [1.1.2]: https://github.com/bfrangi/pytransposer/compare/v1.1.1...v1.1.2 -->
[1.2.0]: https://github.com/bfrangi/pytransposer/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/bfrangi/pytransposer/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/bfrangi/pytransposer/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/bfrangi/pytransposer/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/bfrangi/pytransposer/releases/tag/v1.0.0 