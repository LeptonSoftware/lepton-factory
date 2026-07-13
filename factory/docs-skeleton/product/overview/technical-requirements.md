---
title: Technical Requirements
summary: Externally binding technical constraints — platforms, integrations, compliance, performance and scale floors — that all features inherit.
owners: [product-owner]
applies_to: ["apps/**", "packages/**", "services/**"]
status: draft
last_verified: 2026-07-12
---

# Technical Requirements

This document holds the technical constraints that are product intent because they
are externally binding: platforms that must be supported, systems that must be
integrated, compliance regimes, and performance/scale/availability floors.
Internal technology choices do not belong here — those are architecture decisions
(`docs/architecture/`). Everything here is inherited by every FRD without
restating it.

## Platforms and environments

_To be written by the product owner._

## Required integrations

_External systems the product must interoperate with, and the binding contract for each._

## Compliance and data handling

_Regulatory regimes, data residency, retention, PII obligations._

## Performance, scale, and availability floors

_Measurable minimums (link to `success-metrics.md` where they overlap)._

## Placeholders to confirm

_The reality-operating-system shape in `product-description.md` implies constraints
(e.g. what the data fabric must connect to, what the agentic plane must host).
None are recorded as binding until the product owner confirms them here._
