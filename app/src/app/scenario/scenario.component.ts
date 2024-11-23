import { Component, inject, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { MatTableModule } from "@angular/material/table";
import { MatToolbar } from "@angular/material/toolbar";
import {
  MatCardModule,
  MatCardContent,
  MatCardHeader,
} from "@angular/material/card";
import { MatButtonModule } from "@angular/material/button";
import { MatDividerModule } from "@angular/material/divider";
import { MatIconModule } from "@angular/material/icon";
import { MapComponent } from "../map/map.component";
import { MatList, MatListItem } from "@angular/material/list";
import { MatChip } from "@angular/material/chips";
import { Clipboard } from "@angular/cdk/clipboard";
import { MatSnackBar } from "@angular/material/snack-bar";
import { MatFormField } from "@angular/material/form-field";
import { MatInput } from "@angular/material/input";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatBadge } from "@angular/material/badge";

@Component({
  selector: "app-scenario",
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
    MatBadge,
  ],
  templateUrl: "./scenario.component.html",
  styleUrls: ["./scenario.component.scss"],
})
export class ScenarioComponent implements OnInit {
  private _snackBar = inject(MatSnackBar);
  displayedColumns: string[] = ["id", "vehicles", "customers", "actions"];
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
    // this.http.post('http://localhost:8090/Scenarios/initialize_scenario?db_scenario_id=ae7f7c78-2fa6-438f-882f-25e17c514ed8', '{}')

    // Set Interval to get Scenario perdiocially
    window.setInterval(async () => {
      this.getScenario();
    }, 1000);
  }

  getScenario(): void {
    console.log("REQUEST SCENARIO");
    this.http
      .get(
        "http://localhost:1111/Scenarios/get_scenario/d9deaa85-7eed-493b-9b37-d20155da3f7d"
      )
      .subscribe((data: any) => {
        console.log("SCENARIO", data);
        this.selectedScenario = data;
      });
  }
}
