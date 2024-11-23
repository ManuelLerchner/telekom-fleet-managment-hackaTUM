import { Component } from '@angular/core';
import {MatCard, MatCardContent, MatCardTitle} from '@angular/material/card';
import {MatList, MatListItem} from '@angular/material/list';
import {MatAccordion, MatExpansionPanel, MatExpansionPanelHeader, MatExpansionPanelTitle} from '@angular/material/expansion';
import {RouterLink} from '@angular/router';
import {MatButton, MatFabButton} from '@angular/material/button';

@Component({
  selector: 'app-landing-page',
  standalone: true,
  imports: [
    MatCard,
    MatCardTitle,
    MatCardContent,
    MatList,
    MatListItem,
    MatExpansionPanel,
    MatExpansionPanelTitle,
    MatExpansionPanelHeader,
    MatAccordion,
    RouterLink,
    MatButton,
    MatFabButton
  ],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.scss'
})
export class LandingPageComponent {
  openLink(url: string) {
    window.open(url, '_blank');
  }
}
