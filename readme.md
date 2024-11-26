# Event Manager

## Closed Issues

Here are links to the resolved issues during this project:

1. **[Internal Server Error (#5)](https://github.com/vvh24/event_manager/issues/5)**  
   Addressed an issue with the `users` table missing due to outdated migrations. Solution involved deleting Alembic migrations and rerunning `alembic upgrade head` to recreate the table structure.

2. **[SMTPServerDisconnected Errors (#4)](https://github.com/vvh24/event_manager/issues/4)**  
   Resolved email-related issues by ensuring Mailtrap credentials were properly configured and by implementing a fail-safe in the `email_service.py` for handling unconfigured SMTP clients.

3. **[Standardizing Login Error Messages (#3)](https://github.com/vvh24/event_manager/issues/3)**  
   Improved error messaging for login failures to provide clearer feedback to the user.

4. **[Password Validation (#2)](https://github.com/vvh24/event_manager/issues/2)**  
   Enhanced password validation logic to enforce stricter security requirements, including uppercase letters, numbers, and special characters.

5. **[Nickname Mismatch in Register API (#1)](https://github.com/vvh24/event_manager/issues/1)**  
   Fixed an issue where the generated nickname did not match the one provided in the API response. Adjusted the `user_service.py` logic to ensure consistency.

---

## Dockerized Project

## Reflection 

This project was a valuable learning experience in both technical and collaborative aspects. Technically, I gained a deeper understanding of Docker, SQLAlchemy migrations, SMTP integration, and error handling within a web application. Implementing features such as password validation, email verification, and role-based access control required diving into secure and scalable coding practices.

One of the main challenges was debugging the Internal Server Error caused by missing database tables. Identifying that outdated migrations were the root cause and resolving it through Alembic migrations taught me the importance of keeping migrations up to date. 

Another challenge was handling SMTP errors; I learned the value of fail-safes and logging to provide better diagnostics for issues related to third-party services.

In conclusion, this assignment enhanced my technical skills in backend development, debugging, and deployment. 

