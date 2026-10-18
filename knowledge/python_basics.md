# Python Programming Basics

## Variables
Variables store values in Python.

Example:
```python
name = "Sandeep"
age = 20
```

## Data Types
Common Python data types include:
- int: integers, such as 10
- float: decimal numbers, such as 3.14
- str: text, such as "Hello"
- bool: True or False
- list: an ordered, changeable collection
- tuple: an ordered, unchangeable collection
- dict: a collection of key-value pairs
- set: a collection of unique values

## Conditional Statements
Conditional statements execute code depending on a condition.

Example:
```python
age = 18

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

## Loops
A for loop iterates over a sequence.

Example:
```python
for number in range(5):
    print(number)
```

A while loop repeats while a condition is true.

Example:
```python
count = 0

while count < 3:
    print(count)
    count += 1
```

## Functions
Functions are reusable blocks of code defined using `def`.

Example:
```python
def add(a, b):
    return a + b

print(add(2, 3))
```

## Lists
Lists store multiple items in a single variable.

Example:
```python
fruits = ["apple", "banana", "orange"]
print(fruits[0])
fruits.append("mango")
```

## Dictionaries
Dictionaries store key-value pairs.

Example:
```python
student = {"name": "Sam", "age": 21}
print(student["name"])
```

## Exception Handling
Use try and except to handle errors.

Example:
```python
try:
    number = int("abc")
except ValueError:
    print("Invalid number")
```

## Object-Oriented Programming
Classes define the structure of objects. Objects are instances of classes.

Example:
```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print("Woof!")

dog = Dog("Buddy")
dog.bark()
```

## File Handling
Use `open()` to read or write files.

Example:
```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("Hello, Python!")
```
