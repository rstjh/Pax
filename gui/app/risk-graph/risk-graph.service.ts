import { Http, Response, Request, Headers, RequestOptions, RequestMethod, URLSearchParams } from "@angular/http";
import { Injectable, OnInit } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class RiskGraphService implements OnInit {
  C2REST:string = "";

  constructor(private http: Http) {
	};

  getC2REST() {
    var requestoptions = new RequestOptions({
      method: RequestMethod.Get,
      url: 'application/environment/c2/'
    });

    return this.http.request(new Request(requestoptions))
    .map(res => res.json());
  };

  // Check on C2 status
  getC2Status() {
    var requestoptions = new RequestOptions({
			method: RequestMethod.Get,
			url: 'application/status/C2/'
		});
		return this.http.request(new Request(requestoptions))
		.map(res => res.json());
  };

  getMissionTimeAssessment(systemId, missionTaskData) {
    var headers = new Headers();
		headers.append("Content-Type", 'application/json');

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: 'application/system/mission_time/' + systemId + '/',
      headers: headers,
      body: JSON.stringify(missionTaskData)
		});

		return this.http.request(new Request(requestoptions))
		.map(res => res.json());
  };

  getEstimatedTime(systemId, task) {
    var headers = new Headers();
		headers.append("Content-Type", 'application/json');

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: '/application/actions/estimated_time/' + systemId + '/',
      headers: headers,
      body: JSON.stringify(task)
		});

		return this.http.request(new Request(requestoptions))
		.map(res => res.json());
  };

  // GET Unit list
  getMissionUnits() {
    var requestoptions = new RequestOptions({
      method: RequestMethod.Get,
      url: this.C2REST + 'entity/Unit'
    });

    return this.http.request(new Request(requestoptions))
    .map(res => res.json());
  };

  // GET Mission data
  getMissionData(missionId) {
    var requestoptions = new RequestOptions({
      method: RequestMethod.Get,
      url: this.C2REST + 'missions/' + missionId
    });

    return this.http.request(new Request(requestoptions))
    .map(res => res.json());
  };

  // POST Task
  postTask(missionId, coaId, task) {
    var headers = new Headers();
		headers.append("Content-Type", 'application/json');

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: this.C2REST + 'coa/mission/' + missionId + '/coa/' + coaId + '/task',
      headers: headers,
      body: JSON.stringify(task)
		});

    return this.http.request(new Request(requestoptions))
		.map((res: Response) => {
			if (res) {
				return {
          status: res.status
				};
			};
		});
  };

  // DELETE Task
  deleteTask(missionId, coaId, taskId) {
    var requestoptions = new RequestOptions({
      method: RequestMethod.Delete,
      url: this.C2REST + 'coa/mission/' + missionId + '/coa/' + coaId + '/task/' + taskId
    });

    return this.http.request(new Request(requestoptions))
    .map((res: Response) => {
			if (res) {
				return {
          status: res.status
				};
			};
		});
  };

  // Create new COA
  postCOA(missionId, name) {
    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: this.C2REST + 'coa/mission/' + missionId + '/coa/' + name
		});
    return this.http.request(new Request(requestoptions))
		.map((res: Response) => {
			if (res) {
				return {status: res.status};
			};
		});
  };

  // DELETE COA
  deleteCOA(missionId, coaId) {
    var requestoptions = new RequestOptions({
      method: RequestMethod.Delete,
      url: this.C2REST + 'coa/mission/' + missionId + '/coa/' + coaId
    });

    return this.http.request(new Request(requestoptions))
    .map((res: Response) => {
      if (res) {
        return {status: res.status}
			};
		});
  };

  postSystemRiskAnalysis(systemId) {
    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: 'application/risk_analysis/system/' + systemId + '/'
		});

		return this.http.request(new Request(requestoptions))
		.map(res => res.json());
  };

  postNewSystem(systemId, taskList) {
    var headers = new Headers();
		headers.append("Content-Type", 'application/json');

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: 'application/system/task_update/' + systemId + '/',
      headers: headers,
      body: JSON.stringify(taskList)
		});

		return this.http.request(new Request(requestoptions))
		.map(res => res.json());
  };

  postEffects(systemId, effectList) {
    var headers = new Headers();
		headers.append("Content-Type", 'application/json');

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: 'application/risk_analysis/task_dependency/' + systemId + '/',
      headers: headers,
      body: JSON.stringify(effectList)
		});

		return this.http.request(new Request(requestoptions))
		.map(res => res.json());
  };

  compareCOAs(systemId, coAs) {
    var headers = new Headers();
		headers.append("Content-Type", 'application/json');

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: 'application/risk_analysis/compare_system/' + systemId + '/',
      headers: headers,
      body: JSON.stringify(coAs)
		});

		return this.http.request(new Request(requestoptions))
		.map(res => res.json());
  };

  // GET System data
  getSystemData(systemId) {
    var requestoptions = new RequestOptions({
      method: RequestMethod.Get,
      url: this.C2REST + 'system/' + systemId
    });

    return this.http.request(new Request(requestoptions))
    .map(res => res.json());
  };

  // GET All missions
  getAllMissions() {
    var requestoptions = new RequestOptions({
      method: RequestMethod.Get,
      url: this.C2REST + 'missions'
    });

    return this.http.request(new Request(requestoptions))
    .map(res => res.json());
  };
};