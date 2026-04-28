from UI import UI
from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

dataStruct = UI()
print(dataStruct.studentID)
print(dataStruct.timeElpased)

with engine.connect() as conn:
    result = conn.execute(f"select {dataStruct.studentID}")
    conn.commit()