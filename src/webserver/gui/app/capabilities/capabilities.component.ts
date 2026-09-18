import { Component, OnInit } from '@angular/core';

import { CapabilitiesService } from './capabilities.service';

@Component({
	selector: 'capabilities',
	templateUrl: 'app/capabilities/capabilities.component.html',
	providers: [CapabilitiesService]
})

export class CapabilitiesComponent implements OnInit {
	capabilities: any[] = [];
	rollups: { [refCode: string]: any } = {};

	newCapability: any = this.blankCapability();
	editingId: string = null;
	editCapability: any = {};

	importFile: File = null;
	importMessage: string = '';

	constructor(private capabilitiesService: CapabilitiesService) {
	};

	ngOnInit() {
		this.loadCapabilities();
	};

	loadCapabilities() {
		this.capabilitiesService.getCapabilities().subscribe(capabilities => {
			this.capabilities = capabilities;
			capabilities.forEach(capability => this.loadRollup(capability.refCode));
		});
	};

	loadRollup(refCode: string) {
		this.capabilitiesService.getRiskRollup(refCode).subscribe(rollup => {
			this.rollups[refCode] = rollup;
		});
	};

	blankCapability() {
		return { refCode: '', level: 1, name: '', description: '', parentRefCode: '', order: 0 };
	};

	indent(level: number) {
		return (level - 1) * 24;
	};

	createCapability() {
		if (!this.newCapability.refCode || !this.newCapability.name) {
			return;
		}
		const payload = Object.assign({}, this.newCapability);
		if (!payload.parentRefCode) {
			delete payload.parentRefCode;
		}
		this.capabilitiesService.createCapability(payload).subscribe(() => {
			this.newCapability = this.blankCapability();
			this.loadCapabilities();
		});
	};

	startEdit(capability) {
		this.editingId = capability._id;
		this.editCapability = Object.assign({}, capability);
	};

	cancelEdit() {
		this.editingId = null;
	};

	saveEdit() {
		this.capabilitiesService.updateCapability(this.editingId, this.editCapability).subscribe(() => {
			this.editingId = null;
			this.loadCapabilities();
		});
	};

	deleteCapability(capability) {
		if (!confirm('Delete capability "' + capability.name + '"? This does not delete its children.')) {
			return;
		}
		this.capabilitiesService.deleteCapability(capability._id).subscribe(() => {
			this.loadCapabilities();
		});
	};

	onFileSelected(event) {
		this.importFile = event.target.files.length ? event.target.files[0] : null;
	};

	importDocument() {
		if (!this.importFile) {
			return;
		}
		this.importMessage = 'Importing...';
		this.capabilitiesService.importCapabilities(this.importFile).subscribe(
			result => {
				this.importMessage = 'Imported ' + result.imported + ' capabilities.';
				this.importFile = null;
				this.loadCapabilities();
			},
			() => {
				this.importMessage = 'Import failed — check the file uses Heading 1-4 styles with numbered text.';
			});
	};
}
