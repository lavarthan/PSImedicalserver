# """Example of training spaCy's named entity recognizer, starting off with an
# existing model or a blank model.
#
# For more details, see the documentation:
# * Training: https://spacy.io/usage/training
# * NER: https://spacy.io/usage/linguistic-features#named-entities
#
# Compatible with: spaCy v2.0.0+
# Last tested with: v2.1.0
# """
# from __future__ import unicode_literals, print_function
#
# import plac
# import random
# from pathlib import Path
# import spacy
# from spacy.util import minibatch, compounding
#
# # training data
# TRAIN_DATA = [
#     ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
#     ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
#     ("What is the temperature in Kilinochi?", {"entities": [(27, 36, "GPE")]}),
#     ("What is the temperature in Mullaitivu?", {"entities": [(27, 37, "GPE")]}),
#     ("What is the temperature in Vavuniya?", {"entities": [(27, 35, "GPE")]}),
#     ("What is the temperature in Mannar?", {"entities": [(27, 33, "GPE")]}),
#     ("I want to know the location of jaffna teaching hospital", {"entities": [(31, 37, "GPE")]}),
#     ("What is the temperature in Puttalam?", {"entities": [(27, 35, "GPE")]}),
#     ("What is the temperature in pollanaruwa?", {"entities": [(27, 38, "GPE")]}),
#     ("What is the temperature in Kurunegala?", {"entities": [(27, 37, "GPE")]}),
#     ("What is the temperature in Colombo?", {"entities": [(27, 34, "GPE")]}),
#     ("What is the temperature in Gampaha?", {"entities": [(27, 34, "GPE")]}),
#     ("What is the temperature in kalutara?", {"entities": [(27, 35, "GPE")]}),
#     ("What is the temperature in Anuradhapura?", {"entities": [(27, 39, "GPE")]}),
#     ("What is the temperature in Matale?", {"entities": [(27, 33, "GPE")]}),
#     ("What is the temperature in Kandy?", {"entities": [(27, 32, "GPE")]}),
#     ("What is the temperature in Nuwara Eliya?", {"entities": [(27, 39, "GPE")]}),
#     ("What is the temperature in Kegalle?", {"entities": [(27, 34, "GPE")]}),
#     ("What is the temperature in Ratnapura?", {"entities": [(27, 36, "GPE")]}),
#     ("What is the temperature in Trincomalee?", {"entities": [(27, 38, "GPE")]}),
#     ("What is the temperature in Batticaloa?", {"entities": [(27, 37, "GPE")]}),
#     ("What is the temperature in Ampara?", {"entities": [(27, 33, "GPE")]}),
#     ("What is the temperature in badulla?", {"entities": [(27, 34, "GPE")]}),
#     ("What is the temperature in Monaragala?", {"entities": [(27, 38, "GPE")]}),
#     ("What is the temperature in Hambantota?", {"entities": [(27, 37, "GPE")]}),
#     ("What is the temperature in Matara?", {"entities": [(27, 33, "GPE")]}),
#     ("What is the temperature in Galle?", {"entities": [(27, 32, "GPE")]}),
#     ("I want some details about doctor Mohan?", {"entities": [(33, 38, "PERSON")]}),
#     ("is Dr.Mohan available?", {"entities": [(6, 11, "PERSON")]}),
# ]
#
#
# @plac.annotations(
#     model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
#     output_dir=("Optional output directory", "option", "o", Path),
#     n_iter=("Number of training iterations", "option", "n", int),
# )
# def main(model='en', output_dir="custom", n_iter=100):
#     """Load the model, set up the pipeline and train the entity recognizer."""
#     if model is not None:
#         nlp = spacy.load(model)  # load existing spaCy model
#         print("Loaded model '%s'" % model)
#     else:
#         nlp = spacy.blank("en")  # create blank Language class
#         print("Created blank 'en' model")
#
#     # create the built-in pipeline components and add them to the pipeline
#     # nlp.create_pipe works for built-ins that are registered with spaCy
#     if "ner" not in nlp.pipe_names:
#         ner = nlp.create_pipe("ner")
#         nlp.add_pipe(ner, last=True)
#     # otherwise, get it so we can add labels
#     else:
#         ner = nlp.get_pipe("ner")
#
#     # add labels
#     for _, annotations in TRAIN_DATA:
#         for ent in annotations.get("entities"):
#             ner.add_label(ent[2])
#
#     # get names of other pipes to disable them during training
#     pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
#     other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
#     with nlp.disable_pipes(*other_pipes):  # only train NER
#         # reset and initialize the weights randomly – but only if we're
#         # training a new model
#         if model is None:
#             nlp.begin_training()
#         for itn in range(n_iter):
#             random.shuffle(TRAIN_DATA)
#             losses = {}
#             # batch up the examples using spaCy's minibatch
#             batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
#             for batch in batches:
#                 texts, annotations = zip(*batch)
#                 nlp.update(
#                     texts,  # batch of texts
#                     annotations,  # batch of annotations
#                     drop=0.5,  # dropout - make it harder to memorise data
#                     losses=losses,
#                 )
#             print("Losses", losses)
#
#     # test the trained model
#     i=1
#     for text, _ in TRAIN_DATA:
#         print(i, "\n")
#         i += 1
#         doc = nlp(text)
#         print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
#         print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
#
#     # save model to output directory
#     if output_dir is not None:
#         output_dir = Path(output_dir)
#         if not output_dir.exists():
#             output_dir.mkdir()
#         nlp.to_disk(output_dir)
#         print("Saved model to", output_dir)
#
#         # test the saved model
#         print("Loading from", output_dir)
#         nlp2 = spacy.load(output_dir)
#         for text, _ in TRAIN_DATA:
#             doc = nlp2(text)
#             print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
#             print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
#
#
# if __name__ == "__main__":
#     plac.call(main)
#
#     # Expected output:
#     # Entities [('Shaka Khan', 'PERSON')]
#     # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
#     # ('Khan', 'PERSON', 1), ('?', '', 2)]
#     # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
#     # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
#     # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)
