from .config import transposer_config as config

# STANDARDIZED (SIMPLEST-EXPRESSION) TRANPOSER


def standardized_song_key(song, half_tones=0, pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=config.abc):
	"""Gets the standard key of a song from its first chord 
	and transposes it a number of half tones. We assign the 
	name of 'standard' key to the simplest expressions of a 
	particular chord. For example, the 'standard' expression
	of the key `Fb` is `E`, and for `F##` it is `G`:

	>>> standardized_song_key('Exa\[Fb]mple so\[Bb4]ng')
	'E'

	>>> standardized_song_key('Exa\[F##]mple so\[Bb4]ng')
	'G'

	You can also set a number of half tones to transpose
	the song key:

	>>> standardized_song_key('Exa\[F]mple so\[Bb4]ng', 2)
	'G'

	And you can choose the notation style of the output:

	>>> standardized_song_key('Exa\[F]mple so\[Bb4]ng', 2, chord_style_out='doremi')
	'SOL'
	"""
	import re
	chord_group_regex = re.compile(
		r'(' + pre_chord + r')((?:(?!' + post_chord + r').)*)(' + post_chord + r')')
	first_chord_group = chord_group_regex.findall(song)[0][1]
	first_chord = config.get_chord_regex().findall(first_chord_group)[0]
	standard_key = config.key_to_standard(first_chord)

	transposed_standard_key = standardized_transpose_chord(
		standard_key,
		half_tones=half_tones,
		chord_style_out=chord_style_out
	)

	from .common import chord_to_chord_style
	return chord_to_chord_style(transposed_standard_key, chord_style_out)


def standardized_transpose_chord(chord, half_tones, chord_style_out=config.abc):
	"""Transposes a chord and returns it in the standard
	form. We give the name of 'standard' key to the simplest 
	expressions of a particular chord. For example, the 
	'standard' expression of the key `Fb` is `E`, for 
	`F##` it is `G` and for `D#` it is `Eb`:

	>>> standardized_transpose_chord('Fb',1)
	'F'

	>>> standardized_transpose_chord('F##', 1)
	'G#'

	You can choose the notation style of the output:

	>>> standardized_transpose_chord('F', 2, chord_style_out='doremi')
	'SOL'
	"""
	from .common import is_abc, is_doremi, chord_to_chord_style
	chord = config.key_to_standard(chord)
	if is_abc(chord):
		standard_keys = config.standard_abc_keys()
	elif is_doremi(chord):
		standard_keys = config.standard_doremi_keys()
	else:
		raise Exception("Invalid chord: %s" % chord)
	current_chord_index = standard_keys.index(chord)
	transposed_chord_index = (
		current_chord_index+half_tones) % len(standard_keys)
	transposed_chord = standard_keys[transposed_chord_index]
	return chord_to_chord_style(transposed_chord, chord_style_out)


def standardized_transpose_chord_group(line, half_tones, chord_style_out=config.abc):
	"""Transposes all chord matches in the string `line` 
	a given number of half tones, expressing all chords 
	in their 'standard' (simplest) form.

	>>> standardized_transpose_chord_group('DO#/RE A#', 3)
	'E/F C#'

	>>> standardized_transpose_chord_group('DO#4/RE', 3, chord_style_out='doremi')
	'MI4/FA'
	"""
	pos_difference = 0
	for match in config.get_chord_regex().finditer(line):
		initial_pos = match.span()[0] + pos_difference
		final_pos = match.span()[1] + pos_difference
		chord = line[initial_pos:final_pos]
		transposed_chord = standardized_transpose_chord(
			chord, half_tones, chord_style_out)
		pos_difference += len(transposed_chord) - len(chord)
		line = line[0:initial_pos] + transposed_chord + line[final_pos::]
	return line


def standardized_transpose_song(song, half_tones, pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=config.abc):
	"""Transposes a song a number of half tones, 
	expressing all chords in their 'standard' (simplest)
	form.

	>>> standardized_transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3)
	'Exa\\\\[E/F]mple so\\\\[C#4]ng'

	You can also set the output notation style:

	>>> standardized_transpose_song('Exa\[DO#/RE]mple so\[Bb4]ng', 3, chord_style_out='doremi')
	'Exa\\\\[MI/FA]mple so\\\\[DO#4]ng'

	You can pass custom `pre_chord` and `post_chord` 
	regex patterns:

	>>> standardized_transpose_song('Exa<<DO#/RE>>mple so<<Bb4>>ng', 3, pre_chord=r'<<', post_chord=r'>>', chord_style_out='doremi')
	'Exa<<MI/FA>>mple so<<DO#4>>ng'
	"""
	chord_group_regex = config.get_chord_group_regex(pre_chord, post_chord)
	return chord_group_regex.sub(
		lambda m: m.group(1) + standardized_transpose_chord_group(m.group(2),
																  half_tones, chord_style_out) + m.group(3),
		song
	)


# KEY-SPECIFIC TRANSPOSER


def song_key(song, half_tones=0, pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=config.abc):
	"""Gets the standard key of a song from its first chord 
	and transposes it a number of half tones. We assign the 
	name of 'standard' key to the simplest expressions of a 
	particular chord. For example, the 'standard' expression
	of the key `Fb` is `E`, and for `F##` it is `G`:

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
	return standardized_song_key(song, half_tones, pre_chord, post_chord, chord_style_out)


def transpose_chord(chord, half_tones, to_key, chord_style_out=config.abc):
	"""Transposes a chord and returns it expressed
	in the `to_key`.

	>>> transpose_chord('Fb', 1, 'Db')
	'F'

	>>> transpose_chord('F##', 1, 'C')
	'Ab'

	You can choose the notation style of the output:

	>>> transpose_chord('F', 2, 'D', chord_style_out='doremi')
	'SOL'
	"""
	from .common import chord_to_chord_style
	to_key = chord_to_chord_style(to_key, chord_style_out)
	key_chords = config.key_chords(to_key)
	standardized_transposed_chord = standardized_transpose_chord(
		chord, half_tones, chord_style_out)
	from .common import is_abc, is_doremi
	if is_abc(standardized_transposed_chord):
		standard_keys = config.standard_abc_keys()
	elif is_doremi(standardized_transposed_chord):
		standard_keys = config.standard_doremi_keys()
	else:
		raise Exception("Invalid chord: %s" % standardized_transposed_chord)
	idx = standard_keys.index(standardized_transposed_chord)
	to_key_transposed_chord = key_chords[idx]
	return to_key_transposed_chord


def transpose_chord_group(line, half_tones, to_key, chord_style_out=config.abc):
	"""Transposes all chord matches in the string `line` 
	a given number of half tones, expressing all chords 
	in the given `to_key`.

	>>> transpose_chord_group('DO#/RE A#', 3, to_key='D#')
	'E/E# C#'

	>>> transpose_chord_group('DO#4/RE', 3, to_key='F', chord_style_out='doremi')
	'MI4/FA'
	"""
	pos_difference = 0
	for match in config.get_chord_regex().finditer(line):
		initial_pos = match.span()[0] + pos_difference
		final_pos = match.span()[1] + pos_difference
		chord = line[initial_pos:final_pos]
		transposed_chord = transpose_chord(
			chord, half_tones, to_key, chord_style_out)
		pos_difference += len(transposed_chord) - len(chord)
		line = line[0:initial_pos] + transposed_chord + line[final_pos::]
	return line


def transpose_song(song, half_tones, to_key='auto', pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=config.abc):
	"""Transposes a song a number of half tones. Sharp or flat
	of chords depends on the target key (`to_key`). If it is set 
	to `'auto'`, it is determined automatically from the first chord
	of the song.

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
	chord_group_regex = config.get_chord_group_regex(pre_chord, post_chord)
	if to_key == 'auto':
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
