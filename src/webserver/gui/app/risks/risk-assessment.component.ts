import { Component, OnInit } from '@angular/core';

import { RisksService } from './risks.service';
import { ITAssetsService } from '../it-assets/it-assets.service';
import { AttackReferenceService } from '../attack-coverage/attack-reference.service';

@Component({
	selector: 'risk-assessment',
	templateUrl: 'app/risks/risk-assessment.component.html',
	providers: [RisksService, ITAssetsService, AttackReferenceService]
})

export class RiskAssessmentComponent implements OnInit {
	risks: any[] = [];
	assets: any[] = [];
	techniques: any[] = [];

	selectedRiskId: string = 'new';
	form: any = this.blankForm();
	result: any = null;
	saving: boolean = false;

	constructor(
		private risksService: RisksService,
		private assetsService: ITAssetsService,
		private attackReferenceService: AttackReferenceService) {
	};

	ngOnInit() {
		this.risksService.getRisks().subscribe(risks => this.risks = risks);
		this.assetsService.getAssets().subscribe(assets => this.assets = assets);
		this.attackReferenceService.getReferenceData().subscribe(data => this.techniques = data.techniques);
	};

	blankForm() {
		return { title: '', description: '', owner: '', assetIds: [], attackTechniqueIds: [], lef: null, lm: null };
	};

	onSelectRisk() {
		this.result = null;
		if (this.selectedRiskId === 'new') {
			this.form = this.blankForm();
			return;
		}
		const risk = this.risks.find(r => r._id === this.selectedRiskId);
		this.form = Object.assign({}, risk);
	};

	submit() {
		if (!this.form.title || this.form.lef == null || this.form.lm == null) {
			return;
		}
		this.saving = true;
		if (this.selectedRiskId === 'new') {
			this.risksService.createRisk(this.form).subscribe(response => {
				this.saving = false;
				this.result = response;
				this.risksService.getRisks().subscribe(risks => {
					this.risks = risks;
					this.selectedRiskId = response._id;
				});
			});
		} else {
			this.risksService.updateRisk(this.selectedRiskId, this.form).subscribe(response => {
				this.saving = false;
				this.result = response;
				this.risksService.getRisks().subscribe(risks => this.risks = risks);
			});
		}
	};
}
