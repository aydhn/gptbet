# Policy Bundle and Overlay Guide for Operators

## Bundles
Bundles contain sets of rule records targeting specific families of behavior (e.g., safety, rollout limits). These are assigned to channels or planes and control what operations are allowed.

## Overlays
Overlays enable adding runtime exceptions to a base bundle without modifying the base bundle directly.

### Best Practices
- Keep base bundles small and distinct.
- Avoid stacking overlays unnecessarily.
- Set explicit expiry on emergency overlays.
