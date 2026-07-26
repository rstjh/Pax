import { HttpClient } from "@angular/common/http";
import { environment } from '../../../environment/environment';
import { Injectable } from '@angular/core';


@Injectable()
export class ActionModalService  {
  api:string = environment.API_BASE_URL + "/api/v" + environment.API_VERSION;

  constructor(private http: HttpClient) {
	};

  postEffects(systemId, task) {
		return this.http.post<any>(this.api + '/risk_analysis/task_dependency/' + systemId + '/', JSON.stringify(task), {
			headers: { 'Content-Type': 'application/json' }
		});
  };


  getTaskActions(force, effect, actionType) {
		return this.http.get<any>(this.api + '/action_list/type/' +
      force + '/' +
      effect.toUpperCase() + '/' +
      actionType.toLowerCase() + '/'
    );
  };

};
