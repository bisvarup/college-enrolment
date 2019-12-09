# Database design

## Registration Fields

1. First name + Last Name
2. Full Address
3. Class 10 percentage
4. Class 12 percentage
5. Class 10 pdf upload
6. Class 12 pdf upload
7. Guardian name

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

### Registration Table

- id | integer | primary | auto increment
- student_id | integer
- Full name | string
- Address | string
- Guardian Name | string
- Class 10 percentage | string
- Class 12 percentage | string
- Class 10 pdf link | string
- Class 12 pdf link | string
- registration_time | string
- approved | boolean
