# 🔹 SQL for the Infosys Technical Interview

Every query below runs against the sample schema in the first block. The **Result** under each query is the real output from SQLite, and `tools/verify` re-runs every query in CI, so the results cannot drift. The syntax is standard SQL that also runs on MySQL 8 and PostgreSQL unless a note says otherwise.

## 🔹 Sample Schema

```sql
CREATE TABLE departments (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id           INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    email        TEXT    NOT NULL,
    dept_id      INTEGER REFERENCES departments(id),
    manager_id   INTEGER REFERENCES employees(id),
    salary       INTEGER NOT NULL,
    joining_date TEXT    NOT NULL
);

INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Sales'), (3, 'HR'), (4, 'Research');

INSERT INTO employees VALUES
    (1, 'Asha',   'asha@corp.in',   1, NULL, 150000, '2019-04-01'),
    (2, 'Ravi',   'ravi@corp.in',   1, 1,     90000, '2021-07-15'),
    (3, 'Meera',  'meera@corp.in',  1, 1,    160000, '2020-01-10'),
    (4, 'Kiran',  'kiran@corp.in',  2, NULL, 110000, '2018-11-20'),
    (5, 'Neha',   'neha@corp.in',   2, 4,     75000, '2023-02-01'),
    (6, 'Arjun',  'arjun@corp.in',  2, 4,     75000, '2022-09-30'),
    (7, 'Divya',  'divya@corp.in',  3, NULL,  60000, '2024-03-18'),
    (8, 'Ravi K', 'ravi@corp.in',   1, 1,     90000, '2024-06-01'),
    (9, 'Sam',    'sam@corp.in',    NULL, NULL, 50000, '2025-01-05');
```

---

## 🔹 1. Second highest salary

```sql
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**Result**
```text
second_highest
150000
```

* Works even when the top salary is shared. Returns `NULL` if there is no second value.
* Alternative: `SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;`

## 🔹 2. N-th highest salary (here N = 3) with `DENSE_RANK`

```sql
SELECT DISTINCT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 3;
```

**Result**
```text
salary
110000
```

* `DENSE_RANK` gives tied salaries the same rank and leaves **no gaps**; `RANK` would skip numbers after ties; `ROW_NUMBER` never ties.

## 🔹 3. Employees who earn more than their manager (self join)

```sql
SELECT e.name AS employee, m.name AS manager, e.salary, m.salary AS manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

**Result**
```text
employee | manager | salary | manager_salary
Meera | Asha | 160000 | 150000
```

## 🔹 4. Head-count and average salary per department (including empty departments)

```sql
SELECT d.name AS department, COUNT(e.id) AS employees, ROUND(AVG(e.salary), 2) AS avg_salary
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
GROUP BY d.id, d.name
ORDER BY employees DESC, department;
```

**Result**
```text
department | employees | avg_salary
Engineering | 4 | 122500
Sales | 3 | 86666.67
HR | 1 | 60000
Research | 0 | NULL
```

* `COUNT(e.id)` counts matched employees only, so `Research` shows 0. `COUNT(*)` would show 1 for it (the NULL-padded row).

## 🔹 5. Departments with more than 2 employees (`HAVING`)

```sql
SELECT d.name AS department, COUNT(*) AS employees
FROM employees e
JOIN departments d ON d.id = e.dept_id
GROUP BY d.id, d.name
HAVING COUNT(*) > 2;
```

**Result**
```text
department | employees
Engineering | 4
Sales | 3
```

* `WHERE` filters rows **before** grouping; `HAVING` filters groups **after** aggregation.

## 🔹 6. Highest-paid employee in each department

```sql
SELECT department, name, salary
FROM (
    SELECT d.name AS department, e.name, e.salary,
           RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rnk
    FROM employees e
    JOIN departments d ON d.id = e.dept_id
) ranked
WHERE rnk = 1
ORDER BY department;
```

**Result**
```text
department | name | salary
Engineering | Meera | 160000
HR | Divya | 60000
Sales | Kiran | 110000
```

## 🔹 7. Duplicate emails

```sql
SELECT email, COUNT(*) AS copies
FROM employees
GROUP BY email
HAVING COUNT(*) > 1;
```

**Result**
```text
email | copies
ravi@corp.in | 2
```

## 🔹 8. Delete duplicates, keep the lowest id

```sql
DELETE FROM employees
WHERE id NOT IN (SELECT MIN(id) FROM employees GROUP BY email);

SELECT COUNT(*) AS remaining FROM employees;
```

**Result**
```text
remaining
8
```

* MySQL refuses a subquery on the table being deleted from; wrap it: `... NOT IN (SELECT id FROM (SELECT MIN(id) AS id FROM employees GROUP BY email) keep)`.

## 🔹 9. Employees without a department, and departments without employees

```sql
SELECT 'employee' AS kind, e.name AS name
FROM employees e
LEFT JOIN departments d ON d.id = e.dept_id
WHERE d.id IS NULL
UNION ALL
SELECT 'department', d.name
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
WHERE e.id IS NULL;
```

**Result**
```text
kind | name
employee | Sam
department | Research
```

* `LEFT JOIN … WHERE right.id IS NULL` is the standard "anti-join". `UNION ALL` keeps duplicates; `UNION` removes them (and costs a sort/hash).

## 🔹 10. Running total of salaries by joining date

```sql
SELECT name, joining_date, salary,
       SUM(salary) OVER (ORDER BY joining_date) AS running_total
FROM employees
ORDER BY joining_date
LIMIT 4;
```

**Result**
```text
name | joining_date | salary | running_total
Kiran | 2018-11-20 | 110000 | 110000
Asha | 2019-04-01 | 150000 | 260000
Meera | 2020-01-10 | 160000 | 420000
Ravi | 2021-07-15 | 90000 | 510000
```

## 🔹 11. Top 2 earners per department (`ROW_NUMBER`)

```sql
SELECT department, name, salary
FROM (
    SELECT d.name AS department, e.name, e.salary,
           ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC, e.id) AS rn
    FROM employees e
    JOIN departments d ON d.id = e.dept_id
) ranked
WHERE rn <= 2
ORDER BY department, salary DESC;
```

**Result**
```text
department | name | salary
Engineering | Meera | 160000
Engineering | Asha | 150000
HR | Divya | 60000
Sales | Kiran | 110000
Sales | Neha | 75000
```

## 🔹 12. Salary bands with `CASE`

```sql
SELECT CASE
           WHEN salary >= 150000 THEN 'A'
           WHEN salary >= 90000  THEN 'B'
           ELSE 'C'
       END AS band,
       COUNT(*) AS employees
FROM employees
GROUP BY band
ORDER BY band;
```

**Result**
```text
band | employees
A | 2
B | 3
C | 4
```

## 🔹 13. Employees who joined after 2022, newest first

```sql
SELECT name, joining_date
FROM employees
WHERE joining_date > '2022-12-31'
ORDER BY joining_date DESC;
```

**Result**
```text
name | joining_date
Sam | 2025-01-05
Ravi K | 2024-06-01
Divya | 2024-03-18
Neha | 2023-02-01
```

* ISO dates (`YYYY-MM-DD`) compare correctly as text; in MySQL/PostgreSQL use a real `DATE` column.

## 🔹 14. Salary above the company average (subquery)

```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;
```

**Result**
```text
name | salary
Meera | 160000
Asha | 150000
Kiran | 110000
```

---

## 🔹 Quick Theory Answers

* **`DELETE` vs `TRUNCATE` vs `DROP`:** `DELETE` removes chosen rows (can have `WHERE`, fires triggers, can be rolled back in a transaction); `TRUNCATE` removes all rows quickly and resets storage (no `WHERE`; in many databases it cannot be rolled back); `DROP` removes the table itself.
* **Primary key vs unique key:** both are unique; a table has one primary key and it cannot be `NULL`; unique keys can be several and usually allow `NULL`.
* **Foreign key:** a column whose values must exist in another table's key — enforces referential integrity.
* **`INNER` / `LEFT` / `RIGHT` / `FULL` join:** matched rows only / all left rows / all right rows / all rows from both, with `NULL` where no match.
* **Index:** a sorted structure (usually a B+ tree) that makes lookups `O(log n)`; speeds reads, slows writes, costs space. Index columns used in `WHERE`, `JOIN`, `ORDER BY`.
* **View:** a stored query that behaves like a table; it does not store data itself (unless materialized).
