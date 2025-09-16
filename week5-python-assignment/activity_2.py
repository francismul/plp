#!/usr/bin/env python3
"""
Vehicle Polymorphism System
Demonstrates polymorphism with different vehicles that all move differently!
"""

from abc import ABC, abstractmethod
import random
import time


class Vehicle(ABC):
    """
    Abstract base class for all vehicles.
    Defines common interface that all vehicles must implement.
    """

    def __init__(self, name, max_speed, fuel_capacity=100):
        """Initialize vehicle with basic properties."""
        self.name = name
        self.max_speed = max_speed  # km/h
        self.fuel_capacity = fuel_capacity
        self._current_fuel = fuel_capacity
        self._is_moving = False
        self._distance_traveled = 0  # km
        self._current_speed = 0

    @property
    def fuel_level(self):
        """Get current fuel level as percentage."""
        return (self._current_fuel / self.fuel_capacity) * 100

    @property
    def is_moving(self):
        """Check if vehicle is currently moving."""
        return self._is_moving

    @property
    def distance_traveled(self):
        """Get total distance traveled in km."""
        return self._distance_traveled

    def refuel(self):
        """Refuel the vehicle."""
        self._current_fuel = self.fuel_capacity
        return f"⛽ {self.name} refueled to 100%"

    def consume_fuel(self, amount):
        """Consume fuel, return True if successful."""
        if self._current_fuel >= amount:
            self._current_fuel -= amount
            return True
        return False

    @abstractmethod
    def move(self) -> str:
        """Abstract method - each vehicle moves differently!"""
        pass

    @abstractmethod
    def stop(self) -> str:
        """Abstract method - each vehicle stops differently!"""
        pass

    @abstractmethod
    def get_movement_sound(self) -> str:
        """Each vehicle makes different sounds when moving."""
        pass

    def get_status(self):
        """Get vehicle status information."""
        status = "Moving" if self._is_moving else "Stopped"
        return f"{self.name}: {status} | Fuel: {self.fuel_level:.1f}% | Distance: {self._distance_traveled:.1f} km"


class Car(Vehicle):
    """Car that drives on roads."""

    def __init__(self, name, max_speed=193, fuel_capacity=15):
        super().__init__(name, max_speed, fuel_capacity)
        self.gear = 1
        self.max_gear = 6

    def move(self):
        """Cars drive on roads!"""
        if self._current_fuel <= 0:
            return f"🚗 {self.name} is out of gas! Cannot drive."

        if self._is_moving:
            return f"🚗 {self.name} is already driving!"

        if self.consume_fuel(2):
            self._is_moving = True
            self._current_speed = random.randint(48, min(self.max_speed, 129))  # km/h
            distance = random.uniform(8, 24)  # km
            self._distance_traveled += distance

            return (f"🚗 {self.name} starts driving at {self._current_speed} km/h! "
                    f"{self.get_movement_sound()} Traveled {distance:.1f} km")
        else:
            return f"🚗 {self.name} doesn't have enough fuel to drive!"

    def stop(self):
        """Stop the car."""
        if not self._is_moving:
            return f"🚗 {self.name} is already stopped."

        self._is_moving = False
        self._current_speed = 0
        self.gear = 1
        return f"🚗 {self.name} pulls over and stops. *Brake sounds*"

    def get_movement_sound(self):
        """Car engine sounds."""
        sounds = ["Vroom vroom!", "Engine purring",
                  "Tires on asphalt", "Smooth acceleration"]
        return random.choice(sounds)

    def shift_gear(self):
        """Unique car action - gear shifting."""
        if self._is_moving and self.gear < self.max_gear:
            self.gear += 1
            return f"🚗 {self.name} shifts to gear {self.gear}!"
        return f"🚗 {self.name} cannot shift gears right now."


class Plane(Vehicle):
    """Airplane that flies through the sky."""

    def __init__(self, name, max_speed=805, fuel_capacity=1000):
        super().__init__(name, max_speed, fuel_capacity)
        self.altitude = 0
        self.max_altitude = 12192  # meters

    def move(self):
        """Planes fly through the air!"""
        if self._current_fuel <= 0:
            return f"✈️ {self.name} is out of fuel! Cannot take off."

        if self._is_moving:
            # Already flying, continue flight
            if self.consume_fuel(8):
                distance = random.uniform(80, 241)  # km
                self._distance_traveled += distance
                self.altitude = random.randint(7620, self.max_altitude)  # meters
                return (f"✈️ {self.name} continues flying at {self.altitude} meters! "
                        f"{self.get_movement_sound()} Covered {distance:.1f} km")
            else:
                return f"✈️ {self.name} is running low on fuel!"
        else:
            # Taking off
            if self.consume_fuel(15):
                self._is_moving = True
                self._current_speed = random.randint(322, self.max_speed)  # km/h
                self.altitude = random.randint(3048, 7620)  # meters
                distance = random.uniform(32, 80)  # km
                self._distance_traveled += distance

                return (f"✈️ {self.name} takes off and climbs to {self.altitude} meters! "
                        f"Flying at {self._current_speed} km/h. {self.get_movement_sound()}")
            else:
                return f"✈️ {self.name} doesn't have enough fuel for takeoff!"

    def stop(self):
        """Land the plane."""
        if not self._is_moving:
            return f"✈️ {self.name} is already on the ground."

        self._is_moving = False
        self._current_speed = 0
        self.altitude = 0
        return f"✈️ {self.name} descends and lands safely. Welcome to your destination!"

    def get_movement_sound(self):
        """Airplane sounds."""
        sounds = ["Jet engines roaring!", "Whoosh through clouds",
                  "Turbulence rumbling", "Smooth flight"]
        return random.choice(sounds)

    def change_altitude(self):
        """Unique plane action - altitude change."""
        if self._is_moving:
            new_altitude = random.randint(4572, self.max_altitude)  # meters
            old_altitude = self.altitude
            self.altitude = new_altitude
            direction = "climbing" if new_altitude > old_altitude else "descending"
            return f"✈️ {self.name} is {direction} to {new_altitude} meters!"
        return f"✈️ {self.name} must be flying to change altitude."


class Boat(Vehicle):
    """Boat that sails on water."""

    def __init__(self, name, max_speed=56, fuel_capacity=50):
        super().__init__(name, max_speed, fuel_capacity)
        self.sail_raised = False
        self.anchor_down = False

    def move(self):
        """Boats sail on water!"""
        if self.anchor_down:
            return f"⛵ {self.name} cannot move with anchor down!"

        if self._current_fuel <= 0 and not self.sail_raised:
            return f"⛵ {self.name} is out of fuel and has no wind power!"

        if self._is_moving:
            # Continue sailing
            fuel_needed = 3 if not self.sail_raised else 1
            if self.consume_fuel(fuel_needed):
                distance = random.uniform(15, 46)  # km
                self._distance_traveled += distance
                return (f"⛵ {self.name} continues sailing smoothly! "
                        f"{self.get_movement_sound()} Sailed {distance:.1f} km")
            else:
                return f"⛵ {self.name} is drifting - low on fuel!"
        else:
            # Start sailing
            fuel_needed = 5 if not self.sail_raised else 2
            if self.consume_fuel(fuel_needed):
                self._is_moving = True
                self._current_speed = random.randint(16, self.max_speed)  # km/h
                distance = random.uniform(6, 22)  # km
                self._distance_traveled += distance

                propulsion = "wind and engine" if self.sail_raised else "engine power"
                return (f"⛵ {self.name} sets sail using {propulsion}! "
                        f"Speed: {self._current_speed} km/h. {self.get_movement_sound()}")
            else:
                return f"⛵ {self.name} needs fuel or wind to start sailing!"

    def stop(self):
        """Stop the boat."""
        if not self._is_moving:
            return f"⛵ {self.name} is already anchored."

        self._is_moving = False
        self._current_speed = 0
        self.anchor_down = True
        return f"⛵ {self.name} drops anchor and stops. *Splash*"

    def get_movement_sound(self):
        """Boat water sounds."""
        sounds = ["Waves splashing!", "Water rushing past hull",
                  "Gentle sea breeze", "Peaceful sailing"]
        return random.choice(sounds)

    def raise_sail(self):
        """Unique boat action - sail management."""
        if not self.sail_raised:
            self.sail_raised = True
            return f"⛵ {self.name} raises the sail! Wind power activated!"
        return f"⛵ {self.name}'s sail is already raised."

    def lower_sail(self):
        """Lower the sail."""
        if self.sail_raised:
            self.sail_raised = False
            return f"⛵ {self.name} lowers the sail."
        return f"⛵ {self.name}'s sail is already down."


class Bicycle(Vehicle):
    """Human-powered bicycle."""

    def __init__(self, name, max_speed=40):
        super().__init__(name, max_speed, fuel_capacity=100)  # "Fuel" represents energy
        self.pedaling_intensity = "leisurely"

    def move(self):
        """Bicycles are pedaled by humans!"""
        if self._current_fuel <= 0:
            return f"🚲 {self.name} rider is too tired to pedal!"

        if self._is_moving:
            # Continue pedaling
            energy_used = random.randint(3, 8)
            if self.consume_fuel(energy_used):
                distance = random.uniform(1.6, 8)  # km
                self._distance_traveled += distance
                return (f"🚲 {self.name} keeps pedaling {self.pedaling_intensity}! "
                        f"{self.get_movement_sound()} Rode {distance:.1f} km")
            else:
                return f"🚲 {self.name} rider is getting tired!"
        else:
            # Start pedaling
            energy_used = random.randint(5, 12)
            if self.consume_fuel(energy_used):
                self._is_moving = True
                self._current_speed = random.randint(13, self.max_speed)  # km/h
                distance = random.uniform(0.8, 5)  # km
                self._distance_traveled += distance

                return (f"🚲 {self.name} starts pedaling at {self._current_speed} km/h! "
                        f"{self.get_movement_sound()} Great exercise!")
            else:
                return f"🚲 {self.name} rider needs to rest first!"

    def stop(self):
        """Stop the bicycle."""
        if not self._is_moving:
            return f"🚲 {self.name} is already stopped."

        self._is_moving = False
        self._current_speed = 0
        return f"🚲 {self.name} brakes and comes to a stop. Time for a water break!"

    def get_movement_sound(self):
        """Bicycle sounds."""
        sounds = ["Chain clicking smoothly", "Tires rolling on pavement",
                  "Wind in your face", "Peaceful pedaling"]
        return random.choice(sounds)

    def refuel(self):
        """Rest to restore energy."""
        self._current_fuel = self.fuel_capacity
        return f"🚲 {self.name} rider takes a rest and feels refreshed!"

    def change_intensity(self):
        """Change pedaling intensity."""
        intensities = ["leisurely", "moderate", "intense", "racing"]
        old_intensity = self.pedaling_intensity
        self.pedaling_intensity = random.choice(intensities)
        return f"🚲 {self.name} changes from {old_intensity} to {self.pedaling_intensity} pedaling!"


class TransportManager:
    """Manages a fleet of vehicles - demonstrates polymorphism."""

    def __init__(self):
        """Initialize transport manager."""
        self.fleet = []

    def add_vehicle(self, vehicle):
        """Add a vehicle to the fleet."""
        if isinstance(vehicle, Vehicle):
            self.fleet.append(vehicle)
            return f"✅ Added {vehicle.name} to the fleet!"
        return "❌ Only Vehicle objects can be added to the fleet."

    def move_all_vehicles(self):
        """Move all vehicles - polymorphism in action!"""
        if not self.fleet:
            return "No vehicles in fleet."

        print("🚀 Moving all vehicles in the fleet:")
        print("=" * 50)

        results = []
        for vehicle in self.fleet:
            # This is polymorphism! Each vehicle's move() method behaves differently
            result = vehicle.move()
            results.append(result)
            print(f"  {result}")

        return results

    def stop_all_vehicles(self):
        """Stop all vehicles."""
        print("🛑 Stopping all vehicles:")
        print("=" * 30)

        for vehicle in self.fleet:
            # Polymorphism again! Each stop() method is different
            result = vehicle.stop()
            print(f"  {result}")

    def fleet_status(self):
        """Show status of all vehicles."""
        if not self.fleet:
            return "Fleet is empty."

        print("📊 Fleet Status Report:")
        print("=" * 40)

        total_distance = 0
        moving_count = 0

        for vehicle in self.fleet:
            status = vehicle.get_status()
            print(f"  {status}")
            total_distance += vehicle.distance_traveled
            if vehicle.is_moving:
                moving_count += 1

        print(f"\n📈 Fleet Summary:")
        print(f"  Total Vehicles: {len(self.fleet)}")
        print(f"  Currently Moving: {moving_count}")
        print(f"  Total Distance Traveled: {total_distance:.1f} km")

    def refuel_all(self):
        """Refuel all vehicles."""
        print("⛽ Refueling all vehicles:")
        print("=" * 30)

        for vehicle in self.fleet:
            result = vehicle.refuel()
            print(f"  {result}")


def demo_vehicle_polymorphism():
    """Demonstrate vehicle polymorphism in action!"""
    print("🚗✈️⛵ Vehicle Polymorphism Demo 🚲🚀")
    print("=" * 60)

    # Create different vehicles
    print("\n1. Creating Vehicle Fleet:")
    print("-" * 30)

    manager = TransportManager()

    # Create various vehicles
    vehicles = [
        Car("Lightning McQueen", max_speed=290),  # ~180 mph
        Plane("Sky Explorer", max_speed=724),  # ~450 mph
        Boat("Sea Breeze", max_speed=65),  # ~40 mph
        Bicycle("Green Rider", max_speed=48),  # ~30 mph
        Car("City Cruiser", max_speed=145)  # ~90 mph
    ]

    for vehicle in vehicles:
        print(f"  {manager.add_vehicle(vehicle)}")

    # Demonstrate polymorphism - same method call, different behaviors!
    print("\n2. Polymorphism Demo - All vehicles move() differently:")
    print("-" * 60)
    manager.move_all_vehicles()

    print("\n3. Fleet Status After Movement:")
    print("-" * 35)
    manager.fleet_status()

    # Show unique vehicle abilities
    print("\n4. Unique Vehicle Actions:")
    print("-" * 30)

    # Car-specific actions
    car = vehicles[0]  # Lightning McQueen
    print(f"  {car.shift_gear()}")

    # Plane-specific actions
    plane = vehicles[1]  # Sky Explorer
    print(f"  {plane.change_altitude()}")

    # Boat-specific actions
    boat = vehicles[2]  # Sea Breeze
    print(f"  {boat.raise_sail()}")

    # Bicycle-specific actions
    bike = vehicles[3]  # Green Rider
    print(f"  {bike.change_intensity()}")

    # Continue moving to show different behaviors
    print("\n5. Second Round of Movement:")
    print("-" * 32)
    manager.move_all_vehicles()

    # Demonstrate stopping - another polymorphic method
    print("\n6. Stopping All Vehicles (Polymorphism Again!):")
    print("-" * 50)
    manager.stop_all_vehicles()

    # Final status
    print("\n7. Final Fleet Status:")
    print("-" * 22)
    manager.fleet_status()

    print("\n🎉 Demo Complete! Each vehicle moved differently using the same method name!")
    print("This is the power of polymorphism in object-oriented programming!")


if __name__ == "__main__":
    demo_vehicle_polymorphism()
