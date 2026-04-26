

def print_sizing_summary(manifest: SizingManifest):
    print("\n" + "=" * 50)
    print(" ADVANCED SIZING SUMMARY")
    print("=" * 50)
    print(f"Run ID:         {manifest.run_id}")
    print(f"Sport:          {manifest.sport}")
    print(f"Market:         {manifest.market}")
    print(f"Strategy:       {manifest.strategy}")
    print("-" * 50)

    s = manifest.summary
    print(f"Total Sized Decisions:    {s.total_sized_decisions}")
    print(f"Avg Raw Kelly Fraction:   {s.average_raw_kelly:.4f}")
    print(f"Avg Final Stake Fraction: {s.average_final_stake_fraction:.4f}")
    print(f"Decisions Capped:         {s.capped_decision_count}")
    print(f"Decisions Throttled:      {s.throttled_decision_count}")

    if s.skipped_sizing_reasons:
        print("\nSkip Reasons:")
        for reason, count in s.skipped_sizing_reasons.items():
            print(f"  {reason}: {count}")

    print("=" * 50 + "\n")
