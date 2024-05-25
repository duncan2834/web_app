# BÀI TẬP LỚN: THỰC HÀNH PHÁT TRIỂN HỆ THỐNG TRÍ TUỆ NHÂN TẠO 

THÀNH VIÊN: 
- TRẦN HỒNG ĐĂNG
- TRỊNH MINH HIẾU
- HOÀNG NGỌC HÀO
- TRẦN KIM THÀNH
# HƯỚNG DẪN
CLONE REPO VỀ
COMMANDS : (chạy môi trường ảo và install các gói trong requirement)
  - py -m venv venv
  - venv\Scripts\activate
  - pip install -r requirements.txt
  - manage.py runserver
- KHI KHÔNG CHẠY SCRIPTS ACTIVATE ĐƯỢC THÌ CHẠY Set-ExecutionPolicy Unrestricted -Scope Process RỒI CHẠY Scripts\activate
- LINK FIX: https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows
# ADMIN LOGIN
- http://127.0.0.1:8000/admin
- username: dang@a.com 
- pass: dang
# STRIPE CÁCH SỬ DỤNG(chạy trong cmd)
- stripe login
- stripe listen --forward-to localhost:8000/payment/webhook/
- 
