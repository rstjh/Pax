import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

@Injectable()
export class RoadmapService {
	api: string = environment.API_BASE_URL + '/api/v' + environment.API_VERSION;

	constructor(private http: HttpClient) {
	};

	getCandidates() {
		return this.http.get<any[]>(this.api + '/roadmap/candidates/');
	};

	getPlan() {
		return this.http.get<any[]>(this.api + '/roadmap/');
	};

	addToPlan(entry) {
		return this.http.post<any>(this.api + '/roadmap/', entry);
	};

	updatePlanEntry(id, entry) {
		return this.http.patch<any>(this.api + '/roadmap/?_id=' + id, entry);
	};

	deletePlanEntry(id) {
		return this.http.delete<any>(this.api + '/roadmap/?_id=' + id);
	};
}
