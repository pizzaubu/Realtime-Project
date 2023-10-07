from kafka import KafkaConsumer
import json

# ตั้งค่า KafkaConsumer
consumer = KafkaConsumer(
    'classroom_notifications',  # ชื่อ topic ที่ต้องการ consume
    bootstrap_servers='localhost:9092',  # ที่อยู่ของ Kafka broker
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest',  # เริ่มรับข้อความจากข้อความล่าสุด
    group_id='classroom_group',  # ระบุ group id สำหรับ consumer นี้
)

print("Starting the consumer...")
for message in consumer:
    data = message.value
    notification_type = data.get('type')
    
    if notification_type == 'assignment':
        print(f"New Assignment: {data['message']}")
    elif notification_type == 'announcement':
        print(f"Class Announcement: {data['message']}")
    # คุณสามารถเพิ่มเงื่อนไขเพิ่มเติมได้ตามความต้องการ
