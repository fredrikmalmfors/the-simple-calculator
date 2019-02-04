# the-simple-calculator
A simple calculator with registers and lazy evaluation written in Python.


## Run

```
python3 calculator.py [file]
```

Enter a file path to read input from file. Skip the [file] argument to read from the console.

## Syntax

* Register: Any alphanumerical input with at least one alpha character.
* Operation: ADD, SUBTRACT, or MULTIPLY
* Value: Either an integer or a register

All input is case insensitive.

### Operation
Performs a given operation with given value on given register.
```
<register> <operation> <value>
```

### Print
Evaluates and prints the value of the register
```
print <register>
```

### Quit
Executes all written lines and exits the program.
```
quit
```

## What you can do

Input
```
cost add food
cost add drinks
discount add 5
food add 12
drinks add 18
cost multiply 5
print cost
cost subtract discount
print cost
quit
```
Output
```
150
145
```

---

The calculator can handle circular dependencies.

Input
```
A add B
B add C
C add A
A add 3
print A
print B
print C
quit
```
Output
```
3
3
3
```

