
### DB Schema

#### Users
* Id
* email
* password_hash
* created_at
* is_active

#### jobs
* id
* user_id (FK)
* name
* hourly_rate (DECIMAL 10,2)
* currency
* is_active
* created_at

#### shifts
* id
* job_id(FK)
* user_id (FK)
* start_time (DATETIME)
* end_time (DATETIME)
* source (ENUM: manual/ics)
* ics_uid (VARCHAR, nullable)
* notes
* created_at

UNIQUE(user_id, ics_uid) <- prevents duplicate ICS imports

#### Payslip snapshots <- optional: cache computed payslips
* id
* user_id(FK)
* job_id (FK)
* month (DATE) <- store as first of month
* gross
* tax 
* net
* hours_worked
* computed_at

### Decisions worth noting
* ics_uid + unique constraints handles deduplication cleanly - no application-level checking needed
* DECIMAL for money, never FLOAT
* payslip_snapshots is early on but important once users want to view historical payslips without recomputing
* user_id on shifts is denormalized for query convenience - defensible here