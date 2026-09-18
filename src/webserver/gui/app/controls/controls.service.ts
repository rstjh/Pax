import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

@Injectable()
export class ControlsService {
	api: string = environment.API_BASE_URL + '/api/v' + environment.API_VERSION;

	constructor(private http: HttpClient) {
	};

	getControls() {
		return this.http.get<any[]>(this.api + '/controls/');
	};

	createControl(control) {
		return this.http.post<any>(this.api + '/controls/', control);
	};

	updateControl(id, control) {
		return this.http.patch<any>(this.api + '/controls/?_id=' + id, control);
	};

	deleteControl(id) {
		return this.http.delete<any>(this.api + '/controls/?_id=' + id);
	};
}
