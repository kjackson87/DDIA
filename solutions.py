from collections import deque
def evaluation(exp: deque):
    # First pass mult
    int_stack = deque()
    while exp:
        token = exp.popleft()
        if token == '*':
            int_stack.append(int_stack.pop() * exp.popleft())
        elif token == '-':
            int_stack.append(-exp.popleft())
        elif type(token) == int:
            int_stack.append(token)
    
    return sum(int_stack)


test_cases = [
    # Basic operations
    (deque([2, '+', 3]), 5),
    (deque([2, '-', 3]), -1),
    (deque([2, '*', 3]), 6),
    
    # Multiple operations
    (deque([2, '+', 3, '+', 4]), 9),
    (deque([2, '*', 3, '+', 4]), 10),
    (deque([2, '+', 3, '*', 4]), 14),
    (deque([2, '*', 3, '*', 4]), 24),
    
    # Negative numbers
    (deque([2, '-', 3, '*', 4]), -10),
    (deque([2, '*', 3, '-', 4]), 2),
    
    # Larger numbers
    (deque([12, '*', 3]), 36),
    (deque([12, '+', 3, '*', 4]), 24),
    
    # More complex combinations
    (deque([2, '*', 3, '+', 4, '*', 5]), 26),
    (deque([2, '*', 3, '-', 4, '*', 5]), -14),
    (deque([10, '*', 3, '-', 20, '*', 2]), -10),
]

def run_tests(eval_func):
    for i, (exp, expected) in enumerate(test_cases):
        # Create a copy of deque since it will be modified
        result = eval_func(deque(exp))
        print(f"Test {i+1}: {'PASS' if result == expected else 'FAIL'}")
        print(f"Expression: {list(exp)}")
        print(f"Expected: {expected}, Got: {result}\n")

valid = []

def recOp(left, right):
    if not right:
        if evaluate(deque(left)) == target:
            valid.append(''.join(map(str,left)))
            return
    else:
        d = right[0]

        # +f
        recOp(left + ['+'] + [d], right[1:])
        # -
        recOp(left + ['-'] + [d], right[1:])
        # *
        recOp(left + ['*'] + [d], right[1:])
        # noop
        new_left = left[-1] * 10 + d
        recOp(left[:-1] + [new_left], right[1:])