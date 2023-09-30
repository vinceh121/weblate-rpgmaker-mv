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

	def doTheThing(self, tokens) -> str:
		output = ""
		isSpanOpen = False

		for t in tokens:
			if isinstance(t, RpgLexer.RPGText):
				output += html.escape(t.toFormattedText()).replace("\n", "<br>")
			elif isinstance(t, RpgLexer.RPGToken):
				if isSpanOpen:
					output += "</span>"

				if t.tag == "C":
					output += f'<span color="{self.colors[int(t.argument)]}">'
					isSpanOpen = True
				elif t.tag == "V":
					output += self.variables[int(t.argument)]
				elif t.tag == "N":
					output += self.actorNames[int(t.argument)]
				elif t.tag == "O":
					output += self.partyMemberNames[int(t.argument)]
				elif t.tag == "I":
					output += f'<img alt="{t.argument}" src="{self.icons[int(t.argument)]}">'
				elif t.tag == "G":
					output += self.currency

		if isSpanOpen:
			output += "</span>"
		return output
