PyTransposer 
==========

[![Build Status](https://github.com/bfrangi/pytransposer/workflows/CI/badge.svg)](https://github.com/bfrangi/pytransposer/actions?query=workflow%3ACI) [![Downloads](https://img.shields.io/pypi/dm/pytransposer?color=brightgreen&label=PyPI%20Downloads)](https://pypi.org/project/pytransposer/) 

Python module for transposing chords and entire songs from one key to another and changing between DO-RE-MI and A-B-C notations.

## Features

- Transpose chords and whole songs 
- Change chords and entire songs between DO-RE-MI and A-B-C notations
- Output chords/song following a specific target key
- Change target key part-way through a song

## Usage

### Transposing Single Chords

To transpose single chords, use `pytransposer` like this:

```python
>>> import pytransposer.transposer as tr
>>> tr.transpose_chord('Fb', 1, 'Db')
'F'
>>> tr.transpose_chord('F##', 1, 'C')
'Ab'
>>> tr.transpose_chord('F', 2, 'D', chord_style_out='doremi')
'SOL'
```

To translate chords between notations, use `pytransposer` like this:

```python
>>> from pytransposer.common import chord_doremi_to_abc
>>> chord_doremi_to_abc('MIb')
'Eb'
>>> chord_doremi_to_abc('FA##')
'F##'
```

and:

```python
>>> from pytransposer.common import chord_abc_to_doremi
>>> chord_abc_to_doremi('Eb')
'MIb'
>>> chord_abc_to_doremi('F##')
'FA##'
```

You can also use the method `pytransposer.express_chord_in_key` to express
a general chord in a given key with musical correctness:

```python
>>> express_chord_in_key('DO#', 'D#')
'C#'

>>> express_chord_in_key('DO#', 'F', chord_style_out='doremi')
'REb'
```

### Transposing Songs

Use the function `pytransposer.transpose_song` to transpose a whole song a number of half tones. You can set a target key through the `to_key` parameter so that the chords are expressed with musical correctness in that key:

```python
>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, to_key='F')
'Exa\[E/F]mple so\[Db4]ng'
```

If `to_key` is set to `'auto'`, the target key is determined automatically from the first chord of the song. 

```python	
>>> transpose_song('Exa\[RE]mple so\[Bb4]ng', 3, to_key='auto')
'Exa\[F]mple so\[Db4]ng'
```

If it is left to its default value (`None`), no specific key is targeted. Instead, the chords are expressed in their 'reference' (simplest) form.

```python	
>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3)
'Exa\[E/F]mple so\[C#4]ng'
```

You can also set the output notation style:


```python
>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, to_key='F', chord_style_out='doremi')
'Exa\[MI/FA]mple so\[REb4]ng'
```

And you can pass custom `pre_chord` and `post_chord` regex patterns to specify how you are identifying your chords:

```python
>>> transpose_song('Exa<<DO#/RE>>mple so<<Bb4>>ng', 3, to_key='F', pre_chord=r'<<', post_chord=r'>>', chord_style_out='doremi')
'Exa<<MI/FA>>mple so<<REb4>>ng'
```

The target `to_key` can also be changed at any point in the song by adding `\key{<to_key>}` whenever it should be changed (for example, `\key{DO}` or `\key{D#}`) or by adding `\key{<half_tones>}` (for example, `\key{+2}` or `\key{-5}`).

```python
>>> transpose_song('Thi\[F#]s is \key{Eb}an e\[A]xample \[F#]song')
	'Thi\[F#]s is an e\[A]xample \[Gb]song'
>>> transpose_song('Thi\[F#]s is \key{-3}an e\[A]xample \[F#]song')
	'Thi\[F#]s is an e\[A]xample \[Gb]song'
```

You can change `pre_key` and `post_key` to change the way that the key changes are indicated:

```python
>>> transpose_song('Thi\[F#]s is \|Eb|an e\[A]xample \[F#]song', 7, pre_key=r'\\|', post_key=r'\|')
'Thi\[C#]s is an e\[E]xample \[Db]song'
	
```	

By default, the function removes the key change signalling strings. You can avoid this behaviour by setting `clean_key_change_signals`
to `False`. 

```python
>>> transpose_song('Thi\[F#]s is \key{Eb}an e\[A]xample \[F#]song', 7, clean_key_change_signals=False)
'Thi\[C#]s is \key{Bb}an e\[E]xample \[Db]song'
```
	

## Settings

If you use different symbols to represent sharps and flats, you can set them in the module's configuration like this:

```python
>>> from pytransposer.config import TransposerConfig
>>> from pytransposer.transposer import transpose_song
>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, 'F')
'Exa\[E/F]mple so\[Db4]ng'
>>> TransposerConfig.sharp = 's'
>>> TransposerConfig.flat = '♭'
>>> transpose_song('Exa\[DOs/RE]mple so\[B♭4]ng', 3, 'F')
'Exa\[E/F]mple so\[D♭4]ng'
```

However, be aware that not all symbols have been tested, and setting sharps and flats to some specific characters may lead to unexpected side effects. In general, any character that is easily distinguishable from the chords should be fine.

## Example

You can see an example of the module's usage [here](example.py).

## Testing

Run unit tests using Python's `doctest`, first clone the repo:

```bash
git clone https://github.com/bfrangi/transposer.git
```

Then, open a terminal at the root directory of the repo and run:

```bash
python3 -m src.pytransposer.transposer -v  
```

and

This will run the tests for the main `transposer` sub-module. For the rest of the submodules, use:

```bash
python3 -m src.pytransposer.common -v
python3 -m src.pytransposer.config -v
```

## More info

View on the Python Package Index (PyPI) [here](https://pypi.org/project/pytransposer/).

View on GitHub [here](https://github.com/bfrangi/pytransposer/).

View the change log [here](CHANGELOG.md).