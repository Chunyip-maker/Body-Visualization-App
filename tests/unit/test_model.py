import pytest

from model import *

class Test_Model:
    def setup(self):
        self.model = Model()

    def test_check_user_input(self):
        result = self.model.check_user_input("")
        assert result == False

        result = self.model.check_user_input("*"*60)
        assert result == False

        result = self.model.check_user_input("##")
        assert result == False

        result = self.model.check_user_input("12344")
        assert result == True

    def test_define_basic_model(self):
        result = self.model.define_basic_model(18,"female")
        assert result == "teenager_female"

        result = self.model.define_basic_model(35,"male")
        assert  result == "adult_male"

        result = self.model.define_basic_model(50, "male")
        assert result == "middle_male"

        result = self.model.define_basic_model(70,"male")
        assert result == "old_male"