import { Component, OnInit } from '@angular/core';

import { RoadmapService } from './roadmap.service';

@Component({
	selector: 'roadmap',
	templateUrl: 'app/roadmap/roadmap.component.html',
	providers: [RoadmapService]
})

export class RoadmapComponent implements OnInit {
	candidates: any[] = [];
	plan: any[] = [];
	planByControlId: { [controlId: string]: any } = {};
	// Computed once whenever `plan` loads, not from the template (calling a
	// function from *ngFor re-runs it — and rebuilds the DOM it feeds — on
	// every change-detection cycle, which free-runs forever).
	groupedPlan: { quarter: string, entries: any[] }[] = [];

	quarterByControlId: { [controlId: string]: string } = {};
	rationaleByControlId: { [controlId: string]: string } = {};

	constructor(private roadmapService: RoadmapService) {
	};

	ngOnInit() {
		this.load();
	};

	load() {
		this.roadmapService.getCandidates().subscribe(candidates => this.candidates = candidates);
		this.roadmapService.getPlan().subscribe(plan => {
			this.plan = plan;
			this.planByControlId = {};
			plan.forEach(entry => this.planByControlId[entry.controlId] = entry);
			this.groupedPlan = this.groupByQuarter(plan);
		});
	};

	addToPlan(candidate) {
		const quarter = this.quarterByControlId[candidate.controlId];
		if (!quarter) {
			return;
		}
		this.roadmapService.addToPlan({
			controlId: candidate.controlId,
			quarter: quarter,
			rationale: this.rationaleByControlId[candidate.controlId] ||
				('Ranked by ROI ' + candidate.roi.toFixed(1) + ' across ' + candidate.addressedRiskCount + ' risk(s).'),
			status: 'planned'
		}).subscribe(() => this.load());
	};

	updateStatus(entry, status: string) {
		this.roadmapService.updatePlanEntry(entry._id, { status: status }).subscribe(() => this.load());
	};

	removeFromPlan(entry) {
		this.roadmapService.deletePlanEntry(entry._id).subscribe(() => this.load());
	};

	private groupByQuarter(plan: any[]) {
		const groups: { [quarter: string]: any[] } = {};
		plan.forEach(entry => {
			if (!groups[entry.quarter]) {
				groups[entry.quarter] = [];
			}
			groups[entry.quarter].push(entry);
		});
		return Object.keys(groups).sort().map(quarter => ({ quarter: quarter, entries: groups[quarter] }));
	};
}
