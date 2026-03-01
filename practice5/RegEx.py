import re

txt = ["a", "ab", "abb", "b", "ba"]

#1)
for txt in txt:
    x = re.findall("ab*", txt)
    if x:
        print(x)

#2)
for txt in txt:
    x = re.findall("ab{2,3}", txt)
    if x:
        print(x)


txt2="Hello planet"
#3)
x = re.findall("[a-z]+_[a-z]+", txt2)
print(x)

#4)
x = re.findall("[A-Z][a-z]+", txt2)
print(x)

#5)
for txt in txt:
    x = re.findall("a.*b", txt)
    if x:
        print(x)

#6)
x = re.sub("[ ,\.]", ":", txt2)
print(x)

#7)
txt3 = "this_is_snake_case"


components = txt3.split('_')
x = components[0] + ''.join(c.title() for c in components[1:])
print(x)

#8)
txt4 = "HelloWorldPythonCode"


x = re.split("(?=[A-Z])", txt)
print(x)

#9) 
x = re.sub("([A-Z])", r" \1", txt).strip()
print(x)

#10)
x = re.sub("([A-Z])", r"_\1", txt4).lower()
if x.startswith("_"):
    x = x[1:]
print(x)