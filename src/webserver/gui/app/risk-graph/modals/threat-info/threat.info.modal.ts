import { Component } from '@angular/core';

import { BsModalRef } from 'ngx-bootstrap/modal';



export class ThreatInfoWindowData {
  constructor(public threatInfoData: {}) {}
}


@Component({
  selector: 'modal-content',
  templateUrl: './app/risk-graph/modals/threat-info/threat.info.modal.html',
  providers: []
})


export class ThreatInfoWindow {
  threatInfoData : any;

  constructor(public dialog: BsModalRef) {
  };

  closeModal() {
    this.dialog.hide();
  };
}
