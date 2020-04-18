import spacy

class Interpreter:
  nlp = spacy.load('en_core_web_md')

  @staticmethod
  def run(q):
    doc = nlp(q)

    res = '=== POS Information ===\n\n'
    for token in doc:
        res = res + f'{token.text}, {token.lemma_}, {token.pos_}, {token.tag_}, {token.dep_},
            {token.shape_}, {token.is_alpha}, {token.is_stop}\n'
        
    res = res + '\n=== Named Entity Information ===\n\n'
    for ent in doc.ents:
        res = res + f'{ent.text}, {ent.start_char}, {ent.end_char}, {ent.label_}\n'
    
    return res
