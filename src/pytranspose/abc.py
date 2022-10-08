import re
from .common import sharp_flat
key_list = [('A',), ('A#', 'Bb'), ('B',), ('C',), ('C#', 'Db'), ('D',),
			('D#', 'Eb'), ('E',), ('F',), ('F#', 'Gb'), ('G',), ('G#', 'Ab')]

sharp_flat_preferences = {
	'A' : '#',
	'A#': 'b',
	'Bb': 'b',
	'B' : '#',
	'C' : 'b',
	'C#': 'b',
	'Db': 'b',
	'D' : '#',
	'D#': 'b',
	'Eb': 'b',
	'E' : '#',
	'F' : 'b',
	'F#': '#',
	'Gb': '#',
	'G' : '#',
	'G#': 'b',
	'Ab': 'b',
	}
key_regex = re.compile(r"[ABCDEFG][#b]?")


def get_index_from_key(source_key):
	"""Gets the internal index of a key
	>>> get_index_from_key('Bb')
	1
	"""
	for key_names in key_list:
		if source_key in key_names:
			return key_list.index(key_names)
	raise Exception("Invalid key: %s" % source_key)


def get_key_from_index(index, to_key):
	"""Gets the key at the given internal index.
	Sharp or flat depends on the target key.
	>>> get_key_from_index(1, 'Eb')
	'Bb'
	"""
	key_names = key_list[index % len(key_list)]
	if len(key_names) > 1:
		sharp_or_flat = sharp_flat.index(sharp_flat_preferences[to_key])
		return key_names[sharp_or_flat]
	return key_names[0]


def get_transponation_steps(source_key, target_key):
	"""Gets the number of half tones to transpose
	>>> get_transponation_steps('D', 'C')
	-2
	"""
	source_index = get_index_from_key(source_key)
	target_index = get_index_from_key(target_key)
	return target_index - source_index


if __name__ == "__main__":
    import doctest
    doctest.testmod()