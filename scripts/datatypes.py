from typing import TypedDict, List, Optional
from datetime import datetime


class Config(TypedDict):
    backend_url: str


class Vehicle(TypedDict, total=False):
    """Represents a vehicle in the system"""
    id: str  # Required field
    coordX: float  # Required field
    coordY: float  # Required field
    isAvailable: bool
    vehicleSpeed: float
    customerId: str
    remainingTravelTime: float
    distanceTravelled: float
    activeTime: float
    numberOfTrips: int


class VehicleUpdate(TypedDict, total=False):
    """Represents an update to a vehicle's information"""
    id: str  # Required field
    customerId: str


class Customer(TypedDict, total=False):
    """Represents a customer in the system"""
    id: str  # Required field
    coordX: float
    coordY: float
    destinationX: float
    destinationY: float
    awaitingService: bool


class Scenario(TypedDict, total=False):
    """Represents a complete scenario with vehicles and customers"""
    id: str  # Required field
    vehicles: List[Vehicle]  # Required field
    customers: List[Customer]  # Required field
    startTime: str
    endTime: str
    status: str


class UpdateScenario(TypedDict):
    """Represents an update to a scenario"""
    vehicles: List[VehicleUpdate]


class UpdateScenarioResponse(TypedDict, total=False):
    """Represents the response to an update scenario request"""
    updated_vehicles: List[Vehicle]  # Required field
    failed_to_update: List[Vehicle]


class InitializeScenarioResponse(TypedDict, total=False):
    """Represents the response to an initialize scenario request"""
    message: str  # Required field
    error: str
    scenario: Scenario


class LaunchScenarioResponse(TypedDict):
    """Represents the response to a launch scenario request"""
    message: str
    scenario_id: str
    startTime: str
