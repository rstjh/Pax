import { Component, OnInit } from '@angular/core';

import { CapabilitiesService } from '../capabilities/capabilities.service';
import { ITAssetsService } from '../it-assets/it-assets.service';
import { RisksService } from '../risks/risks.service';

@Component({
	selector: 'assessment-wizard',
	templateUrl: 'app/assessment-wizard/assessment-wizard.component.html',
	providers: [CapabilitiesService, ITAssetsService, RisksService]
})

export class AssessmentWizardComponent implements OnInit {
	step: number = 1;

	capabilities: any[] = [];
	selectedCapabilityRefCode: string = null;

	supportingAssets: any[] = [];
	risksByAssetId: { [assetId: string]: any[] } = {};
	draftByAssetId: { [assetId: string]: any } = {};

	rollup: any = null;

	constructor(
		private capabilitiesService: CapabilitiesService,
		private assetsService: ITAssetsService,
		private risksService: RisksService) {
	};

	ngOnInit() {
		this.capabilitiesService.getCapabilities().subscribe(capabilities => this.capabilities = capabilities);
	};

	startAssessment() {
		if (!this.selectedCapabilityRefCode) {
			return;
		}
		this.assetsService.getAssets().subscribe(assets => {
			this.supportingAssets = assets.filter(
				asset => (asset.capabilityIds || []).indexOf(this.selectedCapabilityRefCode) !== -1);
			this.risksService.getRisks().subscribe(risks => {
				this.supportingAssets.forEach(asset => {
					this.risksByAssetId[asset._id] = risks.filter(
						risk => (risk.assetIds || []).indexOf(asset._id) !== -1);
					this.draftByAssetId[asset._id] = { title: '', lef: null, lm: null };
				});
				this.step = 2;
			});
		});
	};

	addRiskForAsset(asset) {
		const draft = this.draftByAssetId[asset._id];
		if (!draft.title || draft.lef == null || draft.lm == null) {
			return;
		}
		this.risksService.createRisk({
			title: draft.title,
			assetIds: [asset._id],
			lef: draft.lef,
			lm: draft.lm,
			status: 'open'
		}).subscribe(() => {
			this.risksService.getRisks().subscribe(risks => {
				this.risksByAssetId[asset._id] = risks.filter(
					risk => (risk.assetIds || []).indexOf(asset._id) !== -1);
				this.draftByAssetId[asset._id] = { title: '', lef: null, lm: null };
			});
		});
	};

	finishAssessment() {
		this.capabilitiesService.getRiskRollup(this.selectedCapabilityRefCode).subscribe(rollup => {
			this.rollup = rollup;
			this.step = 3;
		});
	};

	restart() {
		this.step = 1;
		this.selectedCapabilityRefCode = null;
		this.supportingAssets = [];
		this.rollup = null;
	};
}
