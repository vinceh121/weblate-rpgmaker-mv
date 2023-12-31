import unittest
import RpgLexer
from formatters import HtmlFormatter, TextFormatter, yttdColors

class LexerTest(unittest.TestCase):
	def test_formats(self):
		string = "\\.\"Trouver le \\C[2]corps\\C[0]...!\n C'est vrai, il y avait la note.\""
		tokens = RpgLexer.lex(string)

		unformatted = ['', '"Trouver le ', '\\C[2]', 'corps', '\\C[0]', '...!\n C\'est vrai, il y avait la note."']
		formatted = ['', '"Trouver le ', '', 'corps', '', '...!\n C\'est vrai, il y avait la note."']

		self.assertEqual(list(map(lambda t : t.toUnformattedText(), tokens)), unformatted)
		self.assertEqual(list(map(lambda t : t.toFormattedText(), tokens)), formatted)

	def test_formats_two(self):
		string = "\\.\\sp[8]\\C[3]Mais qui est cette personne...?"
		tokens = RpgLexer.lex(string)

		unformatted = ['', '\\sp[8]', '\\C[3]', 'Mais qui est cette personne...?']
		formatted = ['', '', '', 'Mais qui est cette personne...?']

		self.assertEqual(list(map(lambda t : t.toUnformattedText(), tokens)), unformatted)
		self.assertEqual(list(map(lambda t : t.toFormattedText(), tokens)), formatted)

class FormatterTest(unittest.TestCase):
	def test_html_formatter(self):
		string = "\\.\"Trouver le \\C[2]\\{\\V[3]\\}\\C[0]...!\n C'est vrai, il y avait la note.\""
		tokens = RpgLexer.lex(string)

		formatter = HtmlFormatter()
		formatter.variableSupplier = lambda v : f"Variable {v}"
		formatter.colors = yttdColors
		self.assertEqual(formatter.doTheThing(tokens), '&quot;Trouver le <span style="color: #ff784c; font-size: 15pt;">Variable 3</span><span style="color: #ffffff; font-size: 14pt;">...!<br> C&#x27;est vrai, il y avait la note.&quot;</span>')

	def test_text_formatter(self):
		string = "\\.\"Trouver le \\C[2]\\{\\V[3]\\}\\C[0]...!\n C'est vrai, il y avait la note.\""
		tokens = RpgLexer.lex(string)

		formatter = TextFormatter()
		formatter.variableSupplier = lambda v : f"Variable {v}"
		self.assertEqual(formatter.doTheThing(tokens), "\"Trouver le Variable 3...!\n C'est vrai, il y avait la note.\"")

if __name__ == '__main__':
	unittest.main()
