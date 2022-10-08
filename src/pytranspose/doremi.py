import re
from .common import sharp_flat
key_list = [('LA',), ('LA#', 'SIb'), ('SI',), ('DO',), ('DO#', 'REb'), ('RE',),
			('RE#', 'MIb'), ('MI',), ('FA',), ('FA#', 'SOLb'), ('SOL',), ('SOL#', 'LAb')]

sharp_flat_preferences = {
	'LA' : '#',
	'LA#': 'b',
	'SIb': 'b',
	'SI' : '#',
	'DO' : 'b',
	'DO#': 'b',
	'REb': 'b',
	'RE' : '#',
	'RE#': 'b',
	'MIb': 'b',
	'MI' : '#',
	'FA' : 'b',
	'FA#': '#',
	'SOLb': '#',
	'SOL' : '#',
	'SOL#': 'b',
	'LAb': 'b',
	}
key_regex = re.compile(r"(?:DO|RE|MI|FA|SOL|LA|SI|DO)[#b]?")


def get_index_from_key(source_key):
	"""Gets the internal index of a key
	>>> get_index_from_key('SIb')
	1
	"""
	for key_names in key_list:
		if source_key in key_names:
			return key_list.index(key_names)
	raise Exception("Invalid key: %s" % source_key)

def get_key_from_index(index, to_key):
	"""Gets the key at the given internal index.
	Sharp or flat depends on the target key.
	>>> get_key_from_index(1, 'MIb')
	'SIb'
	"""
	key_names = key_list[index % len(key_list)]
	if len(key_names) > 1:
		sharp_or_flat = sharp_flat.index(sharp_flat_preferences[to_key])
		return key_names[sharp_or_flat]
	return key_names[0]


def get_transponation_steps(source_key, target_key):
	"""Gets the number of half tones to transpose
	>>> get_transponation_steps('RE', 'DO')
	-2
	"""
	source_index = get_index_from_key(source_key)
	target_index = get_index_from_key(target_key)
	return target_index - source_index


if __name__ == "__main__":
    import doctest
    doctest.testmod()