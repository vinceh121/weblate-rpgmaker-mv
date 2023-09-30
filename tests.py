import unittest
import RpgLexer
import HtmlFormatter

class LexerTest(unittest.TestCase):
	def test_formats(self):
		string = "\\.\"Trouver le \\C[2]corps\\C[0]...!\n C'est vrai, il y avait la note.\""
		tokens = RpgLexer.lex(string)

		unformatted = ['', '"Trouver le ', '\\C[2]', 'corps', '\\C[0]', '...!\n C\'est vrai, il y avait la note."']
		formatted = ['', '"Trouver le ', '', 'corps', '', '...!\n C\'est vrai, il y avait la note."']

		self.assertEqual(list(map(lambda t : t.toUnformattedText(), tokens)), unformatted)
		self.assertEqual(list(map(lambda t : t.toFormattedText(), tokens)), formatted)

class FormatterTest(unittest.TestCase):
	def test_formatter(self):
		string = "\\.\"Trouver le \\C[2]corps\\C[0]...!\n C'est vrai, il y avait la note.\""
		tokens = RpgLexer.lex(string)

		formatter = HtmlFormatter.HtmlFormatter()
		formatter.colors = HtmlFormatter.yttdColors
		print(formatter.doTheThing(tokens))

if __name__ == '__main__':
	unittest.main()
