PyTransposer 
==========

[![Build Status](https://github.com/bfrangi/pytransposer/workflows/CI/badge.svg)](https://github.com/bfrangi/pytransposer/actions?query=workflow%3ACI)

Transposing chords from one key to another and changing between DO-RE-MI and A-B-C notations.


## Usage

### Single Chords

To transpose single chords, use `pytransposer` like this:

    >>> import pytransposer.transposer as tr
    >>> tr.transpose_chord('Fb', 1, 'Db')
    'F'
    >>> tr.transpose_chord('F##', 1, 'C')
    'Ab'
    >>> tr.transpose_chord('F', 2, 'D', chord_style_out='doremi')
    'SOL'

To translate chords between notations, use `pytransposer` like this:

    >>> from pytransposer.common import chord_doremi_to_abc
    >>> chord_doremi_to_abc('MIb')
    'Eb'
    >>> chord_doremi_to_abc('FA##')
    'F##'
and:

    >>> from pytransposer.common import chord_abc_to_doremi
    >>> chord_abc_to_doremi('Eb')
    'MIb'
    >>> chord_abc_to_doremi('F##')
    'FA##'

### Transposing Songs

To transpose a whole song expressing the chords in their simplest form, use `pytransposer` like this:

    >>> import pytransposer.transposer as tr
    >>> tr.standardized_transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3)
    'Exa\\[E/F]mple so\\[C#4]ng'

You can also set the output notation style:

    >>> tr.standardized_transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, chord_style_out='doremi')
    'Exa\\[MI/FA]mple so\\[DO#4]ng'

You can pass custom `pre_chord` and `post_chord` regex patterns to change the way in which you signal chords:

    >>> tr.standardized_transpose_song('Exa<<DO#/RE>>mple so<<Bb4>>ng', 3, pre_chord=r'<<', post_chord=r'>>', chord_style_out='doremi')
    'Exa<<MI/FA>>mple so<<DO#4>>ng'

You can omit the `to_key` parameter to let the function auto-detect it from the first chord:
	
	>>> transpose_song('Exa\[RE]mple so\[Bb4]ng', 3)
	'Exa\[F]mple so\[Db4]ng'

### Transposing Songs to Specific Keys

To transpose a whole song expressing the chords a specific musical key, use `pytransposer` like this:

    >>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, 'F')
    'Exa\\[E/F]mple so\\[Db4]ng'

You can also pass all the same parameters from the standardized methods to customize the behaviour of the transposer.

## Settings

If you use different symbols to represent sharps and flats, you can set them in the module's configuration like this:

    >>> from pytransposer.config import TransposerConfig
    >>> from pytransposer.transposer import transpose_song
    >>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, 'F')
    'Exa\[E/F]mple so\[Db4]ng'
    >>> TransposerConfig.sharp = 's'
    >>> transpose_song('Exa\[DOs/RE]mple so\[Bb4]ng', 3, 'F')
    'Exa\[E/F]mple so\[Db4]ng'

However, be aware that not all symbols have been tested, and setting sharps and flats to some specific characters may lead to unexpected side effects. 

## Example

You can see an example of the module's usage [here](example.py).

## Testing

Run unit tests using Python's `doctest`, first clone the repo:

    git clone https://github.com/bfrangi/transposer.git

Then, open a terminal at the root directory of the repo and run:

    python3 -m src.pytransposer.transposer -v  

and

This will run the tests for the main `transposer` sub-module. For the rest of the submodules, use:

    python3 -m src.pytransposer.common -v
    python3 -m src.pytransposer.config -v  

## More info

View on the Python Package Index (PyPI) [here](https://pypi.org/project/pytransposer/).

View on GitHub [here](https://github.com/bfrangi/pytransposer/).

View the change log [here](CHANGELOG.md).