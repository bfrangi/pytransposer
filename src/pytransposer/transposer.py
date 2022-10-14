from .config import transposer_config as config


def song_key(song, half_tones=0, pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=config.abc):
	"""
	## Description of `song_key`
	This function gets the reference key of a song from its 
	first chord and transposes it a number of half tones. We 
	assign the name of 'reference' key to the simplest expressions 
	of a particular chord. For example, the 'reference' expression
	of the key `Fb` is `E`, and for `F##` it is `G`:

	## Examples and Doctests
	>>> song_key('Exa\[Fb]mple so\[Bb4]ng')
	'E'

	>>> song_key('Exa\[F##]mple so\[Bb4]ng')
	'G'

	You can also set a number of half tones to transpose
	the song key:

	>>> song_key('Exa\[F]mple so\[Bb4]ng', 2)
	'G'

	And you can choose the notation style of the output:

	>>> song_key('Exa\[F]mple so\[Bb4]ng', 2, chord_style_out='doremi')
	'SOL'
	"""
	import re
	chord_group_regex = re.compile(
		r'(' + pre_chord + r')((?:(?!' + post_chord + r').)*)(' + post_chord + r')')
	first_chord_group = chord_group_regex.findall(song)[0][1]
	first_chord = config.get_chord_regex().findall(first_chord_group)[0]
	reference_key = config.key_to_reference(first_chord)

	transposed_reference_key = transpose_chord(
		reference_key,
		half_tones,
		chord_style_out=chord_style_out
	)

	from .common import chord_to_chord_style
	return chord_to_chord_style(transposed_reference_key, chord_style_out)


def transpose_chord(chord, half_tones, to_key=None, chord_style_out=config.abc):
	"""
	## Description of `transpose_chord`
	Transposes a chord and returns it expressed in the key given 
	through the `to_key` parameter. If `to_key` is set to `None`
	(this is the default), the chord is returned in its 'reference' 
	form, defined as the simplest expression of a particular chord. 

	## Examples and Doctests
	>>> transpose_chord('Fb', 1, 'Db')
	'F'

	>>> transpose_chord('F##', 1, 'C')
	'Ab'

	You can choose the notation style of the output:

	>>> transpose_chord('F', 2, 'D', chord_style_out='doremi')
	'SOL'

	If the `to_key` parameter is not given, the chord
	is returned in its simplest form:

	>>> transpose_chord('Fb',1)
	'F'

	>>> transpose_chord('F##', 1)
	'G#'

	>>> transpose_chord('F', 2, chord_style_out='doremi')
	'SOL'
	"""
	from .common import is_abc, is_doremi, chord_to_chord_style
	chord = config.key_to_reference(chord)
	if is_abc(chord):
		reference_keys = config.reference_abc_keys()
	elif is_doremi(chord):
		reference_keys = config.reference_doremi_keys()
	else:
		raise Exception("Invalid chord: %s" % chord)
	current_chord_index = reference_keys.index(chord)
	transposed_chord_index = (
		current_chord_index+half_tones) % len(reference_keys)
	transposed_chord = reference_keys[transposed_chord_index]
	if to_key:
		return express_chord_in_key(transposed_chord, to_key, chord_style_out)
	return chord_to_chord_style(transposed_chord, chord_style_out)


def express_chord_in_key(chord, key, chord_style_out=config.abc):
	"""
	## Description of `express_chord_in_key`
	Represents a general `chord` in a given `key`. For example,
	the chord 'C' in the key 'C' is just 'C'. However, in the 
	key of 'C#', to be musically correct, the chord 'C' is 
	represented as 'B#'.

	## Examples and Doctests
	>>> express_chord_in_key('DO#', 'D#')
	'C#'

	>>> express_chord_in_key('DO#', 'F', chord_style_out='doremi')
	'REb'
	"""
	from .common import chord_to_chord_style
	key = chord_to_chord_style(key, chord_style_out)
	chord = chord_to_chord_style(chord, chord_style_out)
	from .common import is_abc, is_doremi
	if is_abc(chord):
		reference_keys = config.reference_abc_keys()
	elif is_doremi(chord):
		reference_keys = config.reference_doremi_keys()
	else:
		raise Exception("Invalid chord: %s" % chord)
	return config.key_chords(key)[reference_keys.index(chord)]


def transpose_chord_group(line, half_tones, to_key=None, chord_style_out=config.abc):
	"""
	## Description of `transpose_chord_group`
	Transposes all chord matches in the string `line` a given number 
	of half tones, expressing all chords in the given `to_key` or in
	the 'reference' (simplest) form, if `to_key` is `None`.

	## Examples and Doctests
	>>> transpose_chord_group('DO#/RE A#', 3, to_key='D#')
	'E/E# C#'

	>>> transpose_chord_group('DO#4/RE', 3, to_key='F', chord_style_out='doremi')
	'MI4/FA'
	
	>>> transpose_chord_group('DO#/RE A#', 3)
	'E/F C#'

	>>> transpose_chord_group('DO#4/RE', 3, chord_style_out='doremi')
	'MI4/FA'
	"""
	pos_difference = 0
	for match in config.get_chord_regex().finditer(line):
		initial_pos = match.span()[0] + pos_difference
		final_pos = match.span()[1] + pos_difference
		chord = line[initial_pos:final_pos]
		transposed_chord = transpose_chord(
			chord, half_tones, to_key=to_key, chord_style_out=chord_style_out)
		pos_difference += len(transposed_chord) - len(chord)
		line = line[0:initial_pos] + transposed_chord + line[final_pos::]
	return line


def transpose_song(song, half_tones, to_key=None, pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=config.abc):
	"""
	## Description of `transpose_song`
	Transposes a song a number of half tones. If a target 
	key is given through the `to_key` parameter, the chords 
	are expressed in that key. If `to_key` is set to `'auto'`,
	the target key is determined automatically from the first
	chord of the song. If it is left to its default value (`None`),
	no specific key is targeted. Instead, the chords are expressed
	in their 'reference' (simplest) form.

	## Examples and Doctests
	>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, to_key='F')
	'Exa\\\\[E/F]mple so\\\\[Db4]ng'

	You can also set the output notation style:

	>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, to_key='F', chord_style_out='doremi')
	'Exa\\\\[MI/FA]mple so\\\\[REb4]ng'

	You can pass custom `pre_chord` and `post_chord`
	regex patterns:

	>>> transpose_song('Exa<<DO#/RE>>mple so<<Bb4>>ng', 3, to_key='F', pre_chord=r'<<', post_chord=r'>>', chord_style_out='doremi')
	'Exa<<MI/FA>>mple so<<REb4>>ng'

	And you can set `to_key` to `'auto'` to let the
	function auto-detect the key from the first chord:

	>>> transpose_song('Exa\[RE]mple so\[Bb4]ng', 3, to_key='auto')
	'Exa\\\\[F]mple so\\\\[Db4]ng'

	If you omit the parameter `to_key` (it is set to `None` by 
	default) the chords are represented in their 'reference'
	(simplest) forms:

	>>> transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3)
	'Exa\\\\[E/F]mple so\\\\[C#4]ng'
	"""
	chord_group_regex = config.get_chord_group_regex(pre_chord, post_chord)
	if to_key in ['auto']:
		to_key = song_key(
			song,
			half_tones=half_tones,
			pre_chord=pre_chord,
			post_chord=post_chord,
			chord_style_out=chord_style_out,
		)
	
	return chord_group_regex.sub(
		lambda m: m.group(1) + transpose_chord_group(m.group(2),
													 half_tones, to_key, chord_style_out) + m.group(3),
		song
	)


if __name__ == "__main__":
	import doctest
	doctest.testmod()
