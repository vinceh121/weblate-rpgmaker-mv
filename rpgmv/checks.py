from weblate.checks.base import TargetCheck
from django.utils.html import format_html
from rpgmv import RpgLexer
from rpgmv import HtmlFormatter

def frequency_table(tokens, table):
	for t in tokens:
		if isinstance(t, RpgLexer.RPGTag):
			if t.tag in table:
				table[t.tag] += 1
			else:
				table[t.tag] = 1

class RpgTagsCheck(TargetCheck):
	check_id = "rpg-tags"
	name = "Consistency of RPGMaker MV tags"
	default_disabled = True
	always_display = True

	def check_single(self, source, target, unit):
		sourceTokens = RpgLexer.lex(source)
		targetTokens = RpgLexer.lex(target)

		sourceFreq = {}
		targetFreq = {}

		frequency_table(sourceTokens, sourceFreq)
		frequency_table(targetTokens, targetFreq)

		return sourceFreq != targetFreq

	def get_description(self, check_obj):
		formatter = HtmlFormatter.HtmlFormatter()
		formatter.actorNameSupplier = lambda v : f'"Actor {v}"'
		formatter.variableSupplier = lambda v : f'"Variable {v}"'
		formatter.partyMemberSupplier = lambda v : f'"Party member {v}"'
		formatter.iconSupplier = lambda v : '/favicon.ico'
		formatter.colors = HtmlFormatter.yttdColors

		formatter.reset()

		sourceHtml = None
		sourceError = None
		try:
			sourceHtml = formatter.doTheThing(RpgLexer.lex(check_obj.unit.source))
		except ValueError as e:
			sourceError = e

		formatter.reset()

		targetHtml = None
		targetError = None
		try:
			targetHtml = formatter.doTheThing(RpgLexer.lex(check_obj.unit.target))
		except ValueError as e:
			targetError = e

		return format_html(f"""<table class=\"table table-bordered table-striped\">
			<tbody>
			<tr {"class='danger'" if sourceError else ""}>
				<td>Source</td>
				<td>{sourceHtml or sourceError}</td>
			</tr>
			<tr {"class='danger'" if targetError else ""}>
				<td>Target</td>
				<td>{targetHtml or targetError}</td>
			</tr>
		</table>""")

