## Assignment 1: Design Your Own Class! 🏗️

1. Create a class representing anything you like (a Smartphone, Book, or even a
   Superhero!).
2. Add attributes and methods to bring the class to life!
3. Use constructors to initialize each object with unique values.
4. Add an inheritance layer to explore polymorphism or encapsulation.

## Activity 2: Polymorphism Challenge! 🎭

1. Create a program that includes animals or vehicles with the same action (like
   move()). However, make each class define move() differently (for example,
   Car.move() prints "Driving" 🚗, while Plane.move() prints "Flying" ✈️).

---

## Implementation Summary 📋

### Assignment 1 Answers ✅

1. **Create a class representing anything you like**:
   - **File**: `activity_1.py`
   - **Implementation**: `Superhero` abstract base class with `FlyingHero`,
     `TechHero`, and `HybridHero` subclasses

2. **Add attributes and methods to bring the class to life**:
   - **Attributes**: `name`, `real_name`, `health`, `energy`, `mission_count`,
     `flight_speed`, `tech_level`
   - **Methods**: `use_power()`, `heal()`, `take_damage()`, `introduce()`,
     `get_power_description()`

3. **Use constructors to initialize each object with unique values**:
   - **Example**:
     `iron_man = HybridHero("Iron Man", "Tony Stark", flight_speed=300, tech_level=5)`
   - Each hero gets unique initialization parameters

4. **Add an inheritance layer to explore polymorphism or encapsulation**:
   - **Inheritance**: `FlyingHero` and `TechHero` inherit from `Superhero`
   - **Multiple Inheritance**: `HybridHero` inherits from both `FlyingHero` and
     `TechHero`
   - **Polymorphism**: Each hero's `use_power()` method behaves differently
   - **Encapsulation**: Private attributes (`__health`, `__energy`) with
     property accessors

### Activity 2 Answers ✅

1. **Create a program with vehicles/animals with same action defined
   differently**:
   - **File**: `activity_2.py`
   - **Abstract Base**: `Vehicle` class with abstract `move()` method
   - **Polymorphic Implementations**:
     - `Car.move()`: "starts driving at X km/h!"
     - `Plane.move()`: "takes off and climbs to X meters!"
     - `Boat.move()`: "sets sail using propulsion!"
     - `Bicycle.move()`: "starts pedaling at X km/h!"
   - **Demonstrates**: Same method name, different behaviors (polymorphism)

## Files Overview 📁

- **`activity_1.py`**: Superhero OOP System - Inheritance, Polymorphism,
  Encapsulation
- **`activity_2.py`**: Vehicle Polymorphism System - Abstract classes,
  Polymorphism
- **`README.md`**: This documentation file
