# ERD Diagram for DB
- The following is going to represent the structure of my DB.

```mermaid
---
Weather locations and details ERD
---
erDiagram
    cities {
        int city_id PK
        string city_name
        decimal latitude
        decimal longitude
    }

    weather_records {
        int city_id PK
        date record_date PK
        decimal temp_max
        decimal temp_min
        decimal precipitation
        decimal wind_speed
    }

    cities ||--o{ weather_records : has
```