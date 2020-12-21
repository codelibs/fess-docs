# -*- coding: utf-8 -*-
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.body import ParsedLiteral
from docutils import nodes

from sphinx import environment as env
from sphinx.writers import html
from sphinx.highlighting import lexers

from pygments.lexers.web import PhpLexer

from ConfigParser import SafeConfigParser

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
    replace = []
    rst_prolog = ""
    import os
    try:
        # read from build directory
        #conf.read(os.path.join(os.getcwd(), 'conf.ini'))
        # read from conf directory
        conf.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini'))
        for key, value in conf.items('sphinx'):
            app.config._raw_config[key] = value
        # replace =  conf.items('replace')
        for key, value in conf.items('replace'):
            rst_prolog += "\n.. |" + key + "| replace:: " + value
    except:
        print 'Not found conf.ini'

    # includes from each directory
    rst_prolog += u'''
.. include:: _defs.rst_
    '''

    app.config._raw_config["rst_prolog"] = rst_prolog

    # custom styles
    app.add_stylesheet('css/custom.css')


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

