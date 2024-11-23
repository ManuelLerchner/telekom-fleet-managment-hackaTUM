import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatToolbar} from "@angular/material/toolbar";
import {MatAnchor, MatFabButton} from '@angular/material/button';
import {RouterLink, RouterLinkActive} from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, MatToolbar, MatAnchor, RouterLink, RouterLinkActive, MatFabButton, MatIconModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {

}
