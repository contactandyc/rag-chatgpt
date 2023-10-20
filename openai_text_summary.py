import os, sys
import openai

from lib.OpenAIRequester import OpenAIRequester
from lib.ChainOfDensity import ChainOfDensity
from lib.ChooseBestSummary import ChooseBestSummary
from lib.CreateFacts import CreateFacts
from lib.GrammarFix import GrammarFix

from lib.segment_text import segment_text

openai.api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-3.5-turbo-0301"

datadir = sys.argv[1]
if datadir[-1] == '/':
    datadir = datadir[0:-1]


# Load input file
with open(datadir + '/input.txt', "r") as f:
    input_text = f.read()

datadir = datadir + '/summary'
os.makedirs(datadir, exist_ok=True)

segments = segment_text(input_text, max_length=2000, lines_back=3)

OpenAIRequester.separator = "\n\n=====\n\n"

text_file = open(datadir + '/text.txt', 'w')
grammar_fix = GrammarFix(model, open(datadir + '/grammar.txt', 'w'))
create_facts = CreateFacts(model, open(datadir + '/facts.txt', 'w'))
chain_of_density = ChainOfDensity(model, open(datadir + '/chain_of_density.txt', 'w'))
choose_best_summary = ChooseBestSummary(model, open(datadir + '/choose_best_summary.txt', 'w'))

for input_text in segments:
    text_file.write(input_text)
    text_file.write(OpenAIRequester.separator)
    text_file.flush()

    new_text = grammar_fix.run(input_text)
    if new_text is not None:
        input_text = new_text

    create_facts.run(input_text)
    chain_of_density.run(input_text)
    choose_best_summary.run(input_text)

text_file.close()
grammar_fix.close()
create_facts.close()
chain_of_density.close()
choose_best_summary.close()
