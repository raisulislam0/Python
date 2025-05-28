sentence = "(){}{}[]"
sentence_list = list(sentence)
latest = 0
stack = []

if len(sentence_list) & 1:
    print("Invalid")
    stack.append(1)
else:
    for i in range(len(sentence_list)):
        print(stack)
        if stack:
            latest = stack[-1]
        stack.append(sentence_list[i])
        
        if latest == '(' and stack[-1] == ')':
            stack.pop()
            stack.pop()
        if latest == '{' and stack[-1] == '}':
            stack.pop()
            stack.pop()
        if latest == '[' and stack[-1] == ']':
            stack.pop()
            stack.pop()
        
if len(stack) == 0:
    print("Valid")
else:
    print("Invalid")
