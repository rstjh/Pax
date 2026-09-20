import { Component, OnInit } from '@angular/core';

import { RisksService } from '../risks/risks.service';
import { AttackReferenceService } from '../attack-coverage/attack-reference.service';
import { RoadmapService } from '../roadmap/roadmap.service';
import { ControlsService } from '../controls/controls.service';

@Component({
	selector: 'dashboard',
	templateUrl: 'app/dashboard/dashboard.component.html',
	providers: [RisksService, AttackReferenceService, RoadmapService, ControlsService]
})

export class DashboardComponent implements OnInit {
	totalResidualAle: number = 0;
	riskCounts: any = { open: 0, in_progress: 0, closed: 0 };
	overdueCount: number = 0;

	topGaps: any[] = [];

	planCounts: any = { planned: 0, in_progress: 0, done: 0 };

	constructor(
		private risksService: RisksService,
		private attackReferenceService: AttackReferenceService,
		private roadmapService: RoadmapService,
		private controlsService: ControlsService) {
	};

	ngOnInit() {
		this.risksService.getRisks().subscribe(risks => {
			this.riskCounts = { open: 0, in_progress: 0, closed: 0 };
			this.totalResidualAle = 0;
			risks.forEach(risk => {
				this.riskCounts[risk.status] = (this.riskCounts[risk.status] || 0) + 1;
				if (risk.status !== 'closed') {
					this.totalResidualAle += (risk.residualAle || 0);
				}
			});
		});

		this.risksService.getRisks(true).subscribe(overdue => {
			this.overdueCount = overdue.length;
		});

		this.attackReferenceService.getCoverage('enterprise').subscribe(coverage => {
			this.topGaps = coverage.filter(technique => technique.controlCount === 0).slice(0, 8);
		});

		this.roadmapService.getPlan().subscribe(plan => {
			this.planCounts = { planned: 0, in_progress: 0, done: 0 };
			plan.forEach(entry => this.planCounts[entry.status] = (this.planCounts[entry.status] || 0) + 1);
		});
	};
}
