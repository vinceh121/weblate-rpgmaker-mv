import html
import RpgLexer

yttdColors = {
	0: "#ffffff",
	1: "#20a0d6",
	2: "#ff784c",
	3: "#66cc40",
	4: "#99ccff",
	5: "#ccc0ff",
	6: "#ffffa0",
	7: "#808080",
	8: "#c0c0c0",
	9: "#2080cc",
	10: "#ff3810",
	11: "#00a010",
	12: "#3e9ade",
	13: "#a098ff",
	14: "#ffcc20",
	15: "#000000",
	16: "#84aaff",
	17: "#ffff40",
	18: "#ff2020",
	19: "#202040",
	20: "#e08040",
	21: "#f0c040",
	22: "#4080c0",
	23: "#40c0f0",
	24: "#80ff80",
	25: "#c08080",
	26: "#8080ff",
	27: "#ff80ff",
	28: "#00a040",
	29: "#00e060",
	30: "#a060e0",
	31: "#c080ff"
}

class HtmlFormatter:
	colors = {}
	variables = {}
	actorNames = {}
	partyMemberNames = {}
	icons = {}
	currency = "Yen"
	defaultFontSize = 12
	fontUnit = "pt"

	colorSupplier = lambda self, v : self.colors[v]
	variableSupplier = lambda self, v : self.variables[v]
	actorNameSupplier = lambda self, v : self.actorNames[v]
	partyMemberSupplier = lambda self, v : self.partyMemberNames[v]
	iconSupplier = lambda self, v : self.icons[v]

	output = ""
	isSpanOpen = False
	currentStyle = {}

	def serializeCss(self, params) -> str:
		css = ""

		for key in params:
			css += key
			css += ": "
			css += str(params[key])
			if key == "font-size":
				css += self.fontUnit
			css += "; "

		return css.strip()

	def applyStyle(self): # needs to be called at each text write
		if len(self.currentStyle) != 0:
			self.isSpanOpen = True
			self.output += f'<span style="{self.serializeCss(self.currentStyle)}">'

	def doTheThing(self, tokens) -> str:
		for t in tokens:
			if isinstance(t, RpgLexer.RPGText):
				self.applyStyle()
				self.output += html.escape(t.toFormattedText()).replace("\n", "<br>")
			elif isinstance(t, RpgLexer.RPGToken):
				if self.isSpanOpen:
					self.output += "</span>"
					self.isSpanOpen = False

				if t.tag == "C":
					self.currentStyle["color"] = self.colorSupplier(int(t.argument))
				elif t.tag == "V":
					self.applyStyle()
					self.output += self.variableSupplier(int(t.argument))
				elif t.tag == "N":
					self.applyStyle()
					self.output += self.actorNameSupplier(int(t.argument))
				elif t.tag == "O":
					self.applyStyle()
					self.output += self.partyMemberSupplier(int(t.argument))
				elif t.tag == "I":
					self.applyStyle()
					self.output += f'<img alt="{t.argument}" src="{self.iconSupplier(int(t.argument))}">'
				elif t.tag == "G":
					self.applyStyle()
					self.output += self.currency
				elif t.tag == "{":
					if not "font-size" in self.currentStyle:
						self.currentStyle["font-size"] = self.defaultFontSize
					self.currentStyle["font-size"] += 1
				elif t.tag == "}":
					if not "font-size" in self.currentStyle:
						self.currentStyle["font-size"] = self.defaultFontSize
					self.currentStyle["font-size"] -= 1

		if self.isSpanOpen:
			self.output += "</span>"
		return self.output
