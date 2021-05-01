import math

def quadratic_formula(a, b, c):
    disc = b**2 - 4 * a * c
    x1 = (-b - math.sqrt(disc)) / (2 * a)
    x2 = (-b + math.sqrt(disc)) / (2 * a)

    if x1 <= 38:
        return x1
    else:
        return x2

watts = 100

result = quadratic_formula(-0.158, 11.98, (21.8 - watts))
print(result)
