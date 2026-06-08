# Story Map: <Project Name>

> **Outcome:** <one-line statement of what changes for whom if this succeeds>
> **Personas:** <comma-separated list>
> **Slicing strategy:** <walking-skeleton/mvp/r2 | pi-1/pi-2/pi-3 | now/next/later>

## Activity: <First user activity in the narrative>

### Task: <First task within this activity>

- [slice:walking-skeleton] [persona:<persona>] As a <persona>, I want to <action>, so that <outcome>
- [slice:mvp] [persona:<persona>] As a <persona>, I want to <action>, so that <outcome>
- [slice:r2] <story without persona dressing if internal>

### Task: <Second task within this activity>

- [slice:walking-skeleton] ...
- [slice:mvp] ...

## Activity: <Second user activity>

### Task: ...

- [slice:walking-skeleton] ...

<!--
Notes for the author of this map:

- Activities = backbone. Read them left-to-right; they should sound like a
  user narrative.
- Every activity must have at least one [slice:walking-skeleton] (or
  whatever your slice 1 is named) story. That's the rule that keeps slice 1
  end-to-end demoable.
- Slice tags are required on every story. The CSV/Mermaid scripts depend on
  them.
- Persona tag is optional; falls back to "As a <persona>" extraction.
- Stories without persona dressing (e.g., "Display loading spinner") are
  fine — don't pad them.
-->
