import { Component, OnInit } from '@angular/core';

import { AttackReferenceService } from './attack-reference.service';

@Component({
	selector: 'attack-coverage',
	templateUrl: 'app/attack-coverage/attack-coverage.component.html',
	providers: [AttackReferenceService]
})

export class AttackCoverageComponent implements OnInit {
	matrix: string = 'enterprise';
	tactics: any[] = [];
	coverage: any[] = [];
	selectedTechnique: any = null;

	constructor(private attackReferenceService: AttackReferenceService) {
	};

	ngOnInit() {
		this.load();
	};

	setMatrix(matrix: string) {
		this.matrix = matrix;
		this.selectedTechnique = null;
		this.load();
	};

	load() {
		this.attackReferenceService.getReferenceData(this.matrix).subscribe(data => {
			this.tactics = data.tactics;
		});
		this.attackReferenceService.getCoverage(this.matrix).subscribe(coverage => {
			this.coverage = coverage;
		});
	};

	techniquesForTactic(tacticId: string) {
		return this.coverage.filter(technique => technique.tacticIds.indexOf(tacticId) !== -1);
	};

	cellClass(technique) {
		if (technique.controlCount === 0) {
			return 'coverage-cell coverage-gap';
		}
		if (technique.implementedControlCount === 0) {
			return 'coverage-cell coverage-partial';
		}
		return 'coverage-cell coverage-covered';
	};

	selectTechnique(technique) {
		this.selectedTechnique = technique;
	};
}
