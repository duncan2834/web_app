from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# PasswordResetTokenGenerator là một lớp được sử dụng để tạo ra các mã thông báo (tokens) 
# để đặt lại mật khẩu người dùng. Khi người dùng yêu cầu đặt lại mật khẩu, 
# hệ thống sẽ tạo ra một mã thông báo duy nhất để gửi cho họ qua email hoặc một kênh khác.
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):   # tạo ra mã thông báo(tokens) để kích hoạt tài khoản người dùng.
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +    # pk là primary key 
            text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()