import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

@Injectable()
export class ITAssetsService {
	api: string = environment.API_BASE_URL + '/api/v' + environment.API_VERSION;

	constructor(private http: HttpClient) {
	};

	getAssets() {
		return this.http.get<any[]>(this.api + '/it_assets/');
	};

	createAsset(asset) {
		return this.http.post<any>(this.api + '/it_assets/', asset);
	};

	updateAsset(id, asset) {
		return this.http.patch<any>(this.api + '/it_assets/?_id=' + id, asset);
	};

	deleteAsset(id) {
		return this.http.delete<any>(this.api + '/it_assets/?_id=' + id);
	};
}
