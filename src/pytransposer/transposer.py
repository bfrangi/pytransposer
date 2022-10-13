import re
from .abc import (
	get_index_from_key as get_index_from_key_abc,
	get_key_from_index as get_key_from_index_abc,
	key_regex_str as key_regex_abc,
	abc,
	)
from .doremi import (
	get_index_from_key as get_index_from_key_doremi,
	get_key_from_index as get_key_from_index_doremi,
	key_regex_str as key_regex_doremi,
	doremi,
	)
from .common import (
	chord_doremi_to_abc,
	chord_abc_to_doremi,
	is_abc,
	is_doremi,
	)
chord_regex = re.compile(r"((?:" + key_regex_doremi + r")|(?:" + key_regex_abc + r"))")

def transpose_song(song, direction, to_key='auto', pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=abc):
	"""Transposes a song a number of half tones.
	Sharp or flat of chords depends on target key.
	
	>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, 'F')
	'Exa\\\\[E/F]mple so\\\\[Db4]ng'

	You can also set the output notation style:
	
	>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, 'F', chord_style_out='doremi')
	'Exa\\\\[MI/FA]mple so\\\\[REb4]ng'

	You can pass custom `pre_chord` and `post_chord` 
	regex patterns:
	
	>>> transpose_song('Exa<<DO#/RE>>mple so<<Bb4>>ng', 3, 'F', pre_chord=r'<<', post_chord=r'>>', chord_style_out='doremi')
	'Exa<<MI/FA>>mple so<<REb4>>ng'

	And you can omit the `to_key` parameter to let the
	function auto-detect it from the first chord:
	
	>>> transpose_song('Exa\[RE]mple so\[Bb4]ng', 3)
	'Exa\\\\[F]mple so\\\\[Db4]ng'
	"""
	chord_group_regex = re.compile(r'(' + pre_chord + r')((?:(?!' + post_chord + r').)*)(' + post_chord + r')')
	if to_key == 'auto':
		to_key = song_key(song, transpose=direction, pre_chord=pre_chord, post_chord=post_chord)
	song = chord_group_regex.sub(
		lambda m: m.group(1) + transpose_chord_group(m.group(2), direction, to_key, chord_style_out) + m.group(3),
		song
		)
	return song

def song_key(song, transpose=0, pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=abc):
	"""Gets the key of a song from its first chord and 
	transposes it a number of half tones.
	
	>>> song_key('Exa\[DO#/RE]mple so\[Bb4]ng')
	'Db'

	You can also set a number of half tones to transpose
	the song key:
	
	>>> song_key('Exa\[DO#/RE]mple so\[Bb4]ng', 2)
	'Eb'

	And you can choose the notation style of the output:
	
	>>> song_key('Exa\[DO#/RE]mple so\[Bb4]ng', 3, chord_style_out='doremi')
	'MI'
	"""
	chord_group_regex = re.compile(r'(' + pre_chord + r')((?:(?!' + post_chord + r').)*)(' + post_chord + r')')
	first_chord_group = chord_group_regex.findall(song)[0][1]
	first_chord = chord_regex.findall(first_chord_group)[0]
	key = transpose_chord(first_chord,transpose,'C', chord_style_out=chord_style_out)
	return key

def transpose_chord_group(line, direction, to_key, chord_style_out=abc):
	"""Transposes all chord matches in the string `line` 
	a given number of half tones. Sharp or flat of 
	chords depends on target key.
	
	>>> transpose_chord_group('DO#/RE', 3, 'F')
	'E/F'
	
	>>> transpose_chord_group('DO#4/RE', 3, 'F', chord_style_out='doremi')
	'MI4/FA'
	"""
	pos_difference = 0 
	for match in chord_regex.finditer(line):
		initial_pos = match.span()[0] + pos_difference
		final_pos = match.span()[1] + pos_difference
		chord = line[initial_pos:final_pos]
		transposed_chord = transpose_chord(chord, direction, to_key, chord_style_out)
		pos_difference += len(transposed_chord) - len(chord)
		line = line[0:initial_pos] + transposed_chord + line[final_pos::]
	return line

def transpose_chord(source_chord, direction, to_key, chord_style_out=abc):
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
		chord_style_in = abc
	elif is_doremi(source_chord):
		if is_doremi(to_key):
			pass
		elif is_abc(to_key):
			to_key = chord_abc_to_doremi(to_key)
		else:
			raise Exception("Invalid destination key: %s" % to_key)
		source_index = get_index_from_key_doremi(source_chord)
		k = get_key_from_index_doremi(source_index + direction, to_key)
		chord_style_in = doremi
		
	else:
		raise Exception("Invalid source chord: %s" % source_chord)

	if chord_style_out == chord_style_in:
		return k
	elif chord_style_out == abc:
		return chord_doremi_to_abc(k)
	elif chord_style_out == doremi:
		return chord_abc_to_doremi(k)
	raise Exception("Invalid output chord style: %s" % chord_style_out)


if __name__ == "__main__":
	import doctest
	doctest.testmod()