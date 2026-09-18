import { Component, OnInit } from '@angular/core';

import { ControlsService } from './controls.service';
import { ITAssetsService } from '../it-assets/it-assets.service';
import { AttackReferenceService } from '../attack-coverage/attack-reference.service';

@Component({
	selector: 'controls',
	templateUrl: 'app/controls/controls.component.html',
	providers: [ControlsService, ITAssetsService, AttackReferenceService]
})

export class ControlsComponent implements OnInit {
	controls: any[] = [];
	assets: any[] = [];
	techniques: any[] = [];
	statusOptions = ['Planned', 'In Progress', 'Implemented', 'Retired'];

	newControl: any = this.blankControl();
	editingId: string = null;
	editControl: any = {};

	constructor(
		private controlsService: ControlsService,
		private assetsService: ITAssetsService,
		private attackReferenceService: AttackReferenceService) {
	};

	ngOnInit() {
		this.loadControls();
		this.assetsService.getAssets().subscribe(assets => this.assets = assets);
		this.attackReferenceService.getReferenceData().subscribe(data => this.techniques = data.techniques);
	};

	loadControls() {
		this.controlsService.getControls().subscribe(controls => this.controls = controls);
	};

	blankControl() {
		return { name: '', description: '', owner: '', status: 'Planned', assetIds: [], attackTechniqueIds: [], cost: 0, effectiveness: 0.5 };
	};

	assetName(assetId: string) {
		const asset = this.assets.find(a => a._id === assetId);
		return asset ? asset.name : assetId;
	};

	techniqueName(techniqueId: string) {
		const technique = this.techniques.find(t => t.id === techniqueId);
		return technique ? technique.id + ' ' + technique.name : techniqueId;
	};

	createControl() {
		if (!this.newControl.name) {
			return;
		}
		this.controlsService.createControl(this.newControl).subscribe(() => {
			this.newControl = this.blankControl();
			this.loadControls();
		});
	};

	startEdit(control) {
		this.editingId = control._id;
		this.editControl = Object.assign({}, control);
	};

	cancelEdit() {
		this.editingId = null;
	};

	saveEdit() {
		this.controlsService.updateControl(this.editingId, this.editControl).subscribe(() => {
			this.editingId = null;
			this.loadControls();
		});
	};

	deleteControl(control) {
		if (!confirm('Delete control "' + control.name + '"?')) {
			return;
		}
		this.controlsService.deleteControl(control._id).subscribe(() => {
			this.loadControls();
		});
	};
}
