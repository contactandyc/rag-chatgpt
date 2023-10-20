from lib.OpenAIRequester import OpenAIRequester

class CreateFacts(OpenAIRequester):
    def __init__(self, model, output_file):
        super().__init__('CreateFacts', model, output_file)

    def get_system_message(self):
        return {
           "role": "system",
           "content": f"""I will provide you with piece of content (e.g. articles, papers, documentation, etc.)

           You will generate 5 or more unique facts from the context.  Ideally you would generate 10 unique facts.

           Guidelines:

           All facts should be different in some meaningful way.
           All facts should be able to stand on their own without the context of the paragraph.
           Pronouns and references to things should be resolved.
           If a fact only makes sense within the context of the paragraph, it should be thrown out.
           A fact may be up to two sentences and ~50 words.

           Answer in JSON. The JSON should be a list of dictionaries whose key is "Fact"."""
       }

    def get_user_message(self, input_text, warn=False):
        warning = ""
        if warn is True:
            warning = "In the last response, you have missed that the response should be a JSON array.  Please make sure that the response is a JSON object with an array of objects each containing a 'Fact' key as described in the system prompt.  "

        return {
                "role": "user",
                "content": f"{warning}Here is the input text for you to summarise using the 'Fact' approach:\n\n{input_text}",
            }

    def parse(self, input_text):
        return self.parse_into_array(input_text, 'Fact')

    def format_output(self, parsed):
        res = ''
        for f in parsed:
            res = res + f + '\n\n'

        return res
