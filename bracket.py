sentence = "()()"
sentence_list = list(sentence)
latest = 0
stack = []

if len(sentence_list) & 1:
    print("false")
    exit()

closing = (')', ']', '}')
opening = ('(', '[', '{')

if sentence_list[0] in closing:
    print("false")
    exit()
    
if sentence_list[-1] in opening:
    print("false")
    exit()
    
for i in range(len(sentence_list)):
    print(stack)
    print(i)
    
    if stack:
        latest = stack[-1]
        
    stack.append(sentence_list[i])
    
    if latest == '(' and stack[-1] == ')':
        try:
            stack.pop()
            stack.pop()
        except:
            print("false")
            exit()
    if latest == '{' and stack[-1] == '}':
        try:
            stack.pop()
            stack.pop()
        except:
            print("false")
            exit()
    if latest == '[' and stack[-1] == ']':
        try:
            stack.pop()
            stack.pop()
        except:
            print("false")
            exit()
   
if len(stack) == 0:
    print("true")
else:
    print("false")
