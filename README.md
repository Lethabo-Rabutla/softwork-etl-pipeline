## 📘 Softwork ETL Pipeline

**Author:** Lethabo Rabutla
**Repository:** `softwork-etl-pipeline`
**Last Updated:** August 2025

### Overview

This repository contains a production-ready **ETL (Extract, Transform, Load)** pipeline that ingests employee data from a CSV file, performs necessary data cleaning operations, and loads the sanitized data into a **PostgreSQL** database. The pipeline is modular, secure, and designed for scalability and easy integration with modern data workflows.

### Key Features

- Robust CSV ingestion with pandas
- Duplicate removal and missing value imputation
- Config-driven PostgreSQL integration using SQLAlchemy
- Modular design with externalized secrets
- Easy portability across environments

### Architecture

```
[CSV File]
   ↓
[pandas] ———> Clean → Transform → Impute
   ↓
[PostgreSQL Table: emp_table]
```

### Project Structure

```bash
softwork-etl-pipeline/
├── etl_pipeline.py        # Main ETL process script
├── db_config.py           # Local config file with secrets (excluded from Git)
├── requirements.txt       # Python dependencies
├── .gitignore             # Git exclusion rules
└── README.md              # Project documentation
```

### Setup Instructions

#### 1. Clone the Repository

#### 2. Create a Virtual Environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create Configuration File

```python
# db_config.py
db_username = 'your_username'
db_password = 'your_password'
db_host = 'localhost'
db_port = '5432'
db_name = 'your_database'
csv_file_path = '/absolute/path/to/Softwork_Technologies.csv'
```

#### 5. Run the ETL Pipeline

```bash
python etl_pipeline.py
```

### Data Cleaning Logic

| Step                           | Logic Applied                                 |
| ------------------------------ | --------------------------------------------- |
| Duplicate Handling             | `.drop_duplicates()` — keeps first occurrence |
| Missing `education`            | Filled with `'Not Specified'`                 |
| Missing `previous_year_rating` | Filled with `0`                               |

### Security & Configuration

- Database credentials and file paths are externalized in `db_config.py` for safety.
- This file is included in `.gitignore` to prevent leaking secrets.
- Consider using environment variables or secret managers (e.g., HashiCorp Vault, AWS Secrets Manager) in production.

---

### Testing & Validation

1. **Data Quality Checks:**

   - Confirmed nulls filled.
   - Duplicates dropped.

2. **PostgreSQL Validation:**

   - Ensure the table `emp_table` exists and matches schema.
   - Verify row count after upload equals post-clean DataFrame length.

### Example Output

```bash
Connection to PostgreSQL database established successfully.
Data loaded into PostgreSQL table 'emp_table' successfully.
Connection to PostgreSQL database closed.
ETL process completed successfully.
```

### 📬 Contact

**Author:** [Lethabo Rabutla](mailto:rabutlale@gmail.com)
**GitHub:** [RabutlaLethabo-personal](https://github.com/Lethabo-Rabutla)
