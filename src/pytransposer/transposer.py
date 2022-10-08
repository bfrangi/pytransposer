from .abc import (
	get_index_from_key as get_index_from_key_abc,
	get_key_from_index as get_key_from_index_abc,
	)
from .doremi import (
	get_index_from_key as get_index_from_key_doremi,
	get_key_from_index as get_key_from_index_doremi,
	)
from .common import (
	chord_doremi_to_abc,
	chord_abc_to_doremi,
	is_abc,
	is_doremi,
	)


def transpose_chord(source_chord, direction, to_key, chord_style_out='abc'):
	"""Transposes a chord a number of half tones.
	Sharp or flat depends on target key.

	Note: Only simple chords are accepted, with 
	\# or b at most!
	
	>>> transpose_chord('C', 3, 'Bb')
	'Eb'
	
	>>> transpose_chord('DO', 3, 'Bb')
	'Eb'

	>>> transpose_chord('DO', 3, 'Bb', chord_style_out='doremi')
	'MIb'
	"""
	if is_abc(source_chord):
		if is_abc(to_key):
			pass
		elif is_doremi(to_key):
			to_key = chord_doremi_to_abc(to_key)
		else:
			raise Exception("Invalid destination key: %s" % to_key)
		source_index = get_index_from_key_abc(source_chord)
		k = get_key_from_index_abc(source_index + direction, to_key)
		chord_style_in = 'abc'
	elif is_doremi(source_chord):
		if is_doremi(to_key):
			pass
		elif is_abc(to_key):
			to_key = chord_abc_to_doremi(to_key)
		else:
			raise Exception("Invalid destination key: %s" % to_key)
		source_index = get_index_from_key_doremi(source_chord)
		k = get_key_from_index_doremi(source_index + direction, to_key)
		chord_style_in = 'doremi'
		
	else:
		raise Exception("Invalid source chord: %s" % source_chord)

	if chord_style_out == chord_style_in:
		return k
	elif chord_style_out == 'abc':
		return chord_doremi_to_abc(k)
	elif chord_style_out == 'doremi':
		return chord_abc_to_doremi(k)
	raise Exception("Invalid output chord style: %s" % chord_style_out)


if __name__ == "__main__":
    import doctest
    doctest.testmod()