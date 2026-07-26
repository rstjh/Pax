import { HttpClient } from "@angular/common/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';



@Injectable()
export class CVIService {
	section = {
    'current' : ''
  };

	constructor(private http: HttpClient) {
	};

	getCVIQuestions() {
		return this.http.get<any>('app/cvi/data/cvi.questions.json');
  };

	getCVIAnswers() {
		return this.http.get<any>('app/cvi/data/cvi.answers.json');
  };

	getSampleCVIData() {
		return this.http.get<any>('app/cvi/data/c2-api-get-system-response.json');
  };

	getCurrentSection(currentSection) {
		this.section['current'] = currentSection;
	};

	postCVIData(data) {
		return this.http.post<any>(environment.API_BASE_URL + '/application/system/', JSON.stringify(data), {
			headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
			observe: 'response'
		}).pipe(map((res) => {
			if (res) {
				return { status: res.status }
			}
		}));
	}
}
