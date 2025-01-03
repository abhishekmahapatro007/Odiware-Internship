/** @odoo-module **/
import { registry } from "@web/core/registry";
// import { session } from "@web/session";
import { _t } from "@web/core/l10n/translation";
import {
	Component,
} from "@odoo/owl";
import { onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
// import { WebClient } from "@web/webclient/webclient";
//import { rpc } from "@web/core/network/rpc";
const actionRegistry = registry.category("actions");
export class PayrollDashboard extends Component {
	//
	setup() {
		// this.effect = useService("effect");
		// this.user = useService("user");
		this.action = useService("action");
		this.orm = useService("orm");
		// this.emp_graph = useRef("expense_graph");
		// this.leave_graph = useRef("leave_graph");
		// this.leave_trend = useRef("leave_trend");
		// this.payslips_graph = useRef("payslips_graph");
		// this.contracts_graph = useRef("contracts_graph");
		// this.time_off_graph = useRef("time_off_graph");
		this.state = useState({
			is_manager: false,
			// dashboards_templates: [
			// 	"PayrollManagerDashboard",
			// 	"EmployeeDetails",
			// 	"ManagerLeaveDashboard",
			// 	"PayrollChart",
			// ],
			login_employee: [],
		});

		console.log("Running");

		onWillStart(async () => {
			this.state.is_manager = false;
			var empDetails = await this.orm.call(
				"hr.employee",
				"get_user_employee_info",
				[]
			);
			if (empDetails) {
				this.state.login_employee = empDetails[0];
			}
		});
	}

	computeApplicantStageCount(jobData, stageName) {
		// console.log(jobData, stageName);
		const x = stageName.split(" ").join("_").toLowerCase();
		const x_postfix = x + "_count";

		return jobData[x_postfix] ?? 0;
	}

	async goToApplicants(jobId, stageName) {
		return this.env.services.action.doAction({
			name: _t("Filtered Applicants"),
			type: "ir.actions.act_window",
			res_model: "hr.applicant",
			domain: [
				["job_id", "=", jobId],
				["stage_id.name", "=", stageName],
			],
			views: [
				[false, "list"],
				[false, "kanban"],
				[false, "form"],
			],
			view_mode: "list,kanban,form",
			target: "current",
		});
	}

	payslips_click() {
		this.action.doAction({
			name: _t("Employee Payslips"),
			type: "ir.actions.act_window",
			res_model: "hr.applicant",
			view_mode: "tree,form,calendar",
			views: [
				[false, "list"],
				[false, "form"],
			],
			context: { create: false },
			domain: [["stage_id.name", "=", "Initial Qualification"]],
		});
	}

	hr_attendance() {
		this.action.doAction({
			name: _t("Employee Attendances"),
			type: "ir.actions.act_window",
			res_model: "hr.job",
			view_mode: "tree",
			views: [[false, "list"]],
			context: { create: false },
			//        domain : this.state.is_manager == true ? [] : [['employee_id','=', this.state.login_employee.id]]
		});
	}

	contracts_click() {
		this.action.doAction({
			name: _t("Employee Contracts"),
			type: "ir.actions.act_window",
			res_model: "hr.applicant",
			view_mode: "tree",
			views: [[false, "list"]],
			context: { create: false },
			domain: [
				"|",
				["stage_id.name", "=", "First Interview"],
				["stage_id.name", "=", "Second Interview"],
			],
		});
	}

	salary_click() {
		this.action.doAction({
			name: _t("Salary Rules"),
			type: "ir.actions.act_window",
			res_model: "hr.applicant",
			view_mode: "tree",
			views: [[false, "list"]],
			context: { create: false },
			domain: [["stage_id.name", "=", "Contract Signed"]],
		});
	}
	salary_structure_click() {
		this.action.doAction({
			name: _t("Salary Structures"),
			type: "ir.actions.act_window",
			res_model: "hr.payroll.structure",
			view_mode: "tree",
			views: [[false, "list"]],
			context: { create: false },
		});
	}
	leaves_to_approve() {
		this.action.doAction({
			name: _t("Leave Request"),
			type: "ir.actions.act_window",
			res_model: "hr.applicant",
			view_mode: "tree,form,calendar",
			views: [
				[false, "list"],
				[false, "form"],
			],
			target: "current",
		});
	}
}
actionRegistry.add("recruitment_dashboard", PayrollDashboard);
PayrollDashboard.template = "recruitment_dashboard.PayrollDashboardMain";
