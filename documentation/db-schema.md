# Database design

## Tables

### Teacher Table

- user_id | primary | auto increment
- username | string
- password | string
- registered_on | string

### Student Table

- user_id | integer | primary | auto increment
- username | string
- password | string
- registered_on | string

### Courses

- course_id | integer | primary | auto increment
- course name
- faculty | string

### Registration Table

- id | integer | primary | auto increment
- student_id | integer
- Full name | string
- Guardian Name | string
- Class 10 percentage | string
- Class 12 percentage | string
- Class 10 pdf link | string
- Class 12 pdf link | string
- registration_time | string
- approved | boolean
