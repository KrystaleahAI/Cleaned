import spacy
from spacy.tokens import Token
from spacy.language import Language
import csv

# Register custom extension attribute 'is_slur' on the Token class
Token.set_extension('is_slur', default=False, force=True)

# Function to load slurs from a CSV file
def load_slurs(filename):
    slur_list = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if len(row) >= 3:
                slur_list.append({'slur': row[0], 'group': row[1], 'origin': row[2]})
    return slur_list

# Create a spaCy pipeline with a custom component
def create_pipeline(slur_csv):
    nlp = spacy.blank("en")
    slur_list = load_slurs(slur_csv)

    # Custom component function
    @Language.component("replace_slurs")
    def replace_slurs(doc):
        for token in doc:
            for slur_entry in slur_list:
                if token.text.lower() == slur_entry['slur'].lower():
                    token._.is_slur = True
                    break
        return doc

    # Add the custom component to the pipeline
    nlp.add_pipe("replace_slurs", last=True)
    return nlp