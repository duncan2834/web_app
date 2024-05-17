var stripe = Stripe(STRIPE_PUBLISHABLE_KEY)
var elem = document.getElementById('submit');  // lấy các cái có id là submit

clientsecret = elem.getAttribute('data-secret');  // Lấy giá trị client_secret từ thuộc tính data-secret của cái elem trên
var elements = stripe.elements();  // Tạo đối tượng elements để quản lý các yếu tố UI cho thanh toán.
var style = {  // Định nghĩa style cho thẻ tín dụng, với màu chữ, khoảng cách dòng và cỡ chữ.
    base: {
      color: "#000",
      lineHeight: '2.4',
      fontSize: '16px'
    }
    };
var card = elements.create("card", { style: style });  // Tạo một đối tượng card cho phần tử nhập thông tin thẻ tín dụng với style trên
card.mount("#card-element"); // Gắn phần tử card này vào một phần tử HTML có ID card-element.   

card.on('change', function(event) {  // nghe sự kiện change từ card
    var displayError = document.getElementById('card-errors')
    if (event.error) {
      displayError.textContent = event.error.message;   // có lỗi thì hiển thị thông báo lỗi và thêm css 
      $('#card-errors').addClass('alert alert-info');
    } else {
      displayError.textContent = '';  // không có lỗi thì xóa tbao lỗi và remove css trước đấy
      $('#card-errors').removeClass('alert alert-info');
    }
    });
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    
    var custName = document.getElementById("custName").value;
    var custAdd = document.getElementById("custAdd").value;
    var custAdd2 = document.getElementById("custAdd2").value;
    var postCode = document.getElementById("postCode").value;
    
    
      $.ajax({  // Gửi yêu cầu AJAX để lưu thông tin đơn hàng lên server.

        type: "POST",
        url: 'http://127.0.0.1:8000/orders/add/',
        data: {
          order_key: clientsecret,   // nhận diện xem là thằng nào order
          csrfmiddlewaretoken: CSRF_TOKEN,
          action: "post",
        },
        success: function (json) {
          console.log(json.success)
          stripe.confirmCardPayment(clientsecret, {  // xác nhận thanh toán với stripe bằng clientsecret
            payment_method: {  // định nghĩa thông tin thẻ, thanh toán
              card: card,
              billing_details: {
                address:{
                    line1:custAdd,
                    line2:custAdd2
                },
                name: custName
              },
            }
          }).then(function(result) {
            if (result.error) {
              console.log('payment error')
              console.log(result.error.message);
            } else {
              if (result.paymentIntent.status === 'succeeded') {
                console.log('payment processed')
                // có thể người dùng tắt trình duyệt trước khi payment succeed nên cần cái này
                window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
              }
            }
          });
    
        },
        error: function (xhr, errmsg, err) {},
      });
    
    
    
    });