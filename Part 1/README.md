Tight Coupling
All logic (DB, GUI, and business rules) is bundled in one file, making maintenance and updates harder.

Poor Scalability
As features grow, the single script becomes large and hard to manage. Not suitable for enterprise-scale applications.

Lack of Reusability
No modular design or service interface. External apps (mobile/web) cannot reuse the logic.

Difficult to Test
Testing becomes harder due to intertwined logic. No separation of concerns.

No Remote Access
It runs locally ,~~~~ no API or network access, so other systems can't communicate with it.

Tightly Bound UI
The logic is tied to a PyQt5 GUI — not suitable for web or mobile clients.