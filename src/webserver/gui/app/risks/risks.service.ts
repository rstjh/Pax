import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

@Injectable()
export class RisksService {
	api: string = environment.API_BASE_URL + '/api/v' + environment.API_VERSION;

	constructor(private http: HttpClient) {
	};

	getRisks(overdueOnly: boolean = false) {
		const query = overdueOnly ? '?overdue=true' : '';
		return this.http.get<any[]>(this.api + '/risks/' + query);
	};

	createRisk(risk) {
		return this.http.post<any>(this.api + '/risks/', risk);
	};

	updateRisk(id, risk) {
		return this.http.patch<any>(this.api + '/risks/?_id=' + id, risk);
	};

	deleteRisk(id) {
		return this.http.delete<any>(this.api + '/risks/?_id=' + id);
	};
}
