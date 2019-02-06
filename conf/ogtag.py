# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from docutils import nodes
from sphinx import addnodes
from urlparse import urljoin

class Visitor:

    def __init__(self, document):
        self.document = document
        self.text_list = []
        self.images = []
        self.n_sections = 0

    def dispatch_visit(self, node):
        # toctreeは飛ばす
        if isinstance(node, addnodes.compact_paragraph) and node.get('toctree'):
            raise nodes.SkipChildren

        # 画像を収集
        if isinstance(node, nodes.image):
            self.images.append(node)

        # 3つ目のセクションまではテキスト収集する
        if self.n_sections < 3:

            # テキストを収集
            if isinstance(node, nodes.paragraph):
                self.text_list.append(node.astext())

            # セクションに来たら深さを追加
            if isinstance(node, nodes.section):
                self.n_sections += 1

    def dispatch_departure(self, node):
        pass

    def get_og_description(self):
        # TODO: 何文字までが良いのか?
        text = ' '.join(self.text_list)
        if len(text) > 200:
            text = text[:197] + '...'
        return text

    def get_og_image_url(self, page_url):
        # TODO: 必ず最初の画像で良いのか
        if self.images:
            return urljoin(page_url, self.images[0]['uri'])
        else:
            return None


def get_og_tags(context, doctree, config):
    # page_url
    site_url = config['og_site_url']
    page_url = urljoin(site_url, context['pagename'] + context['file_suffix'])

    # collection
    visitor = Visitor(doctree)
    doctree.walkabout(visitor)

    # og:description
    og_desc = visitor.get_og_description()

    # og:image
    og_image = visitor.get_og_image_url(page_url)

    ## OGP
    tags = '''
    <meta property="og:description" content="{desc}">
    '''.format(ctx=context, desc=og_desc, page_url=page_url, cfg=config)
    if og_image:
        tags += '<meta property="og:image" content="{url}">'.format(url=og_image)
    return tags


def html_page_context(app, pagename, templatename, context, doctree):
    if not doctree:
        return

    context['metatags'] += get_og_tags(context, doctree, app.config)


def setup(app):
    app.add_config_value('og_site_url', None, 'html')
    app.add_config_value('og_twitter_site', None, 'html')
    app.connect('html-page-context', html_page_context)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }