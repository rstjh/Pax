import { Component, OnInit } from '@angular/core';

import { ITAssetsService } from './it-assets.service';
import { CapabilitiesService } from '../capabilities/capabilities.service';

@Component({
	selector: 'it-assets',
	templateUrl: 'app/it-assets/it-assets.component.html',
	providers: [ITAssetsService, CapabilitiesService]
})

export class ITAssetsComponent implements OnInit {
	assets: any[] = [];
	capabilities: any[] = [];
	criticalityOptions = ['Low', 'Medium', 'High', 'Critical'];

	newAsset: any = this.blankAsset();
	editingId: string = null;
	editAsset: any = {};

	constructor(
		private assetsService: ITAssetsService,
		private capabilitiesService: CapabilitiesService) {
	};

	ngOnInit() {
		this.loadAssets();
		this.capabilitiesService.getCapabilities().subscribe(capabilities => {
			this.capabilities = capabilities;
		});
	};

	loadAssets() {
		this.assetsService.getAssets().subscribe(assets => {
			this.assets = assets;
		});
	};

	blankAsset() {
		return { name: '', description: '', owner: '', criticality: 'Medium', domain: 'IT', capabilityIds: [] };
	};

	capabilityName(refCode: string) {
		const capability = this.capabilities.find(c => c.refCode === refCode);
		return capability ? capability.refCode + ' ' + capability.name : refCode;
	};

	createAsset() {
		if (!this.newAsset.name) {
			return;
		}
		this.assetsService.createAsset(this.newAsset).subscribe(() => {
			this.newAsset = this.blankAsset();
			this.loadAssets();
		});
	};

	startEdit(asset) {
		this.editingId = asset._id;
		this.editAsset = Object.assign({}, asset);
	};

	cancelEdit() {
		this.editingId = null;
	};

	saveEdit() {
		this.assetsService.updateAsset(this.editingId, this.editAsset).subscribe(() => {
			this.editingId = null;
			this.loadAssets();
		});
	};

	deleteAsset(asset) {
		if (!confirm('Delete asset "' + asset.name + '"?')) {
			return;
		}
		this.assetsService.deleteAsset(asset._id).subscribe(() => {
			this.loadAssets();
		});
	};
}
