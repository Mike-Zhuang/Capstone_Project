class EmergencyDecisionTree:
    def __init__(self):
        self.decision_tree = {
            "radiation_high": {
                "action": "activate_shield",
                "sub_decisions": {
                    "shield_active": "monitor_levels",
                    "shield_failed": "evacuate_to_inner_chamber"
                }
            },
            "toxic_gas": {
                "action": "seal_ventilation",
                "sub_decisions": {
                    "seal_successful": "activate_filters",
                    "seal_failed": "deploy_emergency_masks"
                }
            },
            "structural_damage": {
                "action": "assess_damage",
                "sub_decisions": {
                    "minor": "repair_immediately",
                    "major": "evacuate_section"
                }
            },
            "power_failure": {
                "action": "switch_to_backup",
                "sub_decisions": {
                    "backup_online": "diagnose_main",
                    "backup_failed": "activate_manual_generators"
                }
            }
        }
    
    def make_decision(self, emergency_type, severity="high", additional_data=None):
        """Make decisions based on emergency situations"""
        if emergency_type not in self.decision_tree:
            return self.default_response()
        
        decision = self.decision_tree[emergency_type]
        
        response = {
            "emergency": emergency_type,
            "severity": severity,
            "immediate_action": decision["action"],
            "sub_actions": [],
            "priority": self.calculate_priority(severity),
            "timestamp": "2024-01-15 14:30:00"  # Should use datetime.now() in production
        }
        
        # Add sub-actions based on severity
        if severity == "high":
            for sub_action in decision["sub_decisions"].values():
                response["sub_actions"].append(sub_action)
        
        # Add resource requirements
        response["resources_needed"] = self.estimate_resources(emergency_type, severity)
        
        return response
    
    def calculate_priority(self, severity):
        priorities = {"low": 3, "medium": 2, "high": 1}
        return priorities.get(severity, 3)
    
    def estimate_resources(self, emergency_type, severity):
        """Estimate resources required to handle emergency situations"""
        resource_map = {
            "radiation_high": {"energy": 50, "manpower": 2},
            "toxic_gas": {"filters": 3, "energy": 20},
            "structural_damage": {"materials": 100, "manpower": 5},
            "power_failure": {"backup_fuel": 200, "manpower": 3}
        }
        
        base = resource_map.get(emergency_type, {})
        
        # Adjust based on severity level
        multiplier = {"low": 0.5, "medium": 1.0, "high": 2.0}.get(severity, 1.0)
        
        return {k: v * multiplier for k, v in base.items()}
    
    def default_response(self):
        return {
            "emergency": "unknown",
            "immediate_action": "initiate_general_emergency_protocol",
            "sub_actions": ["seal_all_doors", "activate_backup_systems"],
            "priority": 1,
            "resources_needed": {"energy": 100, "manpower": 5}
        }