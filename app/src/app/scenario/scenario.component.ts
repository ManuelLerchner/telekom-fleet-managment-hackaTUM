import { Component, inject, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatToolbar } from '@angular/material/toolbar';
import { MatCardModule, MatCardContent, MatCardHeader } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MapComponent } from '../map/map.component';
import { MatList, MatListItem } from '@angular/material/list';
import { MatChip } from '@angular/material/chips';
import { Clipboard } from '@angular/cdk/clipboard';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatFormField } from '@angular/material/form-field';
import { MatInput } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatBadge} from '@angular/material/badge';

@Component({
  selector: 'app-scenario',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    FormsModule,
    MatCardContent,
    MatFormFieldModule,
    MatCardHeader,
    MatTableModule,
    MatToolbar,
    MatButtonModule,
    MatDividerModule,
    MatIconModule,
    MapComponent,
    MatList,
    MatListItem,
    MatChip,
    MatFormField,
    MatInput,
    MatBadge
  ],
  templateUrl: './scenario.component.html',
  styleUrls: ['./scenario.component.scss']
})
export class ScenarioComponent implements OnInit {
  scenarios: any[] = [];
  private _snackBar = inject(MatSnackBar);
  displayedColumns: string[] = ['id', 'vehicles', 'customers', 'actions'];
  selectedScenario: any = null;
  showVehicles = false;
  showCustomers = false;
  numberOfVehicles: number | null = null;
  numberOfCustomers: number | null = null;

  constructor(private http: HttpClient, private clipboard: Clipboard) {}

  toggleVehicles() {
    this.showVehicles = !this.showVehicles;
  }

  toggleCustomers() {
    this.showCustomers = !this.showCustomers;
  }

  ngOnInit(): void {
    this.getScenarios();
  }

  getScenarios(): void {
    this.http.get('http://localhost:8080/scenarios').subscribe((data: any) => {
      this.scenarios = data;
    });
  }

  createScenario(): void {
    if (this.numberOfVehicles !== null && (this.numberOfVehicles < 1 || this.numberOfVehicles > 50)) {
      this._snackBar.open('Number of Vehicles must be between 1 and 50', 'close', { duration: 2000 });
      return;
    }
    if (this.numberOfCustomers !== null && (this.numberOfCustomers < 1 || this.numberOfCustomers > 200)) {
      this._snackBar.open('Number of Customers must be between 1 and 200', 'close', { duration: 2000 });
      return;
    }


    const params = {
       numberOfVehicles: this.numberOfVehicles ?? '',
       numberOfCustomers: this.numberOfCustomers ?? ''
    };

    this.http.post('http://localhost:8080/scenario/create', null, { params }).subscribe(() => {
      this.getScenarios();
    });
  }

  deleteScenarioById(scenarioId: string): void {
    this.http.delete(`http://localhost:8080/scenarios/${scenarioId}`).subscribe(() => {
      this.getScenarios();
    });
  }

  showDetails(scenario: any): void {
    this.selectedScenario = scenario;
  }

  copyIdToClipboard(id: string): void {
    this.clipboard.copy(id);
    this._snackBar.open('Scenario ID copied to clipboard', 'close', {duration: 2000});
  }
}
