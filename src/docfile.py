import docx

doc = docx.Document('sample.docx')
paras = [p.text for p in doc.paragraphs if p.text]

print(f'=== Output type is a {type(paras)} of {type(paras[1])} \n total length is {len(paras)} ===')
