# Operators Guide: Mesh, Tiers, Consortiums, and Registries

## Introduction
As an operator, you configure how the overlay meshes propagate and how route governance tiers apply limits to hints.

## Managing Propagation
Overlay propagation explicitly decays currentness and requires caveat preservation. Ensure that your mesh configurations (in `configs/overlay_mesh_governance/default.yaml`) enforce strict preservation.

## Handling Suppression
Consortium layers automatically suppress signals based on rule thresholds. Do not manually bypass these unless debugging; suppression prevents weak or conflicting data from masquerading as strong support.
