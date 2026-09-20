
import { NgModule }                  from '@angular/core';
import { BrowserModule }             from '@angular/platform-browser';
import { HttpClientModule }          from '@angular/common/http';
import { FormsModule }               from '@angular/forms';

import { ModalModule }               from 'ngx-bootstrap/modal';

import { ChartsModule }              from 'ng2-charts';

import { LeafletModule }             from '@asymmetrik/ngx-leaflet';
// import { LeafletDrawModule }         from '@asymmetrik/ngx-leaflet-draw';

import { NgxDatatableModule }        from '@swimlane/ngx-datatable';

import { AppComponent }              from './app.component';

import { SurveyComponent }           from './survey/survey.component';
import { RiskGraphComponent }        from './risk-graph/risk-graph.component';
import { ActionsComponent }          from './actions/actions.component';
import { CVIComponent }              from './cvi/cvi.component';

import { ActionWindow }              from './risk-graph/modals/action-modal/courses.action.modal';
import { AssetInfoWindow }           from './risk-graph/modals/asset-info/asset.info.modal';
import { ThreatInfoWindow }          from './risk-graph/modals/threat-info/threat.info.modal';

import { NavBarComponent }           from './navbar/navbar.component';
import { NotFoundComponent }         from './not-found/not-found.component';

// Defender Risk & Control Roadmap Tool (Phase 1 — IT)
import { CapabilitiesComponent }     from './capabilities/capabilities.component';
import { ITAssetsComponent }         from './it-assets/it-assets.component';
import { ControlsComponent }         from './controls/controls.component';
import { AttackCoverageComponent }   from './attack-coverage/attack-coverage.component';
import { RiskAssessmentComponent }   from './risks/risk-assessment.component';
import { RiskRegisterComponent }     from './risk-register/risk-register.component';
import { AssessmentWizardComponent } from './assessment-wizard/assessment-wizard.component';
import { RoadmapComponent }          from './roadmap/roadmap.component';
import { DashboardComponent }        from './dashboard/dashboard.component';
import { ReportsComponent }          from './reports/reports.component';

import { routing }                   from './app.routing';


@NgModule({
    imports: [
        ModalModule.forRoot(),
        LeafletModule,
  //       LeafletDrawModule.forRoot(),
        NgxDatatableModule,
        BrowserModule,
        HttpClientModule,
        FormsModule,
        ChartsModule,
        routing
    ],
    declarations: [
        AppComponent,
        SurveyComponent,
        RiskGraphComponent,
        ActionsComponent,
        CVIComponent,
        NavBarComponent,
        NotFoundComponent,
        ActionWindow,
        AssetInfoWindow,
        ThreatInfoWindow,
        CapabilitiesComponent,
        ITAssetsComponent,
        ControlsComponent,
        AttackCoverageComponent,
        RiskAssessmentComponent,
        RiskRegisterComponent,
        AssessmentWizardComponent,
        RoadmapComponent,
        DashboardComponent,
        ReportsComponent
    ],
    bootstrap: [
      AppComponent
    ],
    entryComponents: [
      ActionWindow,
      AssetInfoWindow,
      ThreatInfoWindow
    ]
})


export class AppModule {
}
