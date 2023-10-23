from langdetect import detect

text = input("enter your text here: ")

tone = detect(text)

print("your text is in", tone)
