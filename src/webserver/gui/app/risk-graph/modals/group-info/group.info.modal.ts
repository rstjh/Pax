import { Component, OnInit, ViewEncapsulation } from '@angular/core';

import { BsModalRef, BsModalService } from 'ngx-bootstrap/modal';

import { ActionWindow, ActionWindowData } from '../action-modal/courses.action.modal';

import { AssetInfoService } from '../asset-info/asset.info.modal.service';



export class GroupInfoWindowData {
  constructor(public groupInfoData : {}) {}
}


@Component({
  selector: 'modal-content',
  templateUrl: './app/risk-graph/modals/group-info/group.info.modal.html',
  providers: [AssetInfoService]
})


export class GroupInfoWindow implements OnInit {
  context : GroupInfoWindowData;

  groupInfoData : any;
  groupName : any;
  groupFunction : any;
  groupRiskLevel : any;

  noThreats = 0;
  threatData = [];

  threatRows : any;
  threatSelected = [];

  maxRisk : any;
  maxRiskLabel : any;

  impactInfo = {
    'confidentiality' : 0,
    'integrity' : 0,
    'availability' : 0
  };

  assetRows : any;
  assetSelected = [];

  noActions = 0;
  actionRows = [];
  actionSelected = [];

  groupOverview = 0;
  actionOverview = 0;

  riskImpact = {
    'consequence': 10,
    'likelihood': 8
  };

  constructor(public dialog: BsModalRef, private modal: BsModalService, private assetInfoService: AssetInfoService) {
  };

  ngOnInit() {
    this.groupName = this.groupInfoData[0]['group'];
    this.groupFunction = this.groupInfoData[0]['function'];

    this.impactInfo['confidentiality'] = this.groupInfoData[0]['confidentiality']
    this.impactInfo['integrity'] = this.groupInfoData[0]['integrity']
    this.impactInfo['availability'] = this.groupInfoData[0]['availability']

    this.groupView();
  };

  groupView() {
    this.groupOverview = 1;
    this.actionOverview = 0;
    this.maxRisk = 0;

    for (var i = 0; i < this.groupInfoData.length; i++) {
      this.groupInfoData[i]['riskLabel'] = this.getRiskLabel(this.groupInfoData[i]['currentRiskScore']);
      this.assetInfoService.getThreatData(this.groupInfoData[i]['assetId'])
      .subscribe(threats => {
        var threatLength = threats.length;
        if (threatLength > 0) {
          for (var j = 0; j < threatLength; j++) {
            var threatId = threats[j]['id'];
            var inThisAlready = 0;
            if (this.threatData.length == 0) {
              this.threatData.push(threats[j]);
            } else {
              for (var k = 0; k < this.threatData.length; k++) {
                if (threatId === this.threatData[k]['id']) {
                  inThisAlready = 1;
                };
              };
              if (inThisAlready == 0) {
                this.threatData.push(threats[j]);
              };
            };
          };
        };
        if (this.threatData.length == 0) {
          this.noThreats = 1;
        } else {
          this.noThreats = 0;
          this.threatRows = this.threatData;
        };
      });
      if (this.groupInfoData[i]['currentRiskScore'] > this.maxRisk) {
        this.maxRisk = this.groupInfoData[i]['currentRiskScore'];
      };
    };

    this.maxRiskLabel = this.getRiskLabel(this.maxRisk);

    this.assetRows = this.groupInfoData;
  };

  actionView() {
    this.groupOverview = 0;
    this.actionOverview = 1;
    for (var i = 0; i < this.groupInfoData.length; i++) {
      this.getActions(this.groupInfoData[i]['assetId']);
    };
  };

  getActions(assetId) {
    this.assetInfoService.getActions(assetId)
    .subscribe(actionData => {
      for (var j = 0; j < actionData.length; j++) {
        var actionId = actionData[j]['id'];
        var inThisAlready = 0;
        if (this.actionRows.length == 0) {
          if (actionData[j]['staged'] == 1) {
            actionData[j]['actionStatus'] = 'Remove action';
          } else {
            actionData[j]['actionStatus'] = 'Stage action';
          };
          this.actionRows.push(actionData[j]);
        } else {
          for (var k = 0; k < this.actionRows.length; k++) {
            if (actionId === this.actionRows[k]['id']) {
              inThisAlready = 1;
            };
          };
          if (inThisAlready == 0) {
            if (actionData[j]['staged'] == 1) {
              actionData[j]['actionStatus'] = 'Remove action';
            } else {
              actionData[j]['actionStatus'] = 'Stage action';
            };
            this.actionRows.push(actionData[j]);
          };
        };
      };
      if (this.actionRows.length > 0) {
        this.noActions = 0;
      } else {
        this.noActions = 1;
      };
    });
  };

  toggleActiveAction(event, action) {
    if (action['staged']) {
      action['staged'] = 0;
      action.actionStatus = 'Stage action';
    } else {
      action['staged'] = 1;
      action.actionStatus = 'Remove action';
    };

    this.assetInfoService.toggleAction(action['actionId'], action['staged'])
    .subscribe(activeData => {
      for (var i = 0; i < this.groupInfoData.length; i++) {
        this.getActions(this.groupInfoData[i]['id']);
      };
    });
  };

  getRiskLabel(riskScore) {
    if (riskScore >= 10) {
      return 'Critical';
    } else if (riskScore >= 7.5) {
      return 'High';
    } else if (riskScore >= 5) {
      return 'Medium';
    } else if (riskScore >= 2.5) {
      return 'Low';
    } else {
      return 'Very low';
    };
  };

  onSelect({ selected }) {
  };

  onClickActionTable(event) {
    // Pre-existing bug (not introduced by the Angular migration): ActionWindowData
    // requires systemId/objectiveData/actorData/parentTasks, none of which this
    // component has available. Left broken at the user's direction.
    return this.modal.show(ActionWindow, { initialState: new (ActionWindowData as any)(event.row, this.riskImpact), class: 'modal-lg' });
  };

  closeModal() {
    this.dialog.hide();
  };
}
