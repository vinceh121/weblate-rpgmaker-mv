from weblate.checks.base import TargetCheckParametrized
from django.utils.html import format_html
from rpgmv import RpgLexer
from rpgmv import HtmlFormatter

class RpgTagsCheck(TargetCheckParametrized):
	check_id = "rpg-tags"
	name = "Checks consistency of RPGMaker MV tags, and renders the string"
	default_disabled = True
	always_display = True

	def get_description(self, check_obj):
		formatter = HtmlFormatter.HtmlFormatter()
		formatter.actorNameSupplier = lambda v : f'"Actor {v}"'
		formatter.variableSupplier = lambda v : f'"Variable {v}"'
		formatter.partyMemberSupplier = lambda v : f'"Party member {v}"'
		formatter.iconSupplier = lambda v : '/favicon.ico'
		formatter.colors = HtmlFormatter.yttdColors

		tokens = RpgLexer.lex(check_obj.unit.target)
		return format_html(formatter.doTheThing(tokens))
