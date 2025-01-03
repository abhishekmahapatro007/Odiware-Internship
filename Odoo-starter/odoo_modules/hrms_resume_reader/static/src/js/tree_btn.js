/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { useService } from "@web/core/utils/hooks";

export class ApplicantListController extends ListController {
   setup() {
       super.setup();
       this.action = useService("action");
   }
   async onClickAddFromResume() {
       this.action.doAction({
          name: 'Add Applicant from Resume',
          type: 'ir.actions.act_window',
          res_model: 'applicant.record.wizard',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}

registry.category("views").add("button_in_applicant_tree", {
   ...listView,
   Controller: ApplicantListController,
   buttonTemplate: "parse_btn.ListView.Buttons",
});