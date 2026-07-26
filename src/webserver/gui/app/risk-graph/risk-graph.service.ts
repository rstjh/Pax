import { HttpClient } from "@angular/common/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { map } from 'rxjs/operators';


@Injectable()
export class RiskGraphService {
  api:string = environment.API_BASE_URL + "/api/v" + environment.API_VERSION;
  // Populated by getC2REST(); base URL for the external C2 REST API.
  C2REST: string = environment.C2_REST_API;

  constructor(private http: HttpClient) {
	};

  // Config for the external C2 REST API this app integrates with.
  getC2REST() {
    return of({ c2_rest_api: environment.C2_REST_API });
  };

  getMissionTimeAssessment(systemId, missionTaskData) {
		return this.http.post<any>(this.api + '/system/mission_time/' + systemId + '/', JSON.stringify(missionTaskData), {
			headers: { 'Content-Type': 'application/json' }
		});
  };

  getEstimatedTime(systemId, task) {
		return this.http.post<any>(this.api + '/actions/estimated_time/' + systemId + '/', JSON.stringify(task), {
			headers: { 'Content-Type': 'application/json' }
		});
  };

  // GET Unit list
  getMissionUnits() {
    return this.http.get<any>(this.C2REST + 'entity/Unit');
  };

  // GET Mission data
  getAllMissions() {
    return this.http.get<any>(this.api + '/missions/');
  };

  getMissionData(missionId) {
    return this.http.get<any>(this.api + '/missions/' + missionId);
  };

  // POST Task
  postTask(missionId, coaId, task) {
    return this.http.post<any>(this.C2REST + 'coa/mission/' + missionId + '/coa/' + coaId + '/task', JSON.stringify(task), {
			headers: { 'Content-Type': 'application/json' },
			observe: 'response'
		}).pipe(map((res) => {
			if (res) {
				return {
          status: res.status
				};
			};
		}));
  };

  // DELETE Task
  deleteTask(missionId, coaId, taskId) {
    return this.http.delete<any>(this.C2REST + 'coa/mission/' + missionId + '/coa/' + coaId + '/task/' + taskId, {
      observe: 'response'
    }).pipe(map((res) => {
			if (res) {
				return {
          status: res.status
				};
			};
		}));
  };

  // Create new COA
  postCOA(missionId, name) {
    return this.http.post<any>(this.C2REST + 'coa/mission/' + missionId + '/coa/' + name, null, {
      observe: 'response'
    }).pipe(map((res) => {
			if (res) {
				return {status: res.status};
			};
		}));
  };

  // DELETE COA
  deleteCOA(missionId, coaId) {
    return this.http.delete<any>(this.C2REST + 'coa/mission/' + missionId + '/coa/' + coaId, {
      observe: 'response'
    }).pipe(map((res) => {
      if (res) {
        return {status: res.status}
			};
		}));
  };

  postSystemRiskAnalysis(systemId) {
		return this.http.post<any>(this.api + '/risk_analysis/system/' + systemId + '/', null);
  };

  postNewSystem(systemId, taskList) {
		return this.http.post<any>(environment.API_BASE_URL + '/application/system/task_update/' + systemId + '/', JSON.stringify(taskList), {
			headers: { 'Content-Type': 'application/json' }
		});
  };

  postEffects(systemId, effectList) {
		return this.http.post<any>(this.api + '/risk_analysis/task_dependency/' + systemId + '/', JSON.stringify(effectList), {
			headers: { 'Content-Type': 'application/json' }
		});
  };

  compareCOAs(systemId, coAs) {
		return this.http.post<any>(this.api + '/risk_analysis/compare_system/' + systemId + '/', JSON.stringify(coAs), {
			headers: { 'Content-Type': 'application/json' }
		});
  };

  // GET System data
  getSystemData(systemId) {
    return this.http.get<any>(this.api + '/cvi/' + systemId);
  };

  // GET all currently staged actions
  getStagedActions() {
    return this.http.get<any>(this.api + '/action_instances/');
  };

};
