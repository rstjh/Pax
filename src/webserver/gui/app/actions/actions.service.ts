import { HttpClient } from "@angular/common/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';

@Injectable()
export class ActionsService  {
  api:string = environment.API_BASE_URL + "/api/v" + environment.API_VERSION;

  constructor(private http: HttpClient) {
  };

  deleteEffect(effect) {
    return this.http.delete<any>(environment.API_BASE_URL + '/application/hostile_response/' + effect + '/', {
      observe: 'response'
    }).pipe(map((res) => {
      if (res) {
        return {
          status: res.status
        }
      }
    }));
  };

  getHostileResponses(effect) {
    return this.http.get<any>(environment.API_BASE_URL + '/application/hostile_response/' + effect);
  };

  patchHostileResponse(effect, hostileResponse) {
    return this.http.patch<any>(environment.API_BASE_URL + '/application/hostile_response/' + effect + '/', JSON.stringify(hostileResponse), {
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

  submitNewEffect(data) {
    return this.http.post<any>(environment.API_BASE_URL + '/application/hostile_response/', JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' },
      observe: 'response'
    }).pipe(map((res) => {
      if (res) {
        return { status: res.status }
      }
    }));
  };

  getEffects() {
    return this.http.get<any>(this.api + '/effects/');
  };

  getEffectTypes() {
    return this.http.get<any>('app/actions/data/effect.types.json');
  };

  getActionData(force="hostile") {
    return this.http.get<any>(this.api + '/action_list/all/' + force);
  };

  patchActionData(actions, force, effect, type) {
    return this.http.patch<any>(this.api + '/action_list/type/' + force + '/' + effect + '/' + type + '/', JSON.stringify(actions), {
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
}
