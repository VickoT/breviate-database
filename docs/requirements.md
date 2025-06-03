Requirements

Requirement ID | Requirement description
---------------|-------------------------
R1             | The system must read EggNOG raw annotation data from a TSV file.
R1.1           | The system must parse EggNOG data into a structured DataFrame.
R1.1.1         | The parsed data must be transformed into 1st Normal Form (1NF), with only atomic values.
R1.1.2         | The parsed data must be transformed into 2nd Normal Form (2NF), ensuring no partial dependencies.
R1.2           | The system must support exporting the parsed data into PostgreSQL-compatible tables. 
