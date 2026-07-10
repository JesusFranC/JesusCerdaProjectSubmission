# Notes
## Things to note or mention during my presentation
1. Note that my code can be optimized with bulk loading
2. Add all SQL Statements to the document
3. Add erd to full presenation
4. I am re using my generic DAO from my pythonSQL assigmnent, as it is a generic data access tool and is portable for all SQL assignments
5. I have discovered how expensive database calls are, so I have modified my dao
6. Mention that I am using a Data Gateway style format for the application specific conversions and schema
7. Note for future, we can use bulk loading to improve efficiency, however for the scale of this project it is unnecessary
![](https://i.gyazo.com/24f4c4497a9e365a0d89a12d08c4196a.png)

```
--- Summary Statistics ---
                      date     temp_max     temp_min  precipitation   wind_speed
count                 2739  2739.000000  2739.000000    2739.000000  2739.000000
mean   2025-04-01 00:00:00    65.345674    52.696422       1.488353    11.119387
min    2024-01-01 00:00:00    50.300000    37.000000       0.000000     2.600000
25%    2024-08-16 00:00:00    59.700000    49.100000       0.000000     8.000000
50%    2025-04-01 00:00:00    63.900000    52.200000       0.000000    10.300000
75%    2025-11-15 00:00:00    69.900000    56.000000       0.100000    13.200000
max    2026-07-01 00:00:00   102.500000    71.100000      75.200000    35.700000
std                    NaN     7.682745     5.438036       5.329192     4.428436
Original row count: 2739
Rows removed:       0
Rows remaining:     2739


Clearing the db took 0.0627 seconds
Loading the db took 0.4078 seconds
The slower operation took 166.0344 seconds
```