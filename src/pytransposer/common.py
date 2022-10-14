from .config import transposer_config as config
abc_to_doremi_dictionary = {
	'A' : 'LA',
	'B' : 'SI',
	'C' : 'DO',
	'D' : 'RE',
	'E' : 'MI',
	'F' : 'FA',
	'G' : 'SOL',
	}
doremi_to_abc_dictionary = { 
	abc_to_doremi_dictionary[chord]: chord for chord in abc_to_doremi_dictionary
	}


def is_abc(chord):
	"""Returns True if a chord is in the A-B-C notation.
	False is returned otherwise.
	>>> is_abc('Eb')
	True

	>>> is_abc('FA')
	False
	"""
	import re
	return re.sub(r'[' + config.sharp + config.flat + r']', '', chord) in abc_to_doremi_dictionary


def is_doremi(chord):
	"""Returns True if a chord is in the DO-RE-MI notation.
	False is returned otherwise.
	>>> is_doremi('Eb')
	False

	>>> is_doremi('FA')
	True
	"""
	import re
	return re.sub(r'[' + config.sharp + config.flat + r']', '', chord) in doremi_to_abc_dictionary


def chord_style(chord):
	"""Returns the style of the a given chord.
	Possible styles are A-B-C and DO-RE-MI.
	>>> chord_style('Eb')
	'abc'

	>>> chord_style('FA')
	'doremi'
	"""
	if is_abc(chord):	
		return config.abc
	elif is_doremi(chord):
		return config.doremi
	raise Exception("Invalid chord: %s" % chord)


def chord_doremi_to_abc(chord):
	"""Converts a chord from DO-RE-MI to A-B-C notation.
	>>> chord_doremi_to_abc('MIb')
	'Eb'
	>>> chord_doremi_to_abc('FA##')
	'F##'
	"""
	import re
	if is_doremi(chord):
		sharp_flat = re.findall(r'[' + config.sharp + config.flat + r']', chord)
		clean_chord = re.sub(r'[' + config.sharp + config.flat + r']','', chord)
		translated_chord = doremi_to_abc_dictionary[clean_chord]
		for sf in sharp_flat:
			translated_chord += sf
		return translated_chord
	raise Exception("Invalid chord: %s" % chord)


def chord_abc_to_doremi(chord):
	"""Converts a chord from A-B-C to DO-RE-MI notation.
	>>> chord_abc_to_doremi('Eb')
	'MIb'
	>>> chord_abc_to_doremi('F##')
	'FA##'
	"""
	import re
	if is_abc(chord):
		sharp_flat = re.findall(r'[' + config.sharp + config.flat + r']', chord)
		clean_chord = re.sub(r'[' + config.sharp + config.flat + r']','', chord)
		translated_chord = abc_to_doremi_dictionary[clean_chord]
		for sf in sharp_flat:
			translated_chord += sf
		return translated_chord
	raise Exception("Invalid chord: %s" % chord)


def chord_to_chord_style(chord, chord_style_out=config.abc):
	"""Converts a chord from any notation to a chosen
	notation (either A-B-C or DO-RE-MI).
	>>> chord_to_chord_style('Eb', 'doremi')
	'MIb'
	>>> chord_to_chord_style('G', 'abc')
	'G'
	>>> chord_to_chord_style('DO', 'doremi')
	'DO'
	"""
	if chord_style_out == chord_style(chord):
		return chord
	elif chord_style_out == config.abc:
		return chord_doremi_to_abc(chord)
	elif chord_style_out == config.doremi:
		return chord_abc_to_doremi(chord)
	raise Exception("Invalid output chord style: %s" % chord_style_out)


if __name__ == "__main__":
    import doctest
    doctest.testmod()