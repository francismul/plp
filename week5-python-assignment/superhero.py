"""
Superhero OOP
Demonstrates classes, inheritance, polymorphism, and encapsulation
"""

import random
from abc import ABC, abstractmethod


class Superhero(ABC):
    """
    Abstract base class for all superheroes.
    Demonstrates encapsulation with private attributes and methods.
    Enforces implementation of specific methods in subclasses.
    """

    # Class variable shared by all superheroes
    total_heroes = 0

    def __init__(self, name, real_name, health=100, energy=100):
        """
        Constructor to initialize superhero with unique values.
        Uses name mangling for truly private attributes.
        """
        if not name or not real_name:
            raise ValueError("Name and real name cannot be empty")

        self._name = name  # Protected attribute
        self._real_name = real_name  # Protected attribute
        # Private attribute with validation
        self.__health = max(0, min(100, health))
        # Private attribute with validation
        self.__energy = max(0, min(100, energy))
        self.__is_active = True
        self._mission_count = 0

        Superhero.total_heroes += 1

    # Property decorators for controlled access to private attributes
    @property
    def name(self):
        """Getter for hero name."""
        return self._name

    @property
    def real_name(self):
        """Getter for real name."""
        return self._real_name

    @property
    def health(self):
        """Getter for health."""
        return self.__health

    @property
    def energy(self):
        """Getter for energy."""
        return self.__energy

    @property
    def is_active(self):
        """Check if hero is active."""
        return self.__is_active and self.__health > 0

    @property
    def mission_count(self):
        """Get number of completed missions."""
        return self._mission_count

    # Methods to modify private attributes safely
    def take_damage(self, damage):
        """Reduce health by damage amount."""
        if damage < 0:
            raise ValueError("Damage cannot be negative")

        self.__health = max(0, self.__health - damage)
        if self.__health == 0:
            self.__is_active = False
            print(f"{self._name} has been defeated!")

    def heal(self, amount):
        """Restore health."""
        if amount < 0:
            raise ValueError("Heal amount cannot be negative")

        old_health = self.__health
        self.__health = min(100, self.__health + amount)
        if not self.__is_active and self.__health > 0:
            self.__is_active = True
            print(f"{self._name} is back in action!")
        return self.__health - old_health

    def use_energy(self, amount):
        """Use energy for actions."""
        if amount < 0:
            raise ValueError("Energy usage cannot be negative")

        if self.__energy < amount:
            return False  # Not enough energy
        self.__energy -= amount
        return True

    def rest(self, amount=20):
        """Restore energy by resting."""
        self.__energy = min(100, self.__energy + amount)

    def complete_mission(self):
        """Mark a mission as completed."""
        if self.is_active:
            self._mission_count += 1
            return True
        return False

    # Abstract methods that must be implemented by subclasses
    @abstractmethod
    def use_power(self) -> str:
        """Each superhero must implement their unique power and return a string describing the action."""
        pass

    @abstractmethod
    def get_power_description(self) -> str:
        """Get description of the hero's power."""
        pass

    # Common methods
    def introduce(self):
        """Hero introduces themselves."""
        status = "Active" if self.is_active else "Inactive"
        return f"I am {self._name}, also known as {self._real_name}. Status: {status}"

    def get_stats(self):
        """Return hero's current statistics."""
        return {
            'name': self._name,
            'health': self.__health,
            'energy': self.__energy,
            'active': self.__is_active,
            'missions': self._mission_count
        }

    def __str__(self):
        """String representation of the hero."""
        return f"{self._name} (Health: {self.__health}, Energy: {self.__energy})"

    def __repr__(self):
        """Developer-friendly representation."""
        return f"Superhero(name='{self._name}', real_name='{self._real_name}', health={self.__health}, energy={self.__energy})"


class FlyingHero(Superhero):
    """
    Superhero with flying abilities.
    Demonstrates inheritance and method overriding.
    """

    def __init__(self, name, real_name, flight_speed=100, altitude_limit=10000, **kwargs):
        """Initialize flying hero with additional flight attributes."""
        health = kwargs.pop('health', 100)
        energy = kwargs.pop('energy', 100)
        super().__init__(name, real_name, health=health, energy=energy, **kwargs)
        self.flight_speed = kwargs.pop('flight_speed', flight_speed)  # mph
        self.altitude_limit = kwargs.pop('altitude_limit', altitude_limit)  # feet
        self.__is_flying = False

    @property
    def is_flying(self):
        """Check if hero is currently flying."""
        return self.__is_flying

    def take_flight(self):
        """Take off and start flying."""
        if not self.is_active:
            return False, "Cannot fly while inactive"

        if not self.use_energy(10):
            return False, "Not enough energy to fly"

        self.__is_flying = True
        return True, f"{self.name} takes flight at {self.flight_speed} mph!"

    def land(self):
        """Land safely."""
        if self.__is_flying:
            self.__is_flying = False
            return f"{self.name} lands safely."
        return f"{self.name} is already on the ground."

    def use_power(self):
        """Use flying power."""
        if not self.is_active:
            return "Cannot use power while inactive"

        if self.__is_flying:
            # Perform aerial maneuver
            if self.use_energy(15):
                damage_dealt = random.randint(20, 35)
                return f"{self.name} performs aerial assault dealing {damage_dealt} damage!"
            else:
                return f"{self.name} is too tired for aerial maneuvers"
        else:
            # Take flight first
            success, message = self.take_flight()
            return message

    def get_power_description(self):
        """Describe flying abilities."""
        return f"Flight at {self.flight_speed} mph, max altitude {self.altitude_limit} feet"


class TechHero(Superhero):
    """
    Technology-based superhero.
    Demonstrates composition and method overriding.
    """

    def __init__(self, name, real_name, gadget_count=5, tech_level=1, **kwargs):
        """Initialize tech hero with gadgets and tech level."""
        health = kwargs.pop('health', 100)
        energy = kwargs.pop('energy', 100)
        super().__init__(name, real_name, health=health, energy=energy)
        self.gadget_count = kwargs.pop('gadget_count', gadget_count)
        self.tech_level = kwargs.pop('tech_level', tech_level)
        self.__gadgets = self._initialize_gadgets()

    def _initialize_gadgets(self):
        """Private method to set up initial gadgets."""
        basic_gadgets = ['Scanner', 'Communicator', 'Grappling Hook']
        advanced_gadgets = [
            'Energy Shield', 'Holographic Projector', 'Nano Repair Kit'
        ]

        gadgets = basic_gadgets.copy()
        if self.tech_level > 1:
            gadgets.extend(advanced_gadgets[:self.tech_level-1])

        return gadgets[:self.gadget_count]

    @property
    def available_gadgets(self):
        """Get list of available gadgets."""
        return self.__gadgets.copy()  # Return copy to prevent external modification

    def upgrade_tech(self):
        """Upgrade technology level."""
        if self.use_energy(25):
            self.tech_level += 1
            self.__gadgets = self._initialize_gadgets()
            return f"{self.name} upgraded to tech level {self.tech_level}!"
        return f"{self.name} needs more energy to upgrade"

    def use_power(self):
        """Use technological abilities."""
        if not self.is_active:
            return "Cannot use power while inactive"

        if not self.__gadgets:
            return f"{self.name} has no gadgets available"

        if self.use_energy(12):
            gadget = random.choice(self.__gadgets)
            damage_dealt = random.randint(15, 25) * self.tech_level
            return f"{self.name} uses {gadget} dealing {damage_dealt} tech damage!"
        else:
            return f"{self.name} has insufficient power for gadgets"

    def get_power_description(self):
        """Describe tech abilities."""
        return f"Tech Level {self.tech_level} with gadgets: {', '.join(self.__gadgets)}"


class HybridHero(FlyingHero, TechHero):
    """
    Hero with both flying and tech abilities.
    Demonstrates multiple inheritance and method resolution order.
    """

    def __init__(self, name, real_name, **kwargs):
        """Initialize hybrid hero with both flying and tech abilities."""
        health = kwargs.pop('health', 100)
        energy = kwargs.pop('energy', 100)
        super().__init__(name, real_name, health=health, energy=energy, **kwargs)
        self.__combo_moves = ['Sky Strike', 'Aerial Hack', 'Flying Fortress']

    def use_power(self):
        """Override to use combined abilities."""
        if not self.is_active:
            return "Cannot use power while inactive"

        if self.use_energy(20):
            # Use combination of both powers
            combo_move = random.choice(self.__combo_moves)
            base_damage = random.randint(25, 40)
            tech_bonus = self.tech_level * 5
            flight_bonus = 10 if self.is_flying else 0
            total_damage = base_damage + tech_bonus + flight_bonus

            return f"{self.name} uses {combo_move} dealing {total_damage} combined damage!"
        else:
            return f"{self.name} lacks energy for combo moves"

    def get_power_description(self):
        """Describe combined abilities."""
        return f"Hybrid abilities: {FlyingHero.get_power_description(self)} + {TechHero.get_power_description(self)}"


class Team:
    """
    Team of superheroes demonstrating composition and polymorphism.
    """

    def __init__(self, team_name):
        """Initialize team with a name."""
        self.team_name = team_name
        self.__members = []
        self.__team_missions = 0

    def add_member(self, hero):
        """Add a hero to the team."""
        if not isinstance(hero, Superhero):
            raise TypeError("Only Superhero instances can join the team")

        if hero not in self.__members:
            self.__members.append(hero)
            return f"{hero.name} joined {self.team_name}!"
        return f"{hero.name} is already a team member"

    def remove_member(self, hero):
        """Remove a hero from the team."""
        if hero in self.__members:
            self.__members.remove(hero)
            return f"{hero.name} left {self.team_name}"
        return f"{hero.name} is not a team member"

    @property
    def members(self):
        """Get list of team members."""
        return self.__members.copy()

    @property
    def active_members(self):
        """Get list of active team members."""
        return [member for member in self.__members if member.is_active]

    def team_attack(self):
        """All active members use their powers - demonstrates polymorphism."""
        if not self.active_members:
            return "No active members available for team attack"

        results = []
        for member in self.active_members:
            # Polymorphism: each hero's use_power() method behaves differently
            result = member.use_power()
            results.append(f"  {result}")

        self.__team_missions += 1
        for member in self.active_members:
            member.complete_mission()

        return f"{self.team_name} Team Attack #{self.__team_missions}:\n" + "\n".join(results)

    def get_team_stats(self):
        """Get comprehensive team statistics."""
        total_health = sum(member.health for member in self.__members)
        total_energy = sum(member.energy for member in self.__members)
        total_missions = sum(member.mission_count for member in self.__members)

        return {
            'team_name': self.team_name,
            'total_members': len(self.__members),
            'active_members': len(self.active_members),
            'team_health': total_health,
            'team_energy': total_energy,
            'total_missions': total_missions,
            'team_missions': self.__team_missions
        }


def demo_superhero_system():
    """Demonstrate the superhero OOP system."""
    print("🦸 Superhero OOP System Demo 🦸")
    print("=" * 50)

    # Create different types of heroes
    print("\n1. Creating Heroes:")
    print("-" * 20)

    superman = FlyingHero(
        "Superman", "Clark Kent", flight_speed=500, health=95)
    batman = TechHero(
        "Batman", "Bruce Wayne", gadget_count=8, tech_level=3, energy=90)
    iron_man = HybridHero(
        "Iron Man", "Tony Stark", flight_speed=300, tech_level=5)

    heroes = [superman, batman, iron_man]

    for hero in heroes:
        print(hero.introduce())
        print(f"  Power: {hero.get_power_description()}")

    # Demonstrate encapsulation
    print("\n2. Demonstrating Encapsulation:")
    print("-" * 35)
    print(f"Superman's health: {superman.health}")
    print("Taking 30 damage...")
    superman.take_damage(30)
    print(f"Superman's health after damage: {superman.health}")
    print("Healing 20 points...")
    healed = superman.heal(20)
    print(
        f"Superman healed {healed} points, current health: {superman.health}")

    # Demonstrate polymorphism
    print("\n3. Demonstrating Polymorphism:")
    print("-" * 32)
    for hero in heroes:
        print(f"{hero.name}: {hero.use_power()}")

    # Create and demonstrate team
    print("\n4. Team Operations:")
    print("-" * 18)

    justice_league = Team("Justice League")

    for hero in heroes:
        print(justice_league.add_member(hero))

    print(
        f"\nTeam Members: {[member.name for member in justice_league.members]}")
    print(
        f"Active Members: {[member.name for member in justice_league.active_members]}")

    print("\n" + justice_league.team_attack())

    # Show final statistics
    print("\n5. Final Statistics:")
    print("-" * 19)

    print(f"Total Heroes Created: {Superhero.total_heroes}")

    team_stats = justice_league.get_team_stats()
    for key, value in team_stats.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    print("\nIndividual Hero Stats:")
    for hero in heroes:
        stats = hero.get_stats()
        print(f"  {hero.name}: {stats}")


if __name__ == "__main__":
    demo_superhero_system()
