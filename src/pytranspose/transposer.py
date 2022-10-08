from .abc import (
	# key_regex as key_regex_abc,
	get_index_from_key as get_index_from_key_abc,
	get_key_from_index as get_key_from_index_abc,
	)
from .doremi import (
	# key_regex as key_regex_doremi,
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
		source_index = get_index_from_key_abc(source_chord)
		k = get_key_from_index_abc(source_index + direction, to_key)
		chord_style_in = 'abc'
	elif is_doremi(source_chord):
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




# def transpose_line(source_line, direction, to_key, chord_style_in='abc', chord_style_out='abc'):
# 	"""Transposes a line a number of keys if it starts with a pipe. Examples:
# 	>>> transpose_line('| A | A# | Bb | C#m7/F# |', -2, 'C')
# 	'| G | Ab | Ab | Bm7/E |'

# 	Different keys will be sharp or flat depending on target key.
# 	>>> transpose_line('| A | A# | Bb | C#m7/F# |', -2, 'D')
# 	'| G | G# | G# | Bm7/E |'

# 	It will use the more common key if sharp/flat, for example F# instead of Gb.
# 	>>> transpose_line('| Gb |', 0, 'Gb')
# 	'| F# |'

# 	Lines not starting with pipe will not be transposed
# 	>>> transpose_line('A | Bb |', -2, 'C')
# 	'A | Bb |'
# 	"""
# 	if source_line[0] != '|':
# 		return source_line
# 	if chord_style_in == 'abc':
# 		source_chords = key_regex_abc.findall(source_line)
# 	elif chord_style_in == 'doremi':
# 		source_chords = key_regex_doremi.findall(source_line)
# 		source_chords = [chord_doremi_to_abc(chord) for chord in source_chords]
# 		source_line = key_regex_doremi.sub(lambda x: chord_doremi_to_abc(x.group()),source_line)
# 	else:
# 		raise Exception("Invalid input chord style: %s" % chord_style_in)
# 	return recursive_line_transpose(source_line, source_chords, direction, to_key, chord_style_out)
	

	
# def recursive_line_transpose(source_line, source_chords, direction, to_key, chord_style_out='abc'):
# 	"""Transposes a line of chords.
# 	>>> recursive_line_transpose('| A | B | G#m4 |', ['A', 'B', 'G#'], 3, 'C', chord_style_out='doremi')
# 	'| DO | RE | SIm4 |'
# 	"""
# 	if not source_chords or not source_line:
# 		return source_line
# 	source_chord = source_chords.pop(0)
# 	chord_index = source_line.find(source_chord)
# 	after_chord_index = chord_index + len(source_chord)
# 	return source_line[:chord_index] + \
# 		   transpose_chord(source_chord, direction, to_key, chord_style_out) + \
# 		   recursive_line_transpose(source_line[after_chord_index:], source_chords, direction, to_key, chord_style_out)




