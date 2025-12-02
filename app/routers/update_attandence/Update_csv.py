from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.Students_models import Student
from app.models.Users_models import User
from app.database import get_sqlite_session, get_sql_session
import csv
import io

router = APIRouter(prefix="/students")


@router.post("/technothon")
async def upload_and_update_technothon_csv(
    file: UploadFile = File(...),
    sqlite_db: AsyncSession = Depends(get_sqlite_session),   # SQLite session
    mysql_db: AsyncSession = Depends(get_sql_session)        # MySQL session
):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    try:
        content = await file.read()
        csv_text = content.decode("utf-8")
        csv_reader = csv.reader(io.StringIO(csv_text))

        header = next(csv_reader, None)
        if not header:
            raise HTTPException(status_code=400, detail="CSV is empty")

        inserted = 0
        updated = 0

        for row in csv_reader:
            if len(row) < 4:
                continue

            try:
                student_id = int(row[0])
                name = row[1].strip()
                batch = row[2].strip()
                percentage = float(row[3].strip().replace("%", ""))
            except Exception:
                continue

            # -----------------------------
            # UPDATE IN SQLITE (Students)
            # -----------------------------
            stmt = select(Student).where(Student.Student_ID == student_id)
            result = await sqlite_db.execute(stmt)
            student = result.scalar_one_or_none()

            # -----------------------------
            # UPDATE IN MYSQL (Users)
            # -----------------------------
            stmt2 = select(User).where(User.Student_ID == student_id)
            result2 = await mysql_db.execute(stmt2)
            user = result2.scalar_one_or_none()

            if student:
                # UPDATE existing record in SQLite
                student.Name = name
                student.Batch = batch
                student.Overall_Percentage = percentage

                # UPDATE corresponding record in MySQL
                if user:
                    user.Name = name
                    user.Batch = batch
                    user.Overall_Percentage = percentage

                updated += 1

            else:
                # INSERT into SQLite only
                new_student = Student(
                    Student_ID=student_id,
                    Name=name,
                    Batch=batch,
                    Overall_Percentage=percentage
                )
                sqlite_db.add(new_student)
                inserted += 1

                # Optional: Insert into MySQL if needed
                # Only if you want new entries also in Users table

        # Commit both DBs
        await sqlite_db.commit()
        await mysql_db.commit()

        return {
            "message": "CSV processed successfully",
            "inserted": inserted,
            "updated": updated
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
