from passlib.apache import HtpasswdFile

def add_user_to_htpasswd(username, password, htpasswd_file_path):
    htpasswd = HtpasswdFile(htpasswd_file_path)

    # Mã hóa mật khẩu
    encrypted_password = htpasswd.hash(password)

    # Thêm người dùng mới vào tệp .htpasswd
    htpasswd.set_password(username, encrypted_password)

    # Lưu thay đổi
    htpasswd.save()

# Sử dụng hàm để thêm người dùng
add_user_to_htpasswd('ten_nguoi_dung', 'mat_khau_moi', '/etc/squid/.htpasswd')
