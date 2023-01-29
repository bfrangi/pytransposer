from .config import transposer_config as config
from .common import chord_to_chord_style


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

	If the song has no chords, `None` is returned:

	>>> song_key('Example song', 2, chord_style_out='doremi') is None
	True
	"""
	import re
	chord_group_regex = re.compile(
		r'(' + pre_chord + r')((?:(?!' + post_chord + r').)*)(' + post_chord + r')')
	
	first_chord_group = chord_group_regex.findall(song)
	if not len(first_chord_group) > 0:
		return 
	first_chord_group = first_chord_group[0][1]
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

	>>> express_chord_in_key('SI', 'SOL#', 'doremi')
	'SI'
	"""
	from .common import chord_to_chord_style
	key = chord_to_chord_style(key, chord_style_out)
	chord = chord_to_chord_style(chord, chord_style_out)
	if chord_style_out == config.abc:
		reference_keys = config.reference_abc_keys()
	elif chord_style_out == config.doremi:
		reference_keys = config.reference_doremi_keys()
	else:
		raise Exception("Invalid chord: %s" % chord)
	idx = reference_keys.index(chord)
	return config.key_chords(key)[idx]


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


def process_key_change(current_key, to_key, half_tones=0, chord_style_out=config.abc):
	"""
	## Description of `process_key_change`
	Returns a new key given an input key `current_key` and an a value
	`to_key` which can either be an offset (amount of half-tones to 
	transpose `current_key`) or directly output key. All output keys are
	expressed in the notation according to `chord_style_out`.

	## Examples and Doctests
	>>> process_key_change('DO', ' -3 ')
	'A'

	>>> process_key_change('DO', 'SOL')
	'G'
	"""
	import re
	number_format_key_change = re.search(r'(\+||\-)([0-9]+)', to_key)
	if number_format_key_change:
		offset = int(number_format_key_change.group(0))
		to_key = transpose_chord(current_key, offset)
	return transpose_chord(config.key_to_reference(to_key), half_tones, chord_style_out=chord_style_out)
	

def song_key_segments(song, to_key, half_tones=0, clean=True, chord_style_out=config.abc, pre_key = r'\\key\{', post_key = r'\}'):
	"""
	## Description of `song_key_segments`
	If the song has changes in key, `song_key_segments` returns a list 
	of dictionaries containing each segment and the corresponding key 
	(both transposed by an offset of `half_tones`). The function 
	returns `None` if the song has no changes in key.

	If `clean` is `True`, the key change patterns are removed.

	## Examples and Doctests
	>>> song_key_segments('Thi\[C]s is \key{SIb}an e\[A]xample \[C]song', to_key='D#')
	[{'content': 'Thi\\\\[C]s is ', 'prepend': '', 'to_key': 'Eb'}, {'content': 'an e\\\\[A]xample \\\\[C]song', 'prepend': '', 'to_key': 'Bb'}]
	
	>>> song_key_segments('Thi\[C]s is \key{-1}an e\[A]xample \[C]song', to_key='D#', half_tones=1)
	[{'content': 'Thi\\\\[C]s is ', 'prepend': '', 'to_key': 'E'}, {'content': 'an e\\\\[A]xample \\\\[C]song', 'prepend': '', 'to_key': 'Eb'}]
	
	>>> song_key_segments('Thi\[C]s is \key{-1}an e\[A]xample \key{D#}\[C]song', to_key='D#')
	[{'content': 'Thi\\\\[C]s is ', 'prepend': '', 'to_key': 'Eb'}, {'content': 'an e\\\\[A]xample ', 'prepend': '', 'to_key': 'D'}, {'content': '\\\\[C]song', 'prepend': '', 'to_key': 'Eb'}]
	
	>>> song_key_segments('Thi\[C]s is \key{-1}an e\[A]xample \key{D#}\[C]song', to_key='D#', clean=False)
	[{'content': 'Thi\\\\[C]s is ', 'prepend': '', 'to_key': 'Eb'}, {'content': 'an e\\\\[A]xample ', 'prepend': '\\\\key{D}', 'to_key': 'D'}, {'content': '\\\\[C]song', 'prepend': '\\\\key{Eb}', 'to_key': 'Eb'}]
	
	>>> song_key_segments('Thi\[C]s is an e\[A]xample \[C]song', to_key='D#') is None
	True
	"""
	# Check if there are any changes in key within the song
	import re
	key_change_regex = re.compile(
		r'(' + pre_key + r')((?:(?!' + post_key + r').)*)(' + post_key + r')')
	key_change_matches = key_change_regex.finditer(song)
	key_change_matches = [m for m in key_change_matches]

	# If there are changes in key within the song, create a list
	# containing dictionaries with the song segments and the
	# corresponding `to_key`
	if key_change_matches:
		song_segments = []
		first_match = key_change_matches[0]
		pre_key_str = first_match.group(1)
		post_key_str = first_match.group(3)

		# Store from the beginning of the song to the first change
		# in key
		song_segments.append({
			'content': song[0:first_match.start()],
			'prepend': '',
			'to_key': process_key_change(
				to_key, 
				to_key,
				half_tones=half_tones,
				chord_style_out=chord_style_out
				)
		})

		# Store middle segments of the song
		idx = first_match.end()
		for i in range(len(key_change_matches) - 1):
			processed_to_key = process_key_change(
				to_key, 
				key_change_matches[i].group(2), 
				half_tones=half_tones,
				chord_style_out=chord_style_out
				)	
			key_change_signal_str = pre_key_str + processed_to_key + post_key_str if not clean else ''
			song_segments.append({
				'content': song[idx:key_change_matches[i+1].start()],
				'prepend': key_change_signal_str,
				'to_key': processed_to_key
			})
			idx = key_change_matches[i+1].end()
			
		# Store from the last change in key to the end of the song
		if len(key_change_matches) > 0:
			last_match = key_change_matches[-1]
			processed_to_key = process_key_change(
				to_key, 
				last_match.group(2),
				half_tones=half_tones,
				chord_style_out=chord_style_out
				)
			key_change_signal_str = pre_key_str + processed_to_key + post_key_str if not clean else ''
			song_segments.append({
				'content': song[idx:len(song)],
				'prepend': key_change_signal_str,
				'to_key': processed_to_key
			})
		return song_segments
	# If there are no changes in key, return `None`
	return None
	

def transpose_song(song, half_tones=0, to_key=None, pre_chord=r'\\\[', post_chord=r'\]', chord_style_out=config.abc, 	pre_key = r'\\key\{', post_key = r'\}', clean_key_change_signals=True):
	"""
	## Description of `transpose_song`
	Transposes a song a number of half tones. If a target 
	key is given through the `to_key` parameter, the chords 
	are expressed in that key. If `to_key` is set to `'auto'`,
	the target key is determined automatically from the first
	chord of the song. If it is left to its default value (`None`),
	no specific key is targeted. Instead, the chords are expressed
	in their 'reference' (simplest) form.

	The target `to_key` can also be changed at any point in the 
	song by adding `\key{<to_key>}` whenever it should be changed 
	(for example, `\key{DO}` or `\key{D#}`).

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

	You can change the target key at any point by adding 
	`\key{<to_key>}` or `\key{<half_tones>}` within the song:

	>>> transpose_song('Thi\[F#]s is \key{Eb}an e\[A]xample \[F#]song')
	'Thi\\\\[F#]s is an e\\\\[A]xample \\\\[Gb]song'

	>>> transpose_song('Thi\[F#]s is \key{-3}an e\[A]xample \[F#]song')
	'Thi\\\\[F#]s is an e\\\\[A]xample \\\\[Gb]song'

	You can change `pre_key` and `post_key` to change the way that the
	key changes are indicated:

	>>> transpose_song('Thi\[F#]s is \|Eb|an e\[A]xample \[F#]song', 7, pre_key=r'\\\\\|', post_key=r'\|')
	'Thi\\\\[C#]s is an e\\\\[E]xample \\\\[Db]song'
	
	By default, the function removes the key change signalling strings.
	You can avoid this behaviour by setting `clean_key_change_signals`
	to `False`. 

	>>> transpose_song('Thi\[F#]s is \key{Eb}an e\[A]xample \[F#]song', 7, clean_key_change_signals=False)
	'Thi\\\\[C#]s is \\\\key{Bb}an e\\\\[E]xample \\\\[Db]song'
	"""
	# Get auto to_key without transposing it
	chord_group_regex = config.get_chord_group_regex(pre_chord, post_chord)
	auto_to_key_no_transpose = song_key(
		song,
		half_tones=0,
		pre_chord=pre_chord,
		post_chord=post_chord,
		chord_style_out=chord_style_out,
	)
	# Process songs with changes in key
	song_segments = song_key_segments(
		song, 
		to_key=auto_to_key_no_transpose, 
		half_tones=half_tones,
		clean=clean_key_change_signals,
		chord_style_out=chord_style_out, 
		pre_key = pre_key,
		post_key = post_key
	)
	if song_segments:
		return ''.join([
			song_segment['prepend'] + 
			transpose_song(
				song_segment['content'], 
				half_tones, 
				to_key=song_segment['to_key'],
				pre_chord=pre_chord,
				post_chord=post_chord,
				chord_style_out=chord_style_out
			) for song_segment in song_segments
		])
	
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
