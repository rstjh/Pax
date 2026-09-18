import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

@Injectable()
export class CapabilitiesService {
	api: string = environment.API_BASE_URL + '/api/v' + environment.API_VERSION;

	constructor(private http: HttpClient) {
	};

	getCapabilities() {
		return this.http.get<any[]>(this.api + '/capabilities/');
	};

	createCapability(capability) {
		return this.http.post<any>(this.api + '/capabilities/', capability);
	};

	updateCapability(id, capability) {
		return this.http.patch<any>(this.api + '/capabilities/?_id=' + id, capability);
	};

	deleteCapability(id) {
		return this.http.delete<any>(this.api + '/capabilities/?_id=' + id);
	};

	importCapabilities(file: File) {
		const formData = new FormData();
		formData.append('file', file);
		return this.http.post<any>(this.api + '/capabilities/import/', formData);
	};

	getRiskRollup(refCode: string) {
		return this.http.get<any>(this.api + '/capabilities/' + encodeURIComponent(refCode) + '/risk_rollup/');
	};
}
