from pytransposer.transposer import transpose_song
from pytransposer.config import TransposerConfig
TransposerConfig.sharp = 's'
TransposerConfig.flat = '♭'

song = """
Thi\[MI]s is an example \[SI]song
W\[LA]hich is \[MI]going to be transpo\[DOsm]sed\[LA]
"""
# Auto-detect the key of the song from the first chord
transposed_song = transpose_song(song, 1, chord_style_out='doremi')
print(transposed_song)

# Change the symbol for sharps
TransposerConfig.sharp = '#'
song = """
Thi\[MI]s is an example \[SI]song
W\[LA]hich is \[MI]going to be transpo\[DO#m]sed\[LA]
"""
# Transpose to a given key
transposed_song = transpose_song(song, 1, to_key='D#', chord_style_out='abc')
print(transposed_song)
