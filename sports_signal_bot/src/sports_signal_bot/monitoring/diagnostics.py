def print_diagnostics(health_score):
    print(f"Health Score: {health_score.global_score}")
    for comp_name, comp in health_score.components.items():
        print(f"  {comp_name}: {comp.score} [{comp.status}]")
