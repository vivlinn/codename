## Dingen uitsluiten
- Breadth first
1. Voor elk huis de afstand tot alle batterijen bepalen
2. Sorteren
3. Huizen aan eerste batterij koppelen als dat mogelijk is wat betreft capaciteit

#### Baseline
1. Itereren over elk huis
    - Kies random batterij
    - Check de capaciteit
        - Als dat goed is ga door
        - Anders check volgende batterij
    - Volgens Breadth first kabel leggen