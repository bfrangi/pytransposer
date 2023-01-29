# Changelog

All notable changes to the `pytransposer` extension will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- No unreleased changes.

## [1.3.2] - 2023-01-29
### Changed
- Replace Ab reference with G# reference.
- Update `README.md`.

## [1.3.1] - 2022-12-16
### Changed
- Fix bug in `pytransposer.transposer.song_key_segments`.
- Replace G# reference with Ab reference.
  
## [1.3.0] - 2022-12-15
### Added
- Downloads badge in `README.md`.
- Ability to change the key of the song half-way through.
  
## [1.2.2] - 2022-10-22
### Changed
- Fixed bug in `pytransposer.transposer.song_key` when the song has no chords.


## [1.2.1] - 2022-10-15
### Changed
- Fixed bug in `pytransposer.config.TransposerConfig.key_chords_abc`.

## [1.2.0] - 2022-10-14
### Added
- Module configuration class `TransposerConfig` in a new sub-module `config`. This holds module-wide configurations that the user can modify.
- Added function (`express_chord_in_key`) to express a general chord in a given key.
### Changed
- Changed the `transpose_chord`, `transpose_chord_group` and `transpose_song` methods to express chords differently depending on the `to_key` parameter: if a target chord is given, chords are expressed in the most musically correct way with respect to the given key; if `'auto'` is given, the target key is automatically determined; and if `None` is given (this is the default), the chords are expressed in their simplest form.
- Changed the algorithm used to transpose chords.
- Update [`README.md`](README.md).
### Removed
- Sub-modules `abc.py` and `doremi.py` and all methods within them (old methods from the previously used transposing algorithm).

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



[Unreleased]: https://github.com/bfrangi/pytransposer/compare/v1.3.2...HEAD
[1.3.2]: https://github.com/bfrangi/pytransposer/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/bfrangi/pytransposer/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/bfrangi/pytransposer/compare/v1.2.1...v1.3.0
[1.2.2]: https://github.com/bfrangi/pytransposer/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/bfrangi/pytransposer/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/bfrangi/pytransposer/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/bfrangi/pytransposer/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/bfrangi/pytransposer/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/bfrangi/pytransposer/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/bfrangi/pytransposer/releases/tag/v1.0.0 