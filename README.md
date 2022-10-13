PyTransposer 
==========

[![Build Status](https://github.com/bfrangi/pytransposer/workflows/CI/badge.svg)](https://github.com/bfrangi/pytransposer/actions?query=workflow%3ACI)

Transposing chords from one key to another and changing between DO-RE-MI and A-B-C notations.


## Usage

To transpose single chords, use `pytransposer` like this:

    >>> import pytransposer.transposer as tr
    >>> tr.transpose_chord('C', 3, 'Bb')
    'Eb'
    >>> tr.transpose_chord('DO', 3, 'Bb')
    'Eb'
    >>> tr.transpose_chord('DO', 3, 'Bb', chord_style_out='doremi')
    'MIb'

To translate chords between notations, use `pytransposer` like this:

    >>> from pytransposer.common import chord_abc_to_doremi
    >>> chord_abc_to_doremi('Ab')
    'LAb'
    >>> from pytransposer.common import chord_doremi_to_abc
    >>> chord_doremi_to_abc('DO#')
    'C#'

To transpose a whole song, use `pytransposer` like this:

    >>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, 'F')
	'Exa\[E/F]mple so\[Db4]ng'
	
	>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, 'F', chord_style_out='doremi')
	'Exa\[MI/FA]mple so\[REb4]ng'
	
	>>> transpose_song('Exa<<DO#/RE>>mple so<<Bb4>>ng', 3, 'F', pre_chord=r'<<', post_chord=r'>>', chord_style_out='doremi')
	'Exa<<MI/FA>>mple so<<REb4>>ng'


## Testing

Run unit tests using Python's `doctest`, first clone the repo:

    git clone https://github.com/bfrangi/transposer.git

Then, open a terminal at the root directory of the repo and run:

    python3 -m src.pytransposer.transposer -v  

This will run the tests for the main `transposer` sub-module. For the rest of the submodules, use:

    python3 -m src.pytransposer.common -v
    python3 -m src.pytransposer.abc -v  
    python3 -m src.pytransposer.doremi -v  

## More info

View on the Python Package Index (PyPI) [here](https://pypi.org/project/pytransposer/).

View on GitHub [here](https://github.com/bfrangi/pytransposer/).

View the change log [here](CHANGELOG.md).