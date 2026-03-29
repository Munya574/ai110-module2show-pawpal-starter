# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- Let a user enter basic owner + pet info
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)

- What classes did you include, and what responsibilities did you assign to each?
- Owner
Attributes: name, available_minutes (total time in a day)
Responsibility: Represents the human's constraints
- Pet
Attributes: name, species, age
Responsibility: Holds pet identity; could influence task defaults (e.g., a senior dog needs shorter walks)
- Task
Attributes: name, duration_minutes, priority (1–5), category (walk/feed/meds/etc.), preferred_time (optional: morning/afternoon/evening)
Responsibility: A single care activity with all its metadata
- Scheduler
Attributes: owner, pet, tasks[]
Methods: add_task(), generate_plan(), explain_plan()
Responsibility: Core logic — takes tasks + constraints and produces a prioritized daily plan

Relationships: Scheduler has-a Owner, has-a Pet, has-many Task


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
- Added a `scheduled_tasks` attribute and explicit return type hints to `Scheduler` so the plan lifecycle is clearer and future logic bottlenecks are reduced.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
- The current scheduler detects conflicts only for exact matching due date/time stamps rather than checking overlapping duration windows, which keeps the logic light but misses partial overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
