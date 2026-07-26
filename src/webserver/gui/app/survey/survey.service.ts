import { HttpClient } from "@angular/common/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';


@Injectable()
export class SurveyService {
	riskAppetite = {
		class : "",
		completed : false,
		riskAppetiteLabel : "",
		riskAppetiteScore : 0
	};

	constructor(private _http: HttpClient) {
	}

	getSurveyQuestions() {
		return this._http.get<any>('app/survey/data/survey.questions.json');
  }

	getRiskAppetiteData(riskAppetiteData) {
		this.riskAppetite.riskAppetiteLabel = riskAppetiteData.riskAppetiteLabel;
		this.riskAppetite.riskAppetiteScore = riskAppetiteData.riskAppetiteScore;
		this.riskAppetite.completed = true;

		if (riskAppetiteData.riskAppetiteLabel == "Very High") {
			this.riskAppetite.class = "label label-danger";
		} else if (riskAppetiteData.riskAppetiteLabel == "High") {
			this.riskAppetite.class = "label label-warning";
		} else if (riskAppetiteData.riskAppetiteLabel == "Neutral") {
			this.riskAppetite.class = "label label-success";
		} else {
			this.riskAppetite.class = "label label-info";
		};
	};

	postRiskAppetiteData(data) {
		return this._http.post<any>(environment.API_BASE_URL + '/application/risk-appetite-data', JSON.stringify(data), {
			headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
			observe: 'response'
		}).pipe(map((res) => {
			if (res) {
				return {
					       status: res.status,
					       json: res.body
							 }
			}
		}));
	}
}
