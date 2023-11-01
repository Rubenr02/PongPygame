import random
power_names = "freeze", "shrink", "enlarge", "bounce", "invisible"

# making a random choice of the existing powers
power_ups = random.choices(power_names, weights=(30, 40, 40, 20, 40), k=1)
print(power_ups)