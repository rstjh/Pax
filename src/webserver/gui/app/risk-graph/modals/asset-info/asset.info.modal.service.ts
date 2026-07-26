import { HttpClient, HttpParams } from "@angular/common/http";
import { environment } from '../../../environment/environment';
import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';


@Injectable()
export class AssetInfoService {
  api:string = environment.API_BASE_URL + "/api/v" + environment.API_VERSION;

  constructor(private _http: HttpClient) {
	}

  getMissionData() {
		return this._http.get<any>(environment.API_BASE_URL + '/application/missions');
  };

  getAssetVulnerabilities(systemId, assetId) {
    return this._http.get<any>(environment.API_BASE_URL + '/application/system/vulnerabilities/' + systemId + '/' + assetId + '/');
  };

  getUnitDistance(systemId, assetId, actorId) {
    return this._http.get<any>(this.api + '/geolocation/distance/' + systemId + '/' + assetId + '/' + actorId + '/');
  };

  getAssetLocation(systemId, assetId) {
    return this._http.get<any>(environment.API_BASE_URL + '/application/system/location/' + systemId + '/' + assetId + '/');
  };


  getAssetThreats(systemId, assetId) {
    return this._http.get<any>(environment.API_BASE_URL + '/application/system/threats/' + systemId + '/' + assetId + '/');
  };

  getAllEffectsBasedActions(systemId) {
    return this._http.get<any>(environment.API_BASE_URL + '/application/actions/effects/' + systemId);
  };

  getEffectsBasedActionsObjective(systemId, objectiveId) {
    let params = new HttpParams().set('objective', objectiveId);

    return this._http.get<any>(environment.API_BASE_URL + '/application/actions/effects/' + systemId, { params });
  };

  postEffectsBasedAction(systemId, effectActionData) {
    return this._http.post<any>(environment.API_BASE_URL + '/application/actions/effects/' + systemId + '/', JSON.stringify(effectActionData), {
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

  deleteEffectsBasedActions(systemId, taskIds) {
    return this._http.request<any>('DELETE', environment.API_BASE_URL + '/application/actions/effects/' + systemId + '/', {
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({'effectIds': taskIds}),
      observe: 'response'
    }).pipe(map((res) => {
			if (res) {
				return {
          status: res.status
				}
			}
		}));
  };

  // Callers use effects as names (rendered in dropdowns and set as a task's
  // `effect`), so map the stored documents down to their names.
  getEffects() {
    return this._http.get<any>(this.api + '/effects/').pipe(
      map((effects) => effects.map((e) => e['effect'] || e))
    );
  };

  getObjectives(systemId) {
		return this._http.get<any>(environment.API_BASE_URL + '/application/system/assets/' + systemId);
  };

  getUnits(systemId) {
		return this._http.get<any>(environment.API_BASE_URL + '/application/system/units/' + systemId);
  };

  getUnitsAsset(systemId, assetId) {
		return this._http.get<any>(environment.API_BASE_URL + '/application/system/unit_distance/' + systemId + '/' + assetId);
  };

  getNodeData(globalId) {
    let params = new HttpParams().set('globalId', globalId);

		return this._http.get<any>(environment.API_BASE_URL + '/application/node-data', { params });
  };

  getThreatData(assetId) {
		return this._http.get<any>(environment.API_BASE_URL + '/application/threats/asset/' + assetId);
  };

  getVulnerabilityData(assetId) {
		return this._http.get<any>(environment.API_BASE_URL + '/application/vulnerabilities/asset/' + assetId);
  };

  getDevices(assetId) {
		return this._http.get<any>(environment.API_BASE_URL + '/application/devices/asset/' + assetId);
  };

  getActions(assetId) {
		return this._http.get<any>(environment.API_BASE_URL + '/application/actions/asset/id/' + assetId);
  };

  toggleAction(actionId, newStagedStatus) {
    var data = {
      'staged': newStagedStatus
    };
    return this._http.patch<any>(environment.API_BASE_URL + '/application/actions/staged/' + actionId, JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      observe: 'response'
    }).pipe(map((res) => {
			if (res) {
        return {
          data : res.status
        }
      }
		}));
  };
}
