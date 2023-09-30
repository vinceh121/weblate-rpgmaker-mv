
class RPGToken:
	def toFormattedText(self) -> str:
		return "INVALID"

	def toUnformattedText(self) -> str:
		return "INVALID"

	def __str__(self):
		return self.toUnformattedText()

class RPGTag(RPGToken):
	tag = ""
	argument = None

	def toFormattedText(self) -> str:
		return ""

	def toUnformattedText(self) -> str:
		return f"\\{self.tag}" + f"[{self.argument}]" if self.argument else ""

class RPGText(RPGToken):
	text = ""

	def __init__(self, text):
		self.text = text

	def toFormattedText(self) -> str:
		return self.text

	def toUnformattedText(self) -> str:
		return self.text

def lex(rawText) -> list[RPGToken]:
	i = 0
	tokens = []
	text = ""

	while i < len(rawText):
		c = rawText[i]
		if c == "\\":
			if len(text) != 0:
				tokens.append(RPGText(text))
				text = ''
			
			i += 1
			c = rawText[i]

			if c != "\\": # support double backslash escaping
				tag = RPGTag()
				tokens.append(tag)

				tag.tag = c

				if rawText[i + 1] == "[":
					tag.argument = ""

					i += 2
					while i < len(rawText) and rawText[i] != "]":
						tag.argument += rawText[i]
						i += 1
		else:
			text += c
		i += 1

	if text != "":
		tokens.append(RPGText(text))

	return tokens
