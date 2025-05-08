from datetime import datetime
import os

# Base class
class Flight:
    def __init__(self, flight_id, source, destination, departure, arrival, aircraft_id=None):
        self.flight_id = flight_id
        self.source = source
        self.destination = destination
        self.departure = departure  # datetime object
        self.arrival = arrival
        self.aircraft_id = aircraft_id

    def display_schedule(self):
        print(f"[Flight {self.flight_id}] {self.source} ➡ {self.destination}")
        print(f"Departure: {self.departure} | Arrival: {self.arrival}")

    def reschedule(self, new_departure, new_arrival):
        self.departure = new_departure
        self.arrival = new_arrival


class Passenger:
    def __init__(self, passenger_id, name, contact, passport_number=None):
        self.passenger_id = passenger_id
        self.name = name
        self.contact = contact
        self.passport_number = passport_number
    
    def display_info(self):
        print(f"Passenger: {self.name} (ID: {self.passenger_id})")
        print(f"Contact: {self.contact} | Passport: {self.passport_number or 'N/A'}")


class PassengerFlight(Flight):
    def __init__(self, flight_id, source, destination, departure, arrival, aircraft_id, capacity):
        super().__init__(flight_id, source, destination, departure, arrival, aircraft_id)
        self.passenger_capacity = capacity
        self.passengers = []  # Store actual passenger objects
    
    def book_seat(self, passenger):
        if len(self.passengers) < self.passenger_capacity:
            self.passengers.append(passenger)
            return True
        return False
    
    def get_passenger(self, passenger_id):
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                return passenger
        return None
    
    def cancel_booking(self, passenger_id):
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                self.passengers.remove(passenger)
                return True
        return False

    def available_seats(self):
        return self.passenger_capacity - len(self.passengers)
        
    def list_passengers(self):
        if not self.passengers:
            print("No passengers booked on this flight.")
            return
        
        print(f"\nPassengers on Flight {self.flight_id} ({len(self.passengers)} total):")
        for passenger in self.passengers:
            passenger.display_info()


class Cargo:
    def __init__(self, cargo_id, description, weight, owner_name):
        self.cargo_id = cargo_id
        self.description = description
        self.weight = weight
        self.owner_name = owner_name


class CargoFlight(Flight):
    def __init__(self, flight_id, source, destination, departure, arrival, aircraft_id, max_cargo_weight):
        super().__init__(flight_id, source, destination, departure, arrival, aircraft_id)
        self.max_cargo_weight = max_cargo_weight
        self.current_cargo_weight = 0
        self.cargo_list = []

    def add_cargo(self, cargo):
        if self.current_cargo_weight + cargo.weight <= self.max_cargo_weight:
            self.cargo_list.append(cargo)
            self.current_cargo_weight += cargo.weight
            return True
        return False

    def remove_cargo(self, cargo_id):
        for cargo in self.cargo_list:
            if cargo.cargo_id == cargo_id:
                self.current_cargo_weight -= cargo.weight
                self.cargo_list.remove(cargo)
                return True
        return False

    def available_cargo_space(self):
        return self.max_cargo_weight - self.current_cargo_weight


class Scheduler:
    def __init__(self):
        self.flights = {}

    def schedule_flight(self, flight):
        self.flights[flight.flight_id] = flight
        return True

    def cancel_flight(self, flight_id):
        if flight_id in self.flights:
            del self.flights[flight_id]
            return True
        return False

    def get_schedule_by_date(self, date, sort=False):
        flights_on_date = []
        for flight in self.flights.values():
            if flight.departure.date() == date.date():
                flights_on_date.append(flight)
        
        if sort:
            flights_on_date.sort(key=lambda f: f.departure)
        
        return flights_on_date
    
    def get_flights_by_criteria(self, criteria_type, criteria_value):
        matching_flights = []
        for flight in self.flights.values():
            if criteria_type == 'source' and flight.source.lower() == criteria_value.lower():
                matching_flights.append(flight)
            elif criteria_type == 'destination' and flight.destination.lower() == criteria_value.lower():
                matching_flights.append(flight)
            elif criteria_type == 'aircraft_id' and flight.aircraft_id and flight.aircraft_id.lower() == criteria_value.lower():
                matching_flights.append(flight)
        
        return matching_flights


def get_valid_datetime(prompt):
    """Get a valid datetime from user with proper error handling"""
    while True:
        try:
            date_str = input(prompt + " (YYYY-MM-DD HH:MM): ")
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD HH:MM.")


def get_valid_date(prompt):
    """Get a valid date from user with proper error handling"""
    while True:
        try:
            date_str = input(prompt + " (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return datetime.combine(date.date(), datetime.min.time())
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def main():
    scheduler = Scheduler()
    
    # Sample data for testing
    # Add some sample flights to make testing easier
    today = datetime.now()
    
    # Add a passenger flight
    pf = PassengerFlight(
        "BA123", "London", "New York", 
        datetime(today.year, today.month, today.day, 9, 0), 
        datetime(today.year, today.month, today.day, 17, 0),
        "A380-001", 250
    )
    scheduler.schedule_flight(pf)
    
    # Add a cargo flight
    cf = CargoFlight(
        "CG456", "Dubai", "Singapore", 
        datetime(today.year, today.month, today.day, 14, 0), 
        datetime(today.year, today.month, today.day, 22, 0),
        "B747-002", 5000
    )
    scheduler.schedule_flight(cf)
    
    while True:
        print("\n===== FLIGHT MANAGEMENT SYSTEM =====")
        print("1. Schedule a Flight")
        print("2. Manage Flights")
        print("3. Manage Bookings/Cargo")
        print("4. View Schedules")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            # Schedule a flight
            flight_type = input("Flight type (P for Passenger, C for Cargo): ").upper()
            
            flight_id = input("Flight ID: ")
            source = input("Source airport: ")
            destination = input("Destination airport: ")
            departure = get_valid_datetime("Departure time")
            arrival = get_valid_datetime("Arrival time")
            aircraft_id = input("Aircraft ID (optional): ") or None
            
            if flight_type == 'P':
                try:
                    capacity = int(input("Passenger capacity: "))
                    flight = PassengerFlight(flight_id, source, destination, departure, arrival, aircraft_id, capacity)
                    if scheduler.schedule_flight(flight):
                        print(f"Passenger flight {flight_id} scheduled successfully.")
                except ValueError:
                    print("Invalid capacity. Please enter a number.")
            
            elif flight_type == 'C':
                try:
                    max_weight = float(input("Maximum cargo weight (kg): "))
                    flight = CargoFlight(flight_id, source, destination, departure, arrival, aircraft_id, max_weight)
                    if scheduler.schedule_flight(flight):
                        print(f"Cargo flight {flight_id} scheduled successfully.")
                except ValueError:
                    print("Invalid weight. Please enter a number.")
            
            else:
                print("Invalid flight type.")
        
        elif choice == '2':
            # Manage flights
            print("\n--- MANAGE FLIGHTS ---")
            print("1. Cancel a flight")
            print("2. Reschedule a flight")
            print("3. Return to main menu")
            
            sub_choice = input("Enter choice (1-3): ")
            
            if sub_choice == '1':
                flight_id = input("Enter flight ID to cancel: ")
                if scheduler.cancel_flight(flight_id):
                    print(f"Flight {flight_id} cancelled successfully.")
                else:
                    print("Flight not found.")
            
            elif sub_choice == '2':
                flight_id = input("Enter flight ID to reschedule: ")
                if flight_id in scheduler.flights:
                    new_departure = get_valid_datetime("New departure time")
                    new_arrival = get_valid_datetime("New arrival time")
                    scheduler.flights[flight_id].reschedule(new_departure, new_arrival)
                    print(f"Flight {flight_id} rescheduled successfully.")
                else:
                    print("Flight not found.")
        
        elif choice == '3':
            # Manage bookings/cargo
            print("\n--- MANAGE BOOKINGS/CARGO ---")
            print("1. Book a seat")
            print("2. Cancel a booking")
            print("3. List passengers on a flight")
            print("4. Add cargo to a flight")
            print("5. Remove cargo from a flight")
            print("6. Return to main menu")
            
            sub_choice = input("Enter choice (1-6): ")
            
            if sub_choice == '1':
                flight_id = input("Enter passenger flight ID: ")
                if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], PassengerFlight):
                    flight = scheduler.flights[flight_id]
                    
                    # Check if seats are available first
                    if flight.available_seats() <= 0:
                        print("No available seats on this flight.")
                        continue
                    
                    # Get passenger details
                    print("\n--- Passenger Information ---")
                    passenger_id = input("Passenger ID (e.g., passport or ID number): ")
                    name = input("Full name: ")
                    contact = input("Contact information (phone/email): ")
                    passport = input("Passport number (optional): ") or None
                    
                    # Create passenger object and book
                    passenger = Passenger(passenger_id, name, contact, passport)
                    if flight.book_seat(passenger):
                        print(f"Booking confirmed for {name} on flight {flight_id}.")
                        print(f"{flight.available_seats()} seats remaining.")
                    else:
                        print("Booking failed. Flight might be full.")
                else:
                    print("Invalid flight ID or not a passenger flight.")
            
            elif sub_choice == '2':
                flight_id = input("Enter passenger flight ID: ")
                if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], PassengerFlight):
                    flight = scheduler.flights[flight_id]
                    passenger_id = input("Enter passenger ID to cancel booking: ")
                    
                    if flight.cancel_booking(passenger_id):
                        print(f"Booking cancelled successfully. {flight.available_seats()} seats now available.")
                    else:
                        print("Passenger not found on this flight.")
                else:
                    print("Invalid flight ID or not a passenger flight.")
            
            elif sub_choice == '3':
                flight_id = input("Enter passenger flight ID: ")
                if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], PassengerFlight):
                    scheduler.flights[flight_id].list_passengers()
                else:
                    print("Invalid flight ID or not a passenger flight.")
            
            elif sub_choice == '4':
                flight_id = input("Enter cargo flight ID: ")
                if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], CargoFlight):
                    flight = scheduler.flights[flight_id]
                    
                    cargo_id = input("Cargo ID: ")
                    description = input("Cargo description: ")
                    
                    try:
                        weight = float(input("Cargo weight (kg): "))
                        owner = input("Cargo owner: ")
                        
                        cargo = Cargo(cargo_id, description, weight, owner)
                        if flight.add_cargo(cargo):
                            print(f"Cargo added. Available space: {flight.available_cargo_space()} kg.")
                        else:
                            print("Not enough space for this cargo.")
                    except ValueError:
                        print("Invalid weight. Please enter a number.")
                else:
                    print("Invalid flight ID or not a cargo flight.")
            
            elif sub_choice == '5':
                flight_id = input("Enter cargo flight ID: ")
                if flight_id in scheduler.flights and isinstance(scheduler.flights[flight_id], CargoFlight):
                    cargo_id = input("Enter cargo ID to remove: ")
                    if scheduler.flights[flight_id].remove_cargo(cargo_id):
                        print("Cargo removed successfully.")
                    else:
                        print("Cargo not found.")
                else:
                    print("Invalid flight ID or not a cargo flight.")
        
        elif choice == '4':
            # View schedules
            print("\n--- VIEW SCHEDULES ---")
            print("1. View flights by date")
            print("2. View flights by source")
            print("3. View flights by destination")
            print("4. View flights by aircraft ID")
            print("5. Return to main menu")
            
            sub_choice = input("Enter choice (1-5): ")
            
            if sub_choice == '1':
                date = get_valid_date("Enter date")
                sort_option = input("Sort by departure time? (y/n): ").lower() == 'y'
                flights = scheduler.get_schedule_by_date(date, sort_option)
                
                if not flights:
                    print(f"No flights found on {date.date()}")
                else:
                    print(f"\nFlights on {date.date()}:")
                    for flight in flights:
                        flight.display_schedule()
            
            elif sub_choice in ['2', '3', '4']:
                criteria_type = {
                    '2': 'source',
                    '3': 'destination',
                    '4': 'aircraft_id'
                }[sub_choice]
                
                criteria_name = {
                    'source': 'source airport',
                    'destination': 'destination airport',
                    'aircraft_id': 'aircraft ID'
                }[criteria_type]
                
                criteria_value = input(f"Enter {criteria_name}: ")
                flights = scheduler.get_flights_by_criteria(criteria_type, criteria_value)
                
                if not flights:
                    print(f"No flights found with {criteria_name} '{criteria_value}'")
                else:
                    print(f"\nFlights with {criteria_name} '{criteria_value}':")
                    for flight in flights:
                        flight.display_schedule()
        
        elif choice == '5':
            print("Thank you for using the Flight Management System. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()