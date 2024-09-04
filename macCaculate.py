import hashlib
import urllib.parse


class CheckMacValueService:
    METHOD_MD5 = 'md5'
    METHOD_SHA256 = 'sha256'

    def __init__(self, key, iv, method=METHOD_SHA256):
        self.hash_key = key
        self.hash_iv = iv
        self.method = method

    def append(self, source, is_sort=True):
        """附加 CheckMacValue"""
        source[self.get_field_name()] = self.generate(source)
        if is_sort:
            source = self.sort(source)
        return source

    def filter(self, source):
        """檢查碼參數過濾"""
        if self.get_field_name() in source:
            del source[self.get_field_name()]
        return source

    def generate(self, source):
        """產生檢查碼"""
        filtered = self.filter(source)
        sorted_params = self.sort(filtered)
        combined = self.to_encode_source_string(sorted_params)
        encoded = self.ecpay_url_encode(combined)
        hash_value = self.generate_hash(encoded)
        check_mac_value = hash_value.upper()
        return check_mac_value

    def generate_hash(self, source):
        """產生雜湊值"""
        if self.method == self.METHOD_SHA256:
            return hashlib.sha256(source.encode('utf-8')).hexdigest()
        return hashlib.md5(source.encode('utf-8')).hexdigest()

    def get_field_name(self):
        """取得壓碼欄位名稱"""
        return 'CheckMacValue'

    def set_method(self, method):
        """設定雜湊方式"""
        self.method = method

    def sort(self, source):
        """排序參數"""
        return dict(sorted(source.items()))

    def to_encode_source_string(self, source):
        """轉換為編碼來源字串"""
        combined = f'HashKey={self.hash_key}'
        for name, value in source.items():
            combined += f'&{name}={value}'
        combined += f'&HashIV={self.hash_iv}'
        return combined

    def ecpay_url_encode(self, source):
        """進行 ECPay 特殊 URL encode"""
        # ECPay 要求的特殊 URL encode 規範
        encoded_string = urllib.parse.quote_plus(source).lower()
        return encoded_string.replace('%2d', '-')

    def verify(self, source):
        """檢核檢查碼"""
        check_mac_value = self.generate(source)
        return check_mac_value == source[self.get_field_name()]
