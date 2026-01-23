import pytest
from datetime import datetime, timezone
from ..app.services import registerService as svc
from ..app.db.transactions import Transactions


@pytest.fixture
def register_data():
    return {
        "email": "test@example.com",
        "mobile_number": "0787389913",
        "first_name": "Gayashan",
        "last_name": "Gamage",
        "password": "1234abcd.",
    }


@pytest.fixture
def db():
    # could be a real session fixture in your app; for unit tests a dummy is fine
    return object()


def test_register_raises_when_email_exists(monkeypatch, register_data, db):
    class FakeTransactions:
        @staticmethod
        def check_user_by_email(email, db):
            return {"id": 1}  # user exists

        @staticmethod
        def check_user_by_phonenumber(number, db):
            return None

    monkeypatch.setattr(svc, "Transactions", FakeTransactions)

    with pytest.raises(svc.UserEmailAlreadyExistsException) as exc:
        svc.registerService(register_data, db)

    assert "already exists" in str(exc.value).lower()


def test_register_raises_when_phone_exists(monkeypatch, register_data, db):
    class FakeTransactions:
        @staticmethod
        def check_user_by_email(email, db):
            return None

        @staticmethod
        def check_user_by_phonenumber(number, db):
            return {"id": 2}  # phone exists

    monkeypatch.setattr(svc, "Transactions", FakeTransactions)

    with pytest.raises(svc.UserNumberAlreadyExistsException) as exc:
        svc.registerService(register_data, db)

    assert "phone number" in str(exc.value).lower()


def test_register_success_creates_user_creates_otp_attempt_and_sends_sms(
    monkeypatch, register_data, db
):
    calls = {
        "create_user_payload": None,
        "create_user": None,
        "create_otp_attempt": None,
        "send_otp_sms": None,
        "hash_input": None,
    }

    # fixed OTP + fixed time to make assertions deterministic
    fixed_otp = "123456"
    fixed_now = datetime(2026, 1, 22, 10, 0, 0, tzinfo=timezone.utc)

    def fake_generate_otp_code():
        return fixed_otp

    def fake_build_user_payload(registerData, otp_code):
        calls["create_user_payload"] = {"registerData": registerData, "otp_code": otp_code}
        return {"email": registerData["email"], "mobile_number": registerData["mobile_number"], "otp": otp_code}

    def fake_hash_otp_code(code):
        calls["hash_input"] = code
        return "hashed-otp"

    def fake_send_otp_sms(recipient, otp_code):
        calls["send_otp_sms"] = {"recipient": recipient, "otp_code": otp_code}

    class FakeDatetime:
        @staticmethod
        def now(tz=None):
            # your code calls datetime.now(timezone.utc)
            return fixed_now

    class FakeTransactions:
        @staticmethod
        def check_user_by_email(email, db):
            return None

        @staticmethod
        def check_user_by_phonenumber(number, db):
            return None

        @staticmethod
        def create_user(payload, db):
            calls["create_user"] = {"payload": payload}
            return [{"id": 99}]

        @staticmethod
        def create_otp_attempt(payload, db):
            calls["create_otp_attempt"] = {"payload": payload}
            return {"id": 1}

    monkeypatch.setattr(svc, "Transactions", FakeTransactions)
    monkeypatch.setattr(svc, "generate_otp_code", fake_generate_otp_code)
    monkeypatch.setattr(svc, "build_user_payload", fake_build_user_payload)
    monkeypatch.setattr(svc, "hash_otp_code", fake_hash_otp_code)
    monkeypatch.setattr(svc, "send_otp_sms", fake_send_otp_sms)
    monkeypatch.setattr(svc, "datetime", FakeDatetime)

    res = svc.registerService(register_data, db)

    assert res == {
        "status": "success",
        "message": "User created. Verification code sent.",
    }

    # OTP generated and used in payload build
    assert calls["create_user_payload"]["otp_code"] == fixed_otp

    # user creation called with built payload
    assert calls["create_user"]["payload"]["otp"] == fixed_otp

    # otp attempt created with correct fields
    otp_payload = calls["create_otp_attempt"]["payload"]
    assert otp_payload["user_id"] == 99
    assert otp_payload["otp_hash"] == "hashed-otp"
    assert calls["hash_input"] == fixed_otp

    assert otp_payload["sent_at"] == fixed_now.isoformat()
    # expires should be +10 min
    assert otp_payload["expires_at"] == (fixed_now.replace() + svc.timedelta(minutes=10)).isoformat()
    assert otp_payload["send_count"] == 1
    assert otp_payload["status"] == "sent"

    # sms sent
    assert calls["send_otp_sms"] == {"recipient": register_data["mobile_number"], "otp_code": fixed_otp}


def test_register_success_user_not_created_still_sends_sms_but_no_otp_attempt(
    monkeypatch, register_data, db
):
    calls = {"create_otp_attempt_called": False, "send_otp_sms": None}

    def fake_send_otp_sms(recipient, otp_code):
        calls["send_otp_sms"] = {"recipient": recipient, "otp_code": otp_code}

    class FakeTransactions:
        @staticmethod
        def check_user_by_email(email, db):
            return None

        @staticmethod
        def check_user_by_phonenumber(number, db):
            return None

        @staticmethod
        def create_user(payload, db):
            return []  # simulate user not created / empty list

        @staticmethod
        def create_otp_attempt(payload, db):
            calls["create_otp_attempt_called"] = True

    monkeypatch.setattr(svc, "Transactions", FakeTransactions)
    monkeypatch.setattr(svc, "generate_otp_code", lambda: "999999")
    monkeypatch.setattr(svc, "build_user_payload", lambda rd, otp: {"x": "y"})
    monkeypatch.setattr(svc, "hash_otp_code", lambda x: "hashed")
    monkeypatch.setattr(svc, "send_otp_sms", fake_send_otp_sms)

    res = svc.registerService(register_data, db)

    assert res["status"] == "success"
    assert calls["create_otp_attempt_called"] is False
    assert calls["send_otp_sms"] == {"recipient": register_data["mobile_number"], "otp_code": "999999"}
