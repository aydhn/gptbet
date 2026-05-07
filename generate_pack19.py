import os
import json

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

write_file('configs/hardening/validation_corridors.yaml', """\
default_final_validation_strategy: conservative_final_validation
validation_corridor_rules:
  require_all_stages_lineage: true
  reject_stale_evidence: true
  preserve_no_safe_visibility: true
  preserve_sovereignty_visibility: true
""")

write_file('configs/hardening/release_gating_meshes.yaml', """\
release_gating_mesh_rules:
  reject_stale_blocker_state: true
  preserve_no_safe_visibility: true
  preserve_sovereignty_visibility: true
visibility_gap_severity_rules:
  no_safe_gap: critical
  sovereignty_gap: critical
""")

write_file('configs/hardening/operator_proof_packs.yaml', """\
operator_proof_pack_rules:
  reject_stale_pack_sections: true
  require_replayable_evidence: true
  preserve_no_safe_visibility: true
  preserve_sovereignty_visibility: true
executive_summary_honesty_rules:
  hide_raw_burden: false
""")

write_file('configs/hardening/replay_closure_compilers.yaml', """\
replay_closure_compiler_rules:
  reject_unresolved_residue: true
  reject_stale_replay_inputs: true
  preserve_no_safe_visibility: true
  preserve_sovereignty_visibility: true
residue_visibility_rules:
  hide_raw_residue: false
""")

write_file('configs/hardening/final_validation_budgets.yaml', """\
final_validation_budget_rules:
  stale_proof_budgets: explicit
  blocker_budgets: explicit
  replay_closure_residue_budgets: explicit
  operator_proof_gap_budgets: explicit
""")

write_file('configs/hardening/final_validation_ci.yaml', """\
ci_final_validation_release_blocking_rules:
  unresolved_high_severity_blocker: block
  over_budget_no_safe_loss: block
  over_budget_sovereignty_loss: block
stale_support_rejection_rules:
  reject_stale_validation_evidence: true
""")

# We will generate the Python files in the next step
