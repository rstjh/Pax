import * as SurveyNs from 'survey-angular';
// SystemJS wraps this CJS module's exports under SurveyNs.default rather than
// exposing them directly on the namespace object; unwrap it here.
const Survey = ((SurveyNs as any).default || SurveyNs) as typeof SurveyNs;

import { Component, OnInit, Injectable } from '@angular/core';

import { SurveyService } from './survey.service';

import 'rxjs/add/operator/map';


@Component({
  selector:'Survey',
  templateUrl: 'app/survey/survey.component.html',
  providers: [SurveyService]
})

@Injectable()
export class SurveyComponent implements OnInit  {
  riskAppetite : any;

  constructor(private surveyService: SurveyService) {
    this.riskAppetite = surveyService.riskAppetite;
  };

  ngOnInit() {
    Survey.StylesManager.applyTheme("bootstrap");
    Survey.defaultBootstrapCss.navigationButton = "btn btn-success";
    Survey.defaultBootstrapCss.matrixdynamic.button = "btn btn-default";
    Survey.defaultBootstrapCss.progressBar = "progress-bar progress-bar-success progress-bar-striped active";

    this.surveyService.getSurveyQuestions()
    .subscribe(surveyJSON => {
      var surveyJSON = surveyJSON;
      surveyJSON.showProgressBar = "bottom";

      var surveyServicePass = this.surveyService;
      var survey = new Survey.Model(surveyJSON);

      // SurveyJS invokes onComplete as (sender, options), so the service must
      // come from the closure: a second parameter with a default value would
      // be overwritten by the options argument.
      var surveySendResult = function(surveyResults) {
        surveyServicePass.postRiskAppetiteData(surveyResults.data)
        .subscribe(postResponse => {
          var riskAppetiteResponse = postResponse.json
          surveyServicePass.getRiskAppetiteData(riskAppetiteResponse)
        });
      };

      Survey.SurveyNG.render("surveyElement",
      {
        model: survey,
        onComplete: surveySendResult
      });
    });
  };
}
