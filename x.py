"""
The variable m inside the function func() is local and does not affect the global variable m.
Use the global keyword to modify the global variable m inside the function.
"""
m = 5
def func():
  global m
  m = 17
  return 3

m = m + func()
print(f"Sum1: {m}")

m = func() + m
print(f"Sum2: {m}")