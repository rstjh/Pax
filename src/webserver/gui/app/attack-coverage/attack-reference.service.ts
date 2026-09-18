import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

@Injectable()
export class AttackReferenceService {
	api: string = environment.API_BASE_URL + '/api/v' + environment.API_VERSION;

	constructor(private http: HttpClient) {
	};

	getReferenceData(matrix?: string) {
		const query = matrix ? '?matrix=' + matrix : '';
		return this.http.get<any>(this.api + '/attack_reference/' + query);
	};

	getCoverage(matrix?: string) {
		const query = matrix ? '?matrix=' + matrix : '';
		return this.http.get<any[]>(this.api + '/attack_reference/coverage/' + query);
	};
}
