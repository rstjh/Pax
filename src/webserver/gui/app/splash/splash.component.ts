import { Component } from '@angular/core';

interface SplashLink {
	title: string;
	description: string;
	icon: string;
	route: string;
}

interface SplashGroup {
	name: string;
	description: string;
	links: SplashLink[];
}

@Component({
	selector: 'splash',
	templateUrl: 'app/splash/splash.component.html'
})

export class SplashComponent {
	groups: SplashGroup[] = [
		{
			name: 'Model',
			description: 'Define what you\'re defending, top-down.',
			links: [
				{ title: 'Capability Model', description: 'Build the capability hierarchy, imported from a Word doc or entered by hand.', icon: 'fa-sitemap', route: 'capabilities' },
				{ title: 'Asset Register', description: 'Catalogue IT assets and link each one back to a capability.', icon: 'fa-server', route: 'assets' },
				{ title: 'Control Register', description: 'Track security controls, ownership, cost and effectiveness.', icon: 'fa-shield', route: 'controls' }
			]
		},
		{
			name: 'Assess',
			description: 'Score risk against the ATT&CK lifecycle with FAIR.',
			links: [
				{ title: 'ATT&CK Coverage Matrix', description: 'Heatmap of control coverage across MITRE ATT&CK tactics and techniques.', icon: 'fa-th-large', route: 'attack-coverage' },
				{ title: 'Risk Assessment', description: 'Score a risk with FAIR — loss event frequency × loss magnitude.', icon: 'fa-calculator', route: 'risk-assessment' },
				{ title: 'Risk Register', description: 'Every assessed risk, with owner, treatment and review status.', icon: 'fa-list-alt', route: 'risk-register' },
				{ title: 'Assessment Wizard', description: 'Guided, step-by-step risk assessment across a capability\'s assets.', icon: 'fa-magic', route: 'assessment-wizard' }
			]
		},
		{
			name: 'Plan & report',
			description: 'Turn residual risk into a sequenced, justified plan.',
			links: [
				{ title: 'Dashboard', description: 'Residual risk, top coverage gaps and roadmap status at a glance.', icon: 'fa-tachometer', route: 'dashboard' },
				{ title: 'Roadmap', description: 'Candidate controls ranked by ROI, sequenced into a quarterly plan.', icon: 'fa-road', route: 'roadmap' },
				{ title: 'Reports', description: 'Export a summary report as a downloadable Word document.', icon: 'fa-file-word-o', route: 'reports' }
			]
		},
		{
			name: 'Simulation',
			description: 'The original attack/defend course-of-action tools.',
			links: [
				{ title: 'System', description: 'Interactive network risk graph and course-of-action planning.', icon: 'fa-share-alt', route: 'risk-graph' },
				{ title: 'Actions', description: 'Review action templates and instances.', icon: 'fa-bolt', route: 'actions' },
				{ title: 'CVI', description: 'Cyber Vulnerability Index scoring.', icon: 'fa-line-chart', route: 'cvi' },
				{ title: 'Risk appetite', description: 'Configure organisational risk appetite.', icon: 'fa-sliders', route: 'risk-appetite' }
			]
		}
	];
}
