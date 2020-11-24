class Punycode:
    @staticmethod
    def decode(string: str) -> str:
        return string.encode('utf-8').decode('idna')
