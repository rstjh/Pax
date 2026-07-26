import { HttpClient } from "@angular/common/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';


@Injectable()
export class HomeService  {

  constructor(private http: HttpClient) {
	};

  // CHECK DATA
  checkData(url) {
		return this.http.get<any>(url);
  };

  // GET
  getNetworkData() {
		return this.http.get<any>('app/home/data/network.data.json');
  };

  getRiskAppetiteData() {
		return this.http.get<any>('app/home/data/risk.appetite.data.json');
  };

  getThreatActions() {
		return this.http.get<any>('app/home/data/threat-data/threat.actions.data.json');
  };

  getThreatActorData(threatActor) {
    var threatDataURL = 'app/home/data/threat-data/threat-actor/' + threatActor + '.threat.data.json';

		return this.http.get<any>(threatDataURL);
  };


  // POST
  postNetworkData(networkData) {
		return this.http.post<any>(environment.API_BASE_URL + '/application/network/', JSON.stringify(networkData), {
			headers: { 'Content-Type': 'application/json' },
			observe: 'response'
		}).pipe(map((res) => {
			if (res) {
				return {
          status: res.status
				}
			}
		}));
  };

  postRiskAppetiteData(riskAppetiteData) {
		return this.http.post<any>(environment.API_BASE_URL + '/application/risk_appetite/', JSON.stringify(riskAppetiteData), {
			headers: { 'Content-Type': 'application/json' },
			observe: 'response'
		}).pipe(map((res) => {
			if (res) {
				return {
          status: res.status
				}
			}
		}));
  };

  postThreatData(threatData) {
		return this.http.post<any>(environment.API_BASE_URL + '/application/threats/', JSON.stringify(threatData), {
			headers: { 'Content-Type': 'application/json' },
			observe: 'response'
		}).pipe(map((res) => {
			if (res) {
				return {
          status: res.status
				}
			}
		}));
  };

  // DELETE
  dropData(url) {
		return this.http.delete<any>(url);
  };
}
