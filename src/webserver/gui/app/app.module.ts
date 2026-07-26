
import { NgModule }                  from '@angular/core';
import { BrowserModule }             from '@angular/platform-browser';
import { HttpClientModule }          from '@angular/common/http';

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

import { routing }                   from './app.routing';


@NgModule({
    imports: [
        ModalModule.forRoot(),
        LeafletModule,
  //       LeafletDrawModule.forRoot(),
        NgxDatatableModule,
        BrowserModule,
        HttpClientModule,
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
        ThreatInfoWindow
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
