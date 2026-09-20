import { Component, OnInit } from '@angular/core';

import { RisksService } from '../risks/risks.service';

@Component({
	selector: 'risk-register',
	templateUrl: 'app/risk-register/risk-register.component.html',
	providers: [RisksService]
})

export class RiskRegisterComponent implements OnInit {
	risks: any[] = [];
	statusOptions = ['open', 'in_progress', 'closed'];
	treatmentOptions = ['mitigate', 'accept', 'transfer', 'avoid'];

	statusFilter: string = '';
	ownerFilter: string = '';
	sortField: string = 'residualAle';
	sortDescending: boolean = true;

	editingId: string = null;
	editRisk: any = {};

	today: string = new Date().toISOString().slice(0, 10);

	constructor(private risksService: RisksService) {
	};

	ngOnInit() {
		this.load();
	};

	load() {
		this.risksService.getRisks().subscribe(risks => this.risks = risks);
	};

	isOverdue(risk) {
		return risk.status !== 'closed' && risk.reviewDate && risk.reviewDate < this.today;
	};

	setSort(field: string) {
		if (this.sortField === field) {
			this.sortDescending = !this.sortDescending;
		} else {
			this.sortField = field;
			this.sortDescending = true;
		}
	};

	filteredSortedRisks() {
		let filtered = this.risks.filter(risk =>
			(!this.statusFilter || risk.status === this.statusFilter) &&
			(!this.ownerFilter || (risk.owner || '').toLowerCase().indexOf(this.ownerFilter.toLowerCase()) !== -1));

		const field = this.sortField;
		const direction = this.sortDescending ? -1 : 1;
		filtered = filtered.sort((a, b) => {
			const left = a[field] || '';
			const right = b[field] || '';
			if (left < right) { return -1 * direction; }
			if (left > right) { return 1 * direction; }
			return 0;
		});
		return filtered;
	};

	startEdit(risk) {
		this.editingId = risk._id;
		this.editRisk = Object.assign({}, risk);
	};

	cancelEdit() {
		this.editingId = null;
	};

	saveEdit() {
		const lifecycleUpdate = {
			owner: this.editRisk.owner,
			treatment: this.editRisk.treatment,
			status: this.editRisk.status,
			reviewDate: this.editRisk.reviewDate
		};
		this.risksService.updateRisk(this.editingId, lifecycleUpdate).subscribe(() => {
			this.editingId = null;
			this.load();
		});
	};

	deleteRisk(risk) {
		if (!confirm('Delete risk "' + risk.title + '"?')) {
			return;
		}
		this.risksService.deleteRisk(risk._id).subscribe(() => {
			this.load();
		});
	};
}
