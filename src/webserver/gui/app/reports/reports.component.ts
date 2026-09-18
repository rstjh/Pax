import { Component, OnInit } from '@angular/core';

import { environment } from '../environment/environment';
import { RisksService } from '../risks/risks.service';
import { RoadmapService } from '../roadmap/roadmap.service';

@Component({
	selector: 'reports',
	templateUrl: 'app/reports/reports.component.html',
	providers: [RisksService, RoadmapService]
})

export class ReportsComponent implements OnInit {
	reportUrl: string = environment.API_BASE_URL + '/api/v' + environment.API_VERSION + '/reports/summary.docx';

	totalResidualAle: number = 0;
	riskCounts: any = { open: 0, in_progress: 0, closed: 0 };
	planCount: number = 0;

	constructor(private risksService: RisksService, private roadmapService: RoadmapService) {
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
		this.roadmapService.getPlan().subscribe(plan => this.planCount = plan.length);
	};
}
