import re
sharp_flat = ['#', 'b']
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
	return re.sub(r'[b\#]', '', chord) in abc_to_doremi_dictionary


def is_doremi(chord):
	"""Returns True if a chord is in the DO-RE-MI notation.
	False is returned otherwise.
	>>> is_doremi('Eb')
	False

	>>> is_doremi('FA')
	True
	"""
	return re.sub(r'[b\#]', '', chord) in doremi_to_abc_dictionary


def chord_doremi_to_abc(chord):
	"""Converts a chord from DO-RE-MI to A-B-C notation.
	>>> chord_doremi_to_abc('MIb')
	'Eb'
	"""
	if is_doremi(chord):
		sharp_flat = re.findall(r'[b\#]', chord)
		clean_chord = re.sub(r'[b\#]','', chord)
		translated_chord = doremi_to_abc_dictionary[clean_chord]
		for sf in sharp_flat:
			translated_chord += sf
		return translated_chord
	raise Exception("Invalid chord: %s" % chord)


def chord_abc_to_doremi(chord):
	"""Converts a chord from A-B-C to DO-RE-MI notation.
	>>> chord_abc_to_doremi('Eb')
	'MIb'
	"""
	if is_abc(chord):
		sharp_flat = re.findall(r'[b\#]', chord)
		clean_chord = re.sub(r'[b\#]','', chord)
		translated_chord = abc_to_doremi_dictionary[clean_chord]
		for sf in sharp_flat:
			translated_chord += sf
		return translated_chord
	raise Exception("Invalid chord: %s" % chord)

if __name__ == "__main__":
    import doctest
    doctest.testmod()