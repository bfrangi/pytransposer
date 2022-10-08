PyTranspose 
==========

[![Build Status](https://github.com/bfrangi/transposer/workflows/CI/badge.svg)](https://github.com/bfrangi/transposer/actions?query=workflow%3ACI)

Transposing chords from one key to another and changing between DO-RE-MI and A-B-C notations.


## Usage

To transpose single chords, use `pytranspose` like this:

    >>> import pytranspose.transposer as tr
    >>> tr.transpose_chord('C', 3, 'Bb')
    'Eb'
    >>> tr.transpose_chord('DO', 3, 'Bb')
    'Eb'
    >>> tr.transpose_chord('DO', 3, 'Bb', chord_style_out='doremi')
    'MIb'


## Testing

Run unit tests using Python's `doctest`, first clone the repo:

    git clone https://github.com/bfrangi/transposer.git

Then, open a terminal at the root directory of the repo and run:

    python3 -m src.pytranspose.transposer -v  

This will run the tests for the main `transposer` sub-module. For the rest of the submodules, use:

    python3 -m src.pytranspose.common -v  
    python3 -m src.pytranspose.abc -v  
    python3 -m src.pytranspose.doremi -v  
