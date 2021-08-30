import easyocr
reader = easyocr.Reader(['en','ch_tra']) # need to run only once to load model into memory
result = reader.readtext('3.png')
print('result', result)
