import re
class TransposerConfig():
	sharp = '#'
	flat = 'b'
	abc = 'abc'
	doremi = 'doremi'

	# REGEX PATTERNS

	def get_key_regex_abc(self):
		return r"[ABCDEFG][" + self.sharp + self.flat + r"]{0,2}"
	
	def get_key_regex_doremi(self):
		return r"(?:DO|RE|MI|FA|SOL|LA|SI|DO)[" + self.sharp + self.flat + r"]{0,2}"

	def get_chord_regex(self):
		return re.compile(r"((?:" + self.get_key_regex_doremi() + r")|(?:" + self.get_key_regex_abc() + r"))")
	
	def get_chord_group_regex(self, pre_chord, post_chord):
		return re.compile(r'(' + pre_chord + r')((?:(?!' + post_chord + r').)*)(' + post_chord + r')')

	# DEFINITION OF STANDARD KEYS

	def sharp_flat(self):
		return [self.sharp, self.flat]
	
	def reference_abc_keys(self):
		return [
			'C', 
			'C'+self.sharp, 
			'D', 
			'E'+self.flat, 
			'E', 
			'F', 
			'F'+self.sharp, 
			'G', 
			'G'+self.sharp, 
			'A', 
			'B'+self.flat, 
			'B'
			]
	
	def reference_doremi_keys(self):
		return [
			'DO', 
			'DO'+self.sharp, 
			'RE', 
			'MI'+self.flat, 
			'MI', 
			'FA', 
			'FA'+self.sharp, 
			'SOL', 
			'SOL'+self.sharp, 
			'LA', 
			'SI'+self.flat, 
			'SI'
			]
	
	# STANDARDIZING KEYS/CHORDS

	def key_to_reference_abc(self, key):
		keys = {
			'C':'C',
			'D':'D',
			'E':'E',
			'F':'F',
			'G':'G',
			'A':'A',
			'B':'B',

			'C'+self.sharp:'C'+self.sharp,
			'D'+self.sharp:'E'+self.flat,
			'E'+self.sharp:'F',
			'F'+self.sharp:'F'+self.sharp,
			'G'+self.sharp:'G'+self.sharp,
			'A'+self.sharp:'B'+self.flat,
			'B'+self.sharp:'C',

			'C'+self.flat:'B',
			'D'+self.flat:'C'+self.sharp,
			'E'+self.flat:'E'+self.flat,
			'F'+self.flat:'E',
			'G'+self.flat:'F'+self.sharp,
			'A'+self.flat:'G'+self.sharp,
			'B'+self.flat:'B'+self.flat,

			'C'+self.sharp+self.sharp:'D',
			'D'+self.sharp+self.sharp:'E', # Theoretical
			'E'+self.sharp+self.sharp:'F'+self.sharp, # Theoretical
			'F'+self.sharp+self.sharp:'G',
			'G'+self.sharp+self.sharp:'A',
			'A'+self.sharp+self.sharp:'B', # Theoretical
			'B'+self.sharp+self.sharp:'C'+self.sharp, # Theoretical
			
			'C'+self.flat+self.flat:'B'+self.flat, # Theoretical
			'D'+self.flat+self.flat:'C', # Theoretical
			'E'+self.flat+self.flat:'D',
			'F'+self.flat+self.flat:'E'+self.flat, # Theoretical
			'G'+self.flat+self.flat:'F', # Theoretical
			'A'+self.flat+self.flat:'G', # Theoretical
			'B'+self.flat+self.flat:'A',
		}
		try:
			return keys[key]
		except:
			raise Exception("Invalid key: %s" % key)
	
	def key_to_reference_doremi(self, key):
		keys = {
			'DO':'DO',
			'RE':'RE',
			'MI':'MI',
			'FA':'FA',
			'SOL':'SOL',
			'LA':'LA',
			'SI':'SI',

			'DO'+self.sharp:'DO'+self.sharp,
			'RE'+self.sharp:'MI'+self.flat,
			'MI'+self.sharp:'FA',
			'FA'+self.sharp:'FA'+self.sharp,
			'SOL'+self.sharp:'SOL'+self.sharp,
			'LA'+self.sharp:'SI'+self.flat,
			'SI'+self.sharp:'DO',

			'DO'+self.flat:'SI',
			'RE'+self.flat:'DO'+self.sharp,
			'MI'+self.flat:'MI'+self.flat,
			'FA'+self.flat:'MI',
			'SOL'+self.flat:'FA'+self.sharp,
			'LA'+self.flat:'SOL'+self.sharp,
			'SI'+self.flat:'SI'+self.flat,

			'DO'+self.sharp+self.sharp:'RE',
			'RE'+self.sharp+self.sharp:'MI', # Theoretical
			'MI'+self.sharp+self.sharp:'FA'+self.sharp, # Theoretical
			'FA'+self.sharp+self.sharp:'SOL',
			'SOL'+self.sharp+self.sharp:'LA',
			'LA'+self.sharp+self.sharp:'SI', # Theoretical
			'SI'+self.sharp+self.sharp:'DO'+self.sharp, # Theoretical
			
			'DO'+self.flat+self.flat:'SI'+self.flat, # Theoretical
			'RE'+self.flat+self.flat:'DO', # Theoretical
			'MI'+self.flat+self.flat:'RE',
			'FA'+self.flat+self.flat:'MI'+self.flat, # Theoretical
			'SOL'+self.flat+self.flat:'FA', # Theoretical
			'LA'+self.flat+self.flat:'SOL', # Theoretical
			'SI'+self.flat+self.flat:'LA',
		}
		try:
			return keys[key]
		except:
			raise Exception("Invalid key: %s" % key)

	def key_to_reference(self, key):
		from .common import is_abc, is_doremi
		if is_abc(key):
			return self.key_to_reference_abc(key)
		elif is_doremi(key):
			return self.key_to_reference_doremi(key)
		raise Exception("Invalid key: %s" % key)

	# SCALES

	def key_chords_abc(self, key):
		keys = {'C': ['C', 'C'+self.sharp, 'D', 'E'+self.flat, 'E', 'F', 'F'+self.sharp, 'G', 'A'+self.flat, 'A', 'B'+self.flat, 'B'],
			'C'+self.sharp: ['B'+self.sharp, 'C'+self.sharp, 'D', 'D'+self.sharp, 'E', 'E'+self.sharp, 'F'+self.sharp, 'G', 'G'+self.sharp, 'A', 'A'+self.sharp, 'B'],
			'D'+self.flat: ['C', 'D'+self.flat, 'D', 'E'+self.flat, 'F'+self.flat, 'F', 'G'+self.flat, 'G', 'A'+self.flat, 'B'+self.flat+self.flat, 'C'+self.flat],
			'D': ['C', 'C'+self.sharp, 'D', 'E'+self.flat, 'E', 'F', 'F'+self.sharp, 'G', 'G'+self.sharp, 'A', 'B'+self.flat, 'B'],
			'D'+self.sharp: ['B'+self.sharp, 'C'+self.sharp, 'C'+self.sharp+self.sharp, 'D'+self.sharp, 'E', 'E'+self.sharp, 'F'+self.sharp, 'F'+self.sharp+self.sharp, 'G'+self.sharp, 'A', 'A'+self.sharp, 'B'],
			'E'+self.flat: ['C', 'D'+self.flat, 'D', 'E'+self.flat, 'E', 'F', 'G'+self.flat, 'G', 'A'+self.flat, 'A', 'B'+self.flat, 'C'+self.flat],
			'E': ['C', 'C'+self.sharp, 'D', 'D'+self.sharp, 'E', 'F', 'F'+self.sharp, 'G', 'G'+self.sharp, 'A', 'B'+self.flat, 'B'],
			'F': ['C', 'D'+self.flat, 'D', 'E'+self.flat, 'E', 'F', 'F'+self.sharp, 'G', 'A'+self.flat, 'A', 'B'+self.flat, 'B'],
			'F'+self.sharp: ['C', 'C'+self.sharp, 'D', 'D'+self.sharp, 'E', 'E'+self.sharp, 'F'+self.sharp, 'G', 'G'+self.sharp, 'A', 'A'+self.sharp, 'B'],
			'G'+self.flat: ['C', 'D'+self.flat, 'E'+self.flat+self.flat, 'E'+self.flat, 'F'+self.flat, 'F', 'G'+self.flat, 'G', 'A'+self.flat, 'B'+self.flat+self.flat, 'B'+self.flat, 'C'+self.flat],
			'G': ['C', 'C'+self.sharp, 'D', 'E'+self.flat, 'E', 'F', 'F'+self.sharp, 'G', 'G'+self.sharp, 'A', 'B'+self.flat, 'B'],
			'G'+self.sharp: ['B'+self.sharp, 'C'+self.sharp, 'D', 'D'+self.sharp, 'E', 'E'+self.sharp, 'F'+self.sharp+self.sharp, 'G'+self.sharp, 'A', 'A'+self.sharp, 'B'],
			'A'+self.flat: ['C', 'D'+self.flat, 'D', 'E'+self.flat, 'F'+self.flat, 'F', 'G'+self.flat, 'G', 'A'+self.flat, 'A', 'B'+self.flat, 'C'+self.flat],
			'A': ['C', 'C'+self.sharp, 'D', 'D'+self.sharp, 'E', 'F', 'F'+self.sharp, 'G', 'G'+self.sharp, 'A', 'A'+self.sharp, 'B'],
			'A'+self.sharp: ['B'+self.sharp, 'C'+self.sharp, 'C'+self.sharp+self.sharp, 'D'+self.sharp, 'E', 'E'+self.sharp, 'F'+self.sharp, 'F'+self.sharp+self.sharp, 'G'+self.sharp, 'G'+self.sharp+self.sharp, 'A'+self.sharp, 'B'],
			'B'+self.flat: ['C', 'D'+self.flat, 'D', 'E'+self.flat, 'E', 'F', 'G'+self.flat, 'G', 'A'+self.flat, 'A', 'B'+self.flat, 'B'],
			'B': ['C', 'C'+self.sharp, 'D', 'D'+self.sharp, 'E', 'F', 'F'+self.sharp, 'G', 'G'+self.sharp, 'A', 'A'+self.sharp, 'B']
			}
		try:
			return keys[key]
		except:
			raise Exception("Invalid key: %s" % key)
	
	def key_chords_doremi(self, key):
		from .common import chord_doremi_to_abc, chord_abc_to_doremi
		key = chord_doremi_to_abc(key)
		chords = self.key_chords_abc(key)
		return [chord_abc_to_doremi(ch) for ch in chords]

	def key_chords(self, key):
		from .common import is_abc, is_doremi
		if is_abc(key):
			return self.key_chords_abc(key)
		elif is_doremi(key):
			return self.key_chords_doremi(key)
		raise Exception("Invalid key: %s" % key)


transposer_config = TransposerConfig()