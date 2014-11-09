# -*- coding: utf-8 -*-
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.body import ParsedLiteral
from docutils import nodes

from sphinx import environment as env
from sphinx.writers import html
from sphinx.highlighting import lexers

from pygments.lexers.web import PhpLexer

from ConfigParser import SafeConfigParser

# Add "parsed-code" directive that combines both the features
# of "parsed-literal" (support for inline markup) and "sourcecode"
# (syntax highlighting).
class ParsedCodeBlock(ParsedLiteral):
    """
    Directive for a code block with special highlighting or line numbering
    settings that parses its content first (like "parsed-literal").
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'linenos': directives.flag,
        'class': directives.class_option,
    }
    def run(self):
        res = ParsedLiteral.run(self)
        res[0]['language'] = self.arguments[0]
        res[0]['linenos'] = 'linenos' in self.options
        res[0]['highlight'] = True
        return res

def setup(app):
    # Monkey-patch html.HTMLTranslator.visit_literal_block so that
    # a node with the "highlight" attribute is always highlighted.
    old_visit = html.HTMLTranslator.visit_literal_block
    def new_visit(self, node):
        if node.get('highlight'):
            node.rawsource = node.astext()
        return old_visit(self, node)
    html.HTMLTranslator.visit_literal_block = new_visit

    directives.register_directive('parsed-code', ParsedCodeBlock)

    # Add "project" to the default substitutions.
    env.default_substitutions = set(['version', 'release', 'today', 'project'])

    # Additionnal lexer for inline PHP code blocks.
    lexers['inline-php'] = PhpLexer(startinline=True)

    # import parameters
    conf = SafeConfigParser()
    #conf.read('conf.ini')
    import os
    try:
        conf.read(os.path.join(os.getcwd(), 'conf.ini'))
        for key, value in conf.items('sphinx'):
            exec("%s = %r" % (key, value)) in globals()
    except:
        print 'Not found conf.ini'

    # global includes
    rst_prolog = u'''
.. include:: _definition.rst_
    '''

    # custom styles
    app.add_stylesheet('custom.css')

