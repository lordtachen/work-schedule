## Project Structure

```
work-schedule-backend
├── data_structures       # data structures to be used in the project
│   ├── permission.py
│   └── user.py
├── db
│   ├── core.py           # ORM Base and Session Creator
│   ├── models.py         # ORM Models
│   ├── permission.py     # permission table access
│   └── user.py           # user table access
└── routes                # API endpoints
└── core                  # Business logic
utils                     # extra tooling
config                    # project data
main.py                   # entrypoint
```
