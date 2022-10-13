import re
from .common import sharp_flat, sharp, flat
key_list = [('A',), ('A'+sharp, 'B'+flat), ('B',), ('C',), ('C'+sharp, 'D'+flat), ('D',),
			('D'+sharp, 'E'+flat), ('E',), ('F',), ('F'+sharp, 'G'+flat), ('G',), ('G'+sharp, 'A'+flat)]
abc = 'abc'
sharp_flat_preferences = {
	'A' : sharp,
	'A'+sharp: flat,
	'B'+flat: flat,
	'B' : sharp,
	'C' : flat,
	'C'+sharp: flat,
	'D'+flat: flat,
	'D' : sharp,
	'D'+sharp: flat,
	'E'+flat: flat,
	'E' : sharp,
	'F' : flat,
	'F'+sharp: sharp,
	'G'+flat: sharp,
	'G' : sharp,
	'G'+sharp: flat,
	'A'+flat: flat,
	}
key_regex_str = r"[ABCDEFG][" + sharp + flat + r"]?"
key_regex = re.compile(key_regex_str)

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