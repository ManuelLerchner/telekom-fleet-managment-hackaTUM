import {Component, AfterViewInit, Inject, PLATFORM_ID, Input, OnChanges, SimpleChanges} from '@angular/core';
import {isPlatformBrowser} from '@angular/common';
import {Vehicle} from '../models/vehicle.model';
import {Customer} from '../models/customer.model';

@Component({
  selector: 'app-map', templateUrl: './map.component.html', styleUrls: ['./map.component.scss'], standalone: true,
})
export class MapComponent implements AfterViewInit, OnChanges {
  @Input() vehicles: Vehicle[] = [];
  @Input() customers: Customer[] = [];
  private markers: any[] = [];
  private map: any;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {
  }

  ngAfterViewInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.renderMap();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['vehicles'] && this.map || changes['customers'] && this.map) {
      this.updateMarkers();
    }
  }

  private async renderMap(): Promise<void> {
    if (isPlatformBrowser(this.platformId)) {
      const L = await import('leaflet');
      this.map = L.map('mymap', {
        center: [48.1403, 11.5600], zoom: 13,
      });

      const streetMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 17, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      });

      streetMap.addTo(this.map);
      this.updateMarkers();
    }
  }

  private async updateMarkers(): Promise<void> {
    if (isPlatformBrowser(this.platformId)) {
      const L = await import('leaflet');
      // Clear existing markers
      this.markers.forEach(marker => this.map.removeLayer(marker));
      this.markers = [];

      const vehicleIcon = L.icon({
        iconUrl: 'vehiclemarker.png', // Replace with the path to your custom icon
        iconSize: [25, 41], // Size of the icon
        iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
        popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
      });

      // Add new markers with custom icon
      this.vehicles.forEach(vehicle => {
        const marker = L.marker([vehicle.coordX, vehicle.coordY], {icon: vehicleIcon})
          .addTo(this.map)
          .bindPopup(`Vehicle ID: ${vehicle.id}`)
        this.markers.push(marker);
      });

      const customerIcon = L.icon({
        iconUrl: 'customermarker.png', // Replace with the path to your custom icon
        iconSize: [25, 41], // Size of the icon
        iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
        popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
      });

      this.customers.forEach(customer => {
        const customerMarker = L.marker([customer.coordX, customer.coordY], {icon: customerIcon})
          .addTo(this.map)
          .bindPopup(`Customer ID: ${customer.id}`)
        this.markers.push(customerMarker);

        const destinationIcon = L.icon({
          iconUrl: 'destinationmarker.png', // Replace with the path to your custom icon
          iconSize: [25, 41], // Size of the icon
          iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
          popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
        });

        const destinationMarker = L.marker([customer.destinationX, customer.destinationY], {icon: destinationIcon})
          .addTo(this.map)
          .bindPopup(`Destination for Customer ID: ${customer.id}`)
        this.markers.push(destinationMarker);

        // Draw route between customer and destination
        const route = L.polyline([[customer.coordX, customer.coordY], [customer.destinationX, customer.destinationY]], {
          color: 'blue',
          weight: 1,
          dashArray: '5, 10'
        })
          .addTo(this.map);
        this.markers.push(route);
      });
    }
  }
}
