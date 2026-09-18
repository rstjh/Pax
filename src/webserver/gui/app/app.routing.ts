
import { RouterModule }                  from '@angular/router';

import { RiskGraphComponent }            from './risk-graph/risk-graph.component';
import { ActionsComponent }         	   from './actions/actions.component';
import { SurveyComponent }               from './survey/survey.component';
import { CVIComponent }         		     from './cvi/cvi.component';

import { NotFoundComponent }             from './not-found/not-found.component';

// Defender Risk & Control Roadmap Tool (Phase 1 — IT)
import { CapabilitiesComponent }         from './capabilities/capabilities.component';
import { ITAssetsComponent }             from './it-assets/it-assets.component';
import { ControlsComponent }             from './controls/controls.component';
import { AttackCoverageComponent }       from './attack-coverage/attack-coverage.component';
import { RiskAssessmentComponent }       from './risks/risk-assessment.component';
import { RiskRegisterComponent }         from './risk-register/risk-register.component';
import { AssessmentWizardComponent }     from './assessment-wizard/assessment-wizard.component';
import { RoadmapComponent }              from './roadmap/roadmap.component';
import { DashboardComponent }            from './dashboard/dashboard.component';
import { ReportsComponent }              from './reports/reports.component';


export const routing = RouterModule.forRoot([
	{ path: 'risk-appetite', component: SurveyComponent },
	{ path: '', component: RiskGraphComponent },
	{ path: 'risk-graph/:systemId', component: RiskGraphComponent },
	{ path: 'cvi', component: CVIComponent },
	{ path: 'actions', component: ActionsComponent },
	// Defender Risk & Control Roadmap Tool (Phase 1 — IT)
	{ path: 'dashboard', component: DashboardComponent },
	{ path: 'capabilities', component: CapabilitiesComponent },
	{ path: 'assets', component: ITAssetsComponent },
	{ path: 'controls', component: ControlsComponent },
	{ path: 'attack-coverage', component: AttackCoverageComponent },
	{ path: 'risk-assessment', component: RiskAssessmentComponent },
	{ path: 'risk-register', component: RiskRegisterComponent },
	{ path: 'assessment-wizard', component: AssessmentWizardComponent },
	{ path: 'roadmap', component: RoadmapComponent },
	{ path: 'reports', component: ReportsComponent },
	{ path: 'not-found', component: NotFoundComponent },
	{ path: '**', redirectTo: 'not-found' }
]);
