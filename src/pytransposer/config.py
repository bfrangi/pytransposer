import re
class TransposerConfig():
	sharp = '#'
	flat = 'b'
	abc = 'abc'
	doremi = 'doremi'

	def get_chord_regex(self):
		return re.compile(r"((?:" + self.get_key_regex_str_doremi() + r")|(?:" + self.get_key_regex_str_abc() + r"))")
	
	def get_chord_group_regex(self, pre_chord, post_chord):
		return re.compile(r'(' + pre_chord + r')((?:(?!' + post_chord + r').)*)(' + post_chord + r')')


	def sharp_flat(self):
		return [self.sharp, self.flat]
	
	def get_key_list_abc(self):
		return [
			('A',), 
			('A'+self.sharp, 'B'+self.flat), 
			('B',), 
			('C',), 
			('C'+self.sharp, 'D'+self.flat), 
			('D',),
			('D'+self.sharp, 'E'+self.flat), 
			('E',), ('F',), 
			('F'+self.sharp, 'G'+self.flat), 
			('G',), 
			('G'+self.sharp, 'A'+self.flat)
			]
	
	def get_sharp_flat_preferences_abc(self):
		return {
		'A' : self.sharp,
		'A'+self.sharp: self.flat,
		'B'+self.flat: self.flat,
		'B' : self.sharp,
		'C' : self.flat,
		'C'+self.sharp: self.flat,
		'D'+self.flat: self.flat,
		'D' : self.sharp,
		'D'+self.sharp: self.flat,
		'E'+self.flat: self.flat,
		'E' : self.sharp,
		'F' : self.flat,
		'F'+self.sharp: self.sharp,
		'G'+self.flat: self.sharp,
		'G' : self.sharp,
		'G'+self.sharp: self.flat,
		'A'+self.flat: self.flat,
		}
	
	def get_key_regex_str_abc(self):
		return r"[ABCDEFG][" + self.sharp + self.flat + r"]?"
	
	def get_key_regex_abc(self):
		return re.compile(self.get_key_regex_str_abc())
	
	def get_key_list_doremi(self):
		return [
			('LA',), 
			('LA'+self.sharp, 'SI'+self.flat), 
			('SI',), 
			('DO',), 
			('DO'+self.sharp, 'RE'+self.flat), 
			('RE',),
			('RE'+self.sharp, 'MI'+self.flat), 
			('MI',), 
			('FA',), 
			('FA'+self.sharp, 'SOL'+self.flat), 
			('SOL',), 
			('SOL'+self.sharp, 'LA'+self.flat)
			]
	
	def get_sharp_flat_preferences_doremi(self):
		return {
			'LA' : self.sharp,
			'LA'+self.sharp: self.flat,
			'SI'+self.flat: self.flat,
			'SI' : self.sharp,
			'DO' : self.flat,
			'DO'+self.sharp: self.flat,
			'RE'+self.flat: self.flat,
			'RE' : self.sharp,
			'RE'+self.sharp: self.flat,
			'MI'+self.flat: self.flat,
			'MI' : self.sharp,
			'FA' : self.flat,
			'FA'+self.sharp: self.sharp,
			'SOL'+self.flat: self.sharp,
			'SOL' : self.sharp,
			'SOL'+self.sharp: self.flat,
			'LA'+self.flat: self.flat,
			}
	
	def get_key_regex_str_doremi(self):
		return r"(?:DO|RE|MI|FA|SOL|LA|SI|DO)[" + self.sharp + self.flat + r"]?"
	
	def get_key_regex_doremi(self):
		return re.compile(self.get_key_regex_str_doremi())


transposer_config = TransposerConfig()