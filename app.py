import os
from base64 import b64encode
from collections import OrderedDict
from typing import List
from urllib.parse import quote

from flask import Flask, render_template, request, Response
import yaml

from intent2.alignment import heuristic_alignment, AlignException, gloss_to_morph_align, UnequalTokensException, \
    LangMorphAlignException
from intent2.classification import LRWrapper
from intent2.model import Instance, Phrase, DependencyException
from intent2.processing import load_spacy, process_trans
from intent2.projection import project_pos, project_ds

app = Flask(__name__)
application=app # for mod_wsgi

# Preload the models required
load_spacy()
classifier = LRWrapper.load('pos') # type: LRWrapper

@app.route('/')
def index():
    my_dir = os.path.dirname(__file__)
    with open(os.path.join(my_dir, 'examples.yml')) as f:
        sorted_dict = OrderedDict()
        examples = yaml.load(f)
        for lang in sorted(examples.keys()):
            sorted_dict[lang] = examples[lang].strip()

    return render_template('home.html', examples=sorted_dict)

def process_instance(text: List[str]) -> Instance:
    inst = Instance.from_strings(text)
    inst.has_lang_gloss_aln()
    gloss_to_morph_align(inst)
    process_trans(inst)
    heuristic_alignment(inst)
    project_pos(inst)
    try:
        project_ds(inst)
    except DependencyException:
        pass
    predictions = classifier.classify(inst.gloss, projected_tags=True, subword_tags=True, use_vocab=True)

    return inst, predictions

def render_ds(phrase: Phrase):
    if phrase.dependency_structure:
        trans_png = phrase.dependency_structure.draw()
        trans_data = b64encode(trans_png).decode('ascii')
        return 'data:image/png;base64,{}'.format(quote(trans_data))

@app.route('/process', methods=['POST'])
def process_igt():
    inst_text = request.form.get('text').split('\n')
    if len(inst_text) != 3:
        return Response(status='400', response=render_template('error_msg.html',
                                                               error_txt='Please supply three lines, a language, gloss, and translation line, separated by newlines.'))
    try:
        inst, class_tags = process_instance(inst_text) # type: Instance, List
        col_widths = [max(len(lw.subwords), len(gw.subwords)) for lw, gw in zip(inst.lang, inst.gloss)]

    except UnequalTokensException as ute:
        error_txt = 'Please ensure that the language and gloss lines have the same number of whitespace-separated tokens.'
        return Response(status='400', response=render_template('error_msg.html', error_txt=error_txt))
    except LangMorphAlignException as lmae:
        error_txt = 'Please ensure that the language and gloss lines, when morphemes are present (hyphens) have the same number between language and gloss.'
        return Response(status='400', response=render_template('error_msg.html', error_txt=error_txt))
    else:
        return render_template('instance.html',
                               inst=inst,
                               class_tags=zip(inst.gloss,class_tags),
                               tds = render_ds(inst.trans),
                               lds = render_ds(inst.lang),
                               col_widths=col_widths
                               )


if __name__ == '__main__':
    app.run()
