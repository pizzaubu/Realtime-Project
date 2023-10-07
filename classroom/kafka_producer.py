from kafka import KafkaProducer
import json

# ตั้งค่า Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', 
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_assignment_message(assignment_data):
    """
    ส่งข้อมูลเกี่ยวกับ assignment ที่ถูกสร้างขึ้นไปยัง Kafka topic.
    """
    topic_name = 'classroom_notifications'
    producer.send(topic_name, assignment_data)
    producer.flush()

def send_announcement_message(announcement_data):
    """
    ส่งข้อมูลเกี่ยวกับประกาศในชั้นเรียนที่ถูกสร้างขึ้นไปยัง Kafka topic.
    """
    topic_name = 'classroom_notifications'
    producer.send(topic_name, announcement_data)
    producer.flush()

def send_course_creation_message(course_data):
    """
    ส่งข้อมูลเกี่ยวกับ course ที่ถูกสร้างขึ้นไปยัง Kafka topic.
    """
    topic_name = 'classroom_notifications'
    producer.send(topic_name, course_data)
    producer.flush()

def send_assignment_submission_message(submission_data):
    """
    ส่งข้อมูลเมื่อ student ส่ง assignment ขึ้นไปยัง Kafka topic.
    """
    topic_name = 'classroom_notifications'
    producer.send(topic_name, submission_data)
    producer.flush()

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    assignment_data_example = {
        'type': 'assignment',
        'assignment_id': 1,
        'title': 'การบ้าน #1',
        'description': 'โปรดทำและส่งก่อนวันที่ 20 กันยายน',
        'due_date': '20-09-2023'
    }
    send_assignment_message(assignment_data_example)

    announcement_data_example = {
        'type': 'announcement',
        'announcement_id': 1,
        'title': 'ข่าวประกาศ!',
        'body': 'ตารางสอบปลายภาคได้รับการปรับเปลี่ยน, โปรดตรวจสอบเวลาสอบใหม่'
    }
    send_announcement_message(announcement_data_example)

course_data_example = {
    'type': 'course_creation',
    'course_id': 101,
    'subject_name': 'คณิตศาสตร์',
    'teach_date': 'ทุกวันจันทร์',
    'start_time': '09:00',
    'end_time': '10:30'
}
send_course_creation_message(course_data_example)

# ตัวอย่างการใช้งานสำหรับการส่ง assignment
submission_data_example = {
    'type': 'assignment_submission',
    'assignment_id': 1,
    'student_id': 1001,
    'submitted_date': '19-09-2023',
    'file_path': 'path/to/submitted/file.pdf'
}
send_assignment_submission_message(submission_data_example)