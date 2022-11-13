from os import getcwd

class Language():
	def __init__(self, encoding = "utf-8", support = 0):
		"Init Language"
		self._support = support
		self.langpath = getcwd() + "\\locale\\"
		self.support = ["en_us.lang", "zh_cn.lang"] # Wait For Settings Update
		self.encoding = encoding
		self.read_language()

	def read_language(self):
		"Read Language"
		# Format id:text
		self.textlist = {} # Prepare Dict For Languages
		with open(self.langpath + self.support[self._support], encoding = self.encoding) as lang:
			for line in lang.readlines():
				if line.startswith('#') or line == '\n':
					continue
				
				line = line.split(':')
				self.textlist[line[0]] = line[1]
				del line

	def lang(self, id):
		return self.textlist.get(id)

if __name__ == "__main__":
	en_us = Language()
	print(en_us.lang("version"))
