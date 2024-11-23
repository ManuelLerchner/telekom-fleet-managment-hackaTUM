from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Vehicle:
    """Represents a vehicle in the system"""
    id: str
    coordX: float
    coordY: float
    isAvailable: Optional[bool] = None
    vehicleSpeed: Optional[float] = None
    customerId: Optional[str] = None
    remainingTravelTime: Optional[float] = None
    distanceTravelled: Optional[float] = None
    activeTime: Optional[float] = None
    numberOfTrips: Optional[int] = None


@dataclass
class VehicleUpdate:
    """Represents an update to a vehicle's information"""
    id: str
    customerId: Optional[str] = None


@dataclass
class Customer:
    """Represents a customer in the system"""
    id: str
    coordX: Optional[float] = None
    coordY: Optional[float] = None
    destinationX: Optional[float] = None
    destinationY: Optional[float] = None
    awaitingService: Optional[bool] = None


@dataclass
class Scenario:
    """Represents a complete scenario with vehicles and customers"""
    id: str
    vehicles: List[Vehicle]
    customers: List[Customer]
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    status: Optional[str] = None


@dataclass
class UpdateScenario:
    """Represents an update to a scenario"""
    vehicles: List[VehicleUpdate]


@dataclass
class UpdateScenarioResponse:
    """Represents the response to an update scenario request"""
    updated_vehicles: List[Vehicle]
    failed_to_update: Optional[List[Vehicle]]


@dataclass
class InitializeScenarioResponse:
    """Represents the response to an initialize scenario request"""
    message: str
    error: Optional[str]
    scenario: Scenario


@dataclass
class LaunchScenarioResponse:
    """Represents the response to a launch scenario request"""
    message: str
    scenario_id: str
    startTime: str
