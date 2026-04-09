
from app.contexts.hrms.api.deduction_rule.deduction_rule_command_routes import deduction_rule_command_bp
from app.contexts.hrms.api.deduction_rule.deduction_rule_query_routes import deduction_rule_query_bp




def register_deduction_rule_routes(app) -> None:
    app.register_blueprint(deduction_rule_command_bp, url_prefix="/api/hrms")
    app.register_blueprint(deduction_rule_query_bp, url_prefix="/api/hrms")